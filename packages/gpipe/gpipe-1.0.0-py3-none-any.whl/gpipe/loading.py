#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import datetime
import os
from logzero import logger

from .benchmark import benchmark
from .model import SourceOutputPath, WorkflowBuilder
from .module import load_python_module_from_file, load_python_object_by_path
from .objects import Namespace, ObjectProxy, Tree
from .path import get_absolute_path


# ================================================================================
# config
# ================================================================================

def load_config_python_module(path, customizer=None):
    #
    def inject_items(module):
        module.Tree = Tree
        module.gpipe = Tree()

        if customizer:
            customizer(module)

    #
    module = load_python_module_from_file(path, inject_items)

    items = {}
    for key in dir(module):
        #
        if key.startswith('_'):
            continue

        #
        value = getattr(module, key)
        if isinstance(value, Tree):
            value = value.freeze()

        items[key] = value

    return Namespace(**items)


def load_global_config():
    path = os.path.expanduser('~/.gpipe.config.py')
    if os.path.exists(path):
        logger.info('Global configuration file found: %s', path)
        with benchmark('Loading of global configuration file'):
            return load_config_python_module(path)

    else:
        return Namespace()


# ================================================================================
# workflow
# ================================================================================

class WorkflowLoader(object):
    def __init__(self, global_config):
        self.global_config = global_config
        self._workflow_builder_stack = []

    def load(self, path):
        with benchmark('Loading of runfile'):
            runfile = self._load_runfile(path)
        with benchmark('Loading of Workflow'):
            return self._load_workflow(runfile.gpipe.workflow, runfile)

    def _load_runfile(self, path):
        #
        runfile = load_config_python_module(path, self._create_runfile_item_injector(path))
        gpipe = runfile.gpipe
        if not gpipe.get('workflow'):
            raise Exception

        #
        gpipe.workflow = get_absolute_path(gpipe.workflow, relative_to=path)
        gpipe.work_directory = get_absolute_path(gpipe.get('work_directory', '.'), relative_to=path)
        gpipe.executor_class = load_python_object_by_path(
            gpipe.get('executor_class')
            or self.global_config.get('gpipe.executor_class')   # NOQA: W503
            or 'gpipe.execution:SGEWorkflowExecutor'            # NOQA: W503
        )
        gpipe.task_name_prefix = gpipe.get('task_name_prefix') or ''

        gpipe.log_directory = os.path.join(
            gpipe.work_directory,
            'logs',
            datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        )

        #
        logger.info('Runfile loaded:')
        logger.info('  * Workflow:       %s', gpipe.workflow)
        logger.info('  * Work directory: %s', gpipe.work_directory)
        logger.info('  * Log directory:  %s', gpipe.log_directory)
        logger.info('  * Executor:       %s', str(gpipe.executor_class).split("'")[1])
        logger.info('  * Task prefix:    %s', gpipe.task_name_prefix)

        return runfile

    def _load_workflow(self, path, runfile):
        builder = WorkflowBuilder(runfile)

        self._workflow_builder_stack.insert(0, builder)
        load_python_module_from_file(path, self._create_workflow_item_injector(path, runfile))
        self._workflow_builder_stack.pop(0)

        return builder.build()

    def _create_runfile_item_injector(self, root):
        def require(path, relative_to=None):
            return load_python_module_from_file(
                get_absolute_path(path, relative_to=(relative_to or path)),
                self._create_runfile_item_injector(path)
            )

        def to_absolute_path(path, relative_to=None):
            return get_absolute_path(path, relative_to=(relative_to or path))

        def inject(module):
            module.Tree = Tree
            module.require = require
            module.to_absolute_path = to_absolute_path
            module.options = Tree()

        return inject

    def _create_workflow_item_injector(self, root, runfile):
        def require(path, relative_to=None):
            return load_python_module_from_file(
                get_absolute_path(path, relative_to=(relative_to or path)),
                self._create_workflow_item_injector(path, runfile)
            )

        def dirname(path):
            return os.path.dirname(os.path.normpath(os.path.abspath(path)))

        def inject(module):
            s = self._workflow_builder_stack
            wbp = lambda n: ObjectProxy(lambda: getattr(s[0], n))   # NOQA:E731
            tbp = lambda n: ObjectProxy(lambda: getattr(s[0].current_task_builder, n))  # NOQA:E731

            functions = {
                #
                'gpipe': runfile.gpipe,
                'options': runfile.options,

                #
                'default': wbp('default'),
                'task': wbp('task'),

                'output_of': wbp('output_of'),
                'outputs_of': wbp('outputs_of'),

                'cpus': tbp('cpus'),
                'memory': tbp('memory'),
                'use_temporary_directory': tbp('use_temporary_directory'),
                'env': tbp('env'),
                'resource': tbp('resource'),
                'bind': tbp('bind'),
                'source': tbp('source'),
                'output': tbp('output'),
                'module': tbp('module'),
                'script': tbp('script'),

                #
                'require': require,
                'dirname': dirname,
                'temporary': SourceOutputPath.mask_as_temporary
            }

            for key, function in functions.items():
                setattr(module, key, function)

        return inject
