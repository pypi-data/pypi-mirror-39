#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import functools
import os
import pkg_resources

import jinja2


# ================================================================================
# string manipulation
# ================================================================================

def undent(text):
    #
    offset = 0
    for line in text.splitlines():
        if not line.strip():
            continue

        offset = len(line) - len(line.lstrip())
        break

    #
    return '\n'.join([l[offset:] for l in text.splitlines()]).strip()


# ================================================================================
# jinja2
# ================================================================================

@functools.lru_cache(maxsize=None)
def get_jinja2_environment():
    environment = jinja2.Environment()
    environment.filters.update({
        # task
        'collect_dependency_task_names': _collect_dependency_task_names,

        # path
        'dirname': os.path.dirname,
        'basename': os.path.basename,
        'without_extension': lambda p: os.path.splitext(str(p))[0],

        # size
        'MB': lambda v: float(v) / 1000 / 1000,
        'GB': lambda v: float(v) / 1000 / 1000 / 1000
    })

    for loader in pkg_resources.iter_entry_points('gpipe_jinja2_environment_customizer'):
        loader.load()(environment)

    return environment


def _collect_dependency_task_names(tasks):
    result = set()
    for task in tasks:
        for dependency_task in task.dependency_tasks:
            result.add(dependency_task.name)

    return list(sorted(result))
