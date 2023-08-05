#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import contextlib
import time

from logzero import logger


@contextlib.contextmanager
def benchmark(name):
    start = time.time()
    yield

    elapsed = time.time() - start
    logger.debug('%s: %.02f sec.', name, elapsed)
