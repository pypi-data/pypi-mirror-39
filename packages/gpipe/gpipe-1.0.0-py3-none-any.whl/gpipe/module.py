#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import contextlib
import importlib
import importlib.util
import sys
import uuid


@contextlib.contextmanager
def supress_pyc():
    orig_flag = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    yield
    sys.dont_write_bytecode = orig_flag


@supress_pyc()
def load_python_object_by_path(path):
    module_path, object_name = path.split(':')
    return getattr(importlib.import_module(module_path), object_name)


@supress_pyc()
def load_python_module_from_file(path, customize_module=None):
    spec = importlib.util.spec_from_file_location(f'gpipe.user.m{uuid.uuid4().hex[:8]}', path)
    module = importlib.util.module_from_spec(spec)
    if customize_module:
        customize_module(module)

    spec.loader.exec_module(module)
    return module
