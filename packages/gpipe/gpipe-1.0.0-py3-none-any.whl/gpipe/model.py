#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import collections
import contextlib
import functools
import inspect
import io
import itertools
import os
import subprocess

import humanfriendly
import networkx

from .templating import get_jinja2_environment, undent


# ================================================================================
# path
# ================================================================================

class SourceOutputPath(str):
    def __new__(cls, *args, **kwargs):
        temporary = kwargs.pop('temporary', False)
        instance = str.__new__(cls, *args, **kwargs)
        instance.temporary = temporary
        return instance

    def __add__(self, other):
        return SourceOutputPath(super().__add__(other), temporary=self.temporary)

    @classmethod
    def mask_as_temporary(cls, value):
        if isinstance(value, SourceOutputPath):
            value.temporary = True
        elif isinstance(value, str):
            value = SourceOutputPath(value, temporary=True)
        elif isinstance(value, (tuple, list)):
            value = [cls.mask_as_temporary(v) for v in value]
        else:
            raise Exception

        return value


class SourceOutputPathList(list):
    def __str__(self):
        return ' '.join(self)


# ================================================================================
# task
# ================================================================================

class TaskBuilder(object):
    def __init__(self, runfile, name):
        self._runfile = runfile
        self._name = name
        self._modules = []
        self._cpus = None
        self._memory = None
        self._use_temporary_directory = False
        self._environment = {}
        self._resources = {}
        self._bindings = {}
        self._sources = {}
        self._outputs = {}
        self._script = None
        self._script_caller_file_path = None

    def module(self, module_or_modules):
        if isinstance(module_or_modules, str):
            self._modules.append(module_or_modules)
        elif isinstance(module_or_modules, (tuple, list)):
            self._modules.extend(module_or_modules)
        else:
            raise Exception('Unsupported value type')

    def cpus(self, value):
        self._cpus = value

    def memory(self, value):
        if isinstance(value, str):
            self._memory = humanfriendly.parse_size(value)
        elif isinstance(value, int):
            self._memory = value
        else:
            raise Exception('Unsupported value type')

    def use_temporary_directory(self, value=True, when=None):
        if (when is None) or when:
            self._use_temporary_directory = value

    def env(self, key, value, when=None):
        if (when is None) or when:
            self._environment[key] = value

    def resource(self, key, value, when=None):
        if (when is None) or when:
            self._resources[key] = value

    def bind(self, key, value, when=None):
        if (when is None) or when:
            self._bindings[key] = value

    def source(self, key, value, when=None):
        if (when is None) or when:
            self._sources[key] = self._wrap_path(value)

    def output(self, key, value, when=None):
        if (when is None) or when:
            self._outputs[key] = self._wrap_path(value)

    def _wrap_path(self, target):
        if isinstance(target, SourceOutputPath):
            return SourceOutputPathList([target])
        elif isinstance(target, str):
            return SourceOutputPathList([SourceOutputPath(target)])
        elif isinstance(target, (tuple, list)):
            return SourceOutputPathList([SourceOutputPath(t) for t in target])
        else:
            raise Exception

    def script(self, value):
        self._script = value
        self._script_caller_file_path = os.path.abspath(inspect.stack()[0][1])

    def build(self):
        #
        context = {
            # workflow
            'workflow_directory': os.path.dirname(self._script_caller_file_path),

            # task
            'cpus': self._cpus,
            'memory': self._memory,
        }
        context.update(self._bindings)
        context.update(self._sources)
        context.update(self._outputs)

        env = get_jinja2_environment()
        script = env.from_string(undent(self._script)).render(context)

        #
        return Task(
            self._name,
            self._modules, self._cpus, self._memory, self._use_temporary_directory,
            self._environment, self._resources,
            self._bindings, self._sources, self._outputs,
            script
        )


class Task(object):
    def __init__(
        self, name, cpus, memory, use_temporary_directory, environment, resources,
        bindings, sources, outputs, modules, script
    ):

        self.name = name
        self.cpus = cpus
        self.memory = memory
        self.use_temporary_directory = use_temporary_directory
        self.environment = environment
        self.resources = resources
        self.bindings = bindings
        self.sources = sources
        self.outputs = outputs
        self.modules = modules
        self.script = script

        self.index = None
        self.dependency_tasks = None

    @property
    def dependency_task_names(self):
        if self.dependency_tasks:
            return list(sorted(set(t.name for t in self.dependency_tasks)))
        else:
            return []

    def iterate_sources(self):
        for key, sources in self.sources.items():
            for source in sources:
                yield key, source

    def iterate_outputs(self):
        for key, outputs in self.outputs.items():
            for output in outputs:
                yield key, output

    def create_builder(self, runfile, name):
        builder = TaskBuilder(runfile, name)
        builder._cpus = self.cpus
        builder._memory = self.memory
        builder._use_temporary_directory = self.use_temporary_directory
        builder._environment.update(self.environment)
        builder._resources.update(self.resources)
        builder._bindings.update(self.bindings)
        builder._sources.update(self.sources)
        builder._outputs.update(self.outputs)
        builder._script = self.script
        return builder


# ================================================================================
# workflow
# ================================================================================

