#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import os


def get_absolute_path(path, relative_to=None):
    if relative_to and (not os.path.isabs(path)):
        path = os.path.join(os.path.dirname(relative_to), path)

    return os.path.normpath(os.path.abspath(path))
