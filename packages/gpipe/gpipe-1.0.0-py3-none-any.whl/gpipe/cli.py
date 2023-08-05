#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import logging
import pkg_resources

import click
import logzero

from . import commands


def main():
    #
    @click.group()
    @click.option('--debug', is_flag=True, envvar='GPIPE_DEBUG')
    def run_click(debug):
        logzero.loglevel(logging.DEBUG if debug else logging.INFO)
        logzero.formatter(logzero.LogFormatter(
            fmt='%(asctime)s %(color)s[%(levelname).1s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))

    #
    run_click.add_command(commands.run)
    run_click.add_command(commands.status)
    run_click.add_command(commands.cancel)

    for loader in pkg_resources.iter_entry_points('gpipe_commands'):
        run_click.add_command(loader.load())

    #
    run_click()