class WorkflowBuilder(object):
    def __init__(self, runfile):
        self._runfile = runfile
        self._current_task_builder = None
        self._default_task = None
        self._tasks = []

    @property
    def current_task_builder(self):
        return self._current_task_builder

    @contextlib.contextmanager
    def default(self):
        #
        if self._current_task_builder:
            raise Exception

        #
        self._current_task_builder = TaskBuilder(None)
        yield self._current_task_builder

        self._default_task = self._current_task_builder.build()
        self._current_task_builder = None

    @contextlib.contextmanager
    def task(self, name):
        #
        if self._current_task_builder:
            raise Exception

        #
        if self._runfile.gpipe.task_name_prefix:
            name = self._runfile.gpipe.task_name_prefix + name

        if self._default_task:
            self._current_task_builder = self._default_task.create_builder(self._runfile, name)
        else:
            self._current_task_builder = TaskBuilder(self._runfile, name)

        yield self._current_task_builder

        self._tasks.append(self._current_task_builder.build())
        self._current_task_builder = None

    def output_of(self, task_name, output_key):
        outputs = self.outputs_of(task_name, output_key)
        if len(outputs) != 1:
            raise Exception

        return outputs[0]

    def outputs_of(self, task_name, output_key):
        #
        if self._runfile.gpipe.task_name_prefix:
            task_name = self._runfile.gpipe.task_name_prefix + task_name

        #
        outputs = []
        for task in self._tasks:
            if task.name == task_name:
                for key, path in task.iterate_outputs():
                    if key == output_key:
                        outputs.append(path)

        return outputs

    def build(self):
        return Workflow(self._runfile, self._tasks)


class Workflow(object):
    def __init__(self, runfile, tasks):
        self.runfile = runfile
        self.tasks = tasks
        self.file_dependency_graph = self._build_file_dependency_graph(tasks)
        self.task_dependency_graph = self._build_task_dependency_graph(self.file_dependency_graph)

        self._update_task_properties_inplace(tasks, self.task_dependency_graph)

    @classmethod
    def _build_file_dependency_graph(cls, tasks):
        #
        graph = networkx.DiGraph()
        for task in tasks:
            sources = [s for _, s in task.iterate_sources()]
            if sources:
                for source in sources:
                    for _, output in task.iterate_outputs():
                        graph.add_edge(source, output, task=task)
            else:
                for _, output in task.iterate_outputs():
                    graph.add_edge(None, output, task=task)

        return graph

    @classmethod
    def _build_task_dependency_graph(cls, file_graph):
        task_graph = networkx.DiGraph()
        for edge in file_graph.edges:
            task = file_graph.edges[edge]['task']
            if task_graph.has_node(task.name):
                if task not in task_graph.nodes[task.name]['tasks']:
                    task_graph.nodes[task.name]['tasks'].append(task)
            else:
                task_graph.add_node(task.name, tasks=[task])

        for file1, file2 in file_graph.edges:
            task1 = file_graph.edges[file1, file2]['task']

            for file3 in file_graph.neighbors(file2):
                task2 = file_graph.edges[file2, file3]['task']

                if not task_graph.has_edge(task1.name, task2.name):
                    task_graph.add_edge(task1.name, task2.name)

        return task_graph

    @classmethod
    def _update_task_properties_inplace(cls, tasks, graph):
        # index
        task_name_index_map = collections.defaultdict(int)
        for task in tasks:
            task.index = task_name_index_map[task.name] + 1
            task_name_index_map[task.name] += 1

        # dependency
        for task in tasks:
            task.dependency_tasks = []

        for task1_name, task2_name in graph.edges:
            for task2 in graph.node[task2_name]['tasks']:
                task2.dependency_tasks.extend(graph.node[task1_name]['tasks'])

    def get_task_groups(self):
        #
        self._update_task_state_inplace()

        #
        graph = self.task_dependency_graph
        for task_name in networkx.lexicographical_topological_sort(graph):
            yield graph.nodes[task_name]['tasks']

    @functools.lru_cache(maxsize=None)
    def _update_task_state_inplace(self):
        outdated_files = self.get_outdated_files()
        for task in self.tasks:
            files = itertools.chain(task.iterate_sources(), task.iterate_outputs())
            task.completed = all(f not in outdated_files for _, f in files)

    def get_outdated_files(self):
        #
        file_dependencies = []
        temporay_files = set()
        terminal_files = set()

        graph = self.file_dependency_graph
        reversed_graph = graph.reverse(copy=False)
        for output in reversed_graph.nodes:
            if not output:
                continue

            sources = [s for s in reversed_graph.neighbors(output) if s]
            if (not sources) and (not graph.has_edge(None, output)):
                continue
            else:
                file_dependencies.append((output, sources))

            if output.temporary:
                temporay_files.add(output)
            if graph.out_degree(output) == 0:
                terminal_files.add(output)

        #
        buffer = io.StringIO()
        buffer.write(f'.PHONY: all\n')
        buffer.write(f'.DEFAULT_GOAL: all\n')
        buffer.write(f'all: {" ".join(terminal_files)}\n')
        buffer.write(f'\n')

        if temporay_files:
            buffer.write(f'.SECONDARY:{" ".join(temporay_files)}')
            buffer.write(f'\n')

        for output, sources in file_dependencies:
            buffer.write(f'{output}: {" ".join(sources)}\n')
            buffer.write(f'\t%GP:OUTDATED%\t{output}\n')

        #
        result = subprocess.run(
            [
                'make',
                '--dry-run',
                '--no-builtin-rules',
                '--directory', self.runfile.gpipe.work_directory,
                '--makefile', '-'
            ],
            input=buffer.getvalue().encode('utf-8'),
            stdout=subprocess.PIPE
        )
        if result.returncode != 0:
            raise Exception

        #
        outdated_files = set()
        for line in result.stdout.decode('utf-8').splitlines():
            line = line.strip()
            if line.startswith('%GP:OUTDATED%'):
                outdated_files.add(line.split()[-1])

        return frozenset(outdated_files)

    def check_and_delete_already_existing_files(self, delete=False):
        outdated_files = self.get_outdated_files()

        already_existing_files = set()
        for name in outdated_files:
            path = os.path.join(self.runfile.gpipe.work_directory, name)
            if os.path.exists(path):
                already_existing_files.add(path)

        return already_existing_files
