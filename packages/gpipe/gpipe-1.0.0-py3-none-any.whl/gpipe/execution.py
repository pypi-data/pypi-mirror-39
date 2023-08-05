#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import abc
import enum
import functools
import os
import shlex
import subprocess

import lxml.etree
from logzero import logger

from .benchmark import benchmark
from .templating import get_jinja2_environment


# ================================================================================
# interface
# ================================================================================

class WorkflowExecutor(metaclass=abc.ABCMeta):
    def __init__(self, global_config, workflow):
        self.global_config = global_config
        self.workflow = workflow

    @abc.abstractclassmethod
    def submit(self, dry_run=False):
        raise NotImplementedError   # NOQA

    @abc.abstractclassmethod
    def cancel(self, force=False):
        raise NotImplementedError   # NOQA


class TaskStatus(enum.Enum):
    PENDING = 1
    RUNNING = 2
    ERROR = 3


# ================================================================================
# GridEngine executor
# ================================================================================

class AbstractGridEngineWorkflowExecutor(WorkflowExecutor):
    SINGLE_SCRIPT_TEMPLATE_CONFIG_KEY = None
    SINGLE_SCRIPT_TEMPLATE = None
    ARRAY_SCRIPT_TEMPLATE_CONFIG_KEY = None
    ARRAY_SCRIPT_TEMPLATE = None
    SUBMIT_COMMAND_CONFIG_KEY = None
    SUBMIT_COMMAND = None
    STATUS_COMMAND_CONFIG_KEY = None
    STATUS_COMMAND = None
    CANCEL_COMMAND_CONFIG_KEY = None
    CANCEL_COMMAND = None

    def submit(self, dry_run=False):
        #
        logger.info('Checking outdated files...')
        with benchmark('Outdated file detection'):
            task_groups = list(self.workflow.get_task_groups())

        #
        logger.info('Gnerating task script(s)...')

        submit_scripts = []
        makedirs_cached = functools.lru_cache(maxsize=None)(lambda p: os.makedirs(p, exist_ok=True))

        for tasks in task_groups:
            remailing_tasks = [t for t in tasks if not t.completed]
            if not remailing_tasks:
                continue

            use_array = len(tasks) > 1
            for path, script, submit in self._generate_scripts(remailing_tasks, use_array):
                path = os.path.join(self.workflow.runfile.gpipe.log_directory, path)
                makedirs_cached(os.path.dirname(path))

                with open(path, 'w') as fout:
                    fout.write(script)

                if submit:
                    submit_scripts.append(path)

        if not submit_scripts:
            logger.info('No remailing task.')
            return

        #
        if dry_run:
            logger.info('The following script(s) were generated:')
            for path in submit_scripts:
                logger.info('  * %s', os.path.relpath(path, os.getcwd()))

        else:
            for path in submit_scripts:
                logger.info('Submit %s', path)
                self._submit_script(path)

    def _generate_scripts(self, tasks, use_array):
        if use_array:
            yield f'{tasks[0].name}.sh', self._generate_array_script(tasks), True
            for task in tasks:
                path = os.path.join('array', f'{task.name}.{task.index:06d}.sh')
                yield path, self._generate_single_script(task), False

        else:
            yield f'{tasks[0].name}.sh', self._generate_single_script(tasks[0]), True

    def _generate_single_script(self, task):
        template = self._get_template(
            self.SINGLE_SCRIPT_TEMPLATE_CONFIG_KEY,
            self.SINGLE_SCRIPT_TEMPLATE_PATH
        )
        return template.render({
            'gpipe': self.workflow.runfile.gpipe,
            'task': task
        })

    def _generate_array_script(self, tasks):
        template = self._get_template(
            self.ARRAY_SCRIPT_TEMPLATE_CONFIG_KEY,
            self.ARRAY_SCRIPT_TEMPLATE_PATH
        )
        return template.render({
            'gpipe': self.workflow.runfile.gpipe,
            'tasks': tasks
        })

    def _get_template(self, config_key, default):
        path = self.global_config.get(config_key, default)
        with open(path) as fin:
            return get_jinja2_environment().from_string(fin.read())

    def _submit_script(self, path):
        command = self.global_config.get(self.SUBMIT_COMMAND_CONFIG_KEY, self.SUBMIT_COMMAND)
        subprocess.check_output(shlex.split(command) + [path])

    def status(self):
        for id, name, status in self._get_status():
            logger.info('%6s [%-7s] %s', id, str(status).split('.')[1], name)

    @abc.abstractmethod
    def _get_status(self):
        raise NotImplementedError   # NOQA

    def cancel(self, force=False):
        #
        tasks = list(self._get_status())
        if not tasks:
            logger.info('No task queued.')
            return

        #
        running_tasks = [(i, n) for i, n, s in tasks if s == TaskStatus.RUNNING]
        if running_tasks:
            logger.warn('The following tasks are still running:')
            for id, name in sorted(set(running_tasks)):
                logger.warn('  * %6s: %s', id, name)

            if not force:
                return

        #
        task_id_name_map = {}
        for id, name, _ in tasks:
            if id not in task_id_name_map:
                task_id_name_map[id] = name

        logger.info('Cancelling tasks:')
        for id, name in sorted(task_id_name_map.items()):
            logger.warn('  * %6s: %s', id, name)
            self._cancel_task(id)

    def _cancel_task(self, id):
        command = self.global_config.get(self.CANCEL_COMMAND_CONFIG_KEY, self.CANCEL_COMMAND)
        subprocess.check_call(shlex.split(command) + [id])


class SGEWorkflowExecutor(AbstractGridEngineWorkflowExecutor):
    TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    SINGLE_SCRIPT_TEMPLATE_CONFIG_KEY = 'gpipe.sge.single_script_template'
    SINGLE_SCRIPT_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'sge-single.sh.j2')
    ARRAY_SCRIPT_TEMPLATE_CONFIG_KEY = 'gpipe.sge.array_script_template'
    ARRAY_SCRIPT_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'sge-array.sh.j2')
    SUBMIT_COMMAND_CONFIG_KEY = 'gpipe.sge.submit_command'
    SUBMIT_COMMAND = 'qsub -tearse'
    STATUS_COMMAND_CONFIG_KEY = 'gpipe.sge.status_command'
    STATUS_COMMAND = 'qstat -xml'
    CANCEL_COMMAND_CONFIG_KEY = 'gpipe.sge.cancel_command'
    CANCEL_COMMAND = 'qdel'

    def _get_status(self):
        #
        task_names = set(f'{t.name}.sh' for t in self.workflow.tasks)

        #
        command = self.global_config.get(self.STATUS_COMMAND_CONFIG_KEY, self.STATUS_COMMAND)
        output = subprocess.check_output(shlex.split(command), shell=True)
        xml = lxml.etree.fromstring(output)

        tasks = []
        for job_list in xml.xpath('//job_list'):
            #
            job_name = str(job_list.xpath('./JB_name/text()')[0])
            if job_name not in task_names:
                continue

            #
            job_id = str(job_list.xpath('./JB_job_number/text()')[0])
            job_status = str(job_list.xpath('./state/text()')[0])
            tasks.append((job_id, job_name, self._convert_job_status(job_status)))

        return tasks

    def _convert_job_status(self, value):
        if value.startswith('E'):
            return TaskStatus.ERROR
        elif 'qw' in value:
            return TaskStatus.PENDING
        elif 'r' in value:
            return TaskStatus.RUNNING
        else:
            raise Exception
