#
# copyright (c) 2018 east301
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import os

import click

from .benchmark import benchmark
from .loading import WorkflowLoader, load_global_config

from logzero import logger


# ================================================================================
# commands
# ================================================================================

@click.command(help='Runs a workflow')
@click.argument('runfile', type=click.Path(exists=True))
@click.option('-d', '--dry-run', is_flag=True)
@click.option('--delete-already-existing-files', is_flag=True)
@benchmark('Total execution time')
def run(runfile, dry_run, delete_already_existing_files):
    #
    workflow, executor = _create_executor_from_runfile(runfile)
    if dry_run:
        executor.submit(dry_run=True)
        return

    #
    files = workflow.check_and_delete_already_existing_files(delete=delete_already_existing_files)
    if files:
        if delete_already_existing_files:
            logger.error('The following files are deleted before submitting tasks.')
            for path in files:
                logger.error('  * %(path)s', path=path)
        else:
            logger.error('The following existing files are needs to be updated.')
            for path in files:
                logger.error('  * %(path)s', path)

            logger.error('Run gpipe with "--delete-already-exsiting-files" option to run tasks.')
            return

    #
    executor.submit(dry_run=False)


@click.command(help='Shows task status')
@click.argument('runfile', type=click.Path(exists=True))
@benchmark('Total execution time')
def status(runfile):
    _, executor = _create_executor_from_runfile(runfile)
    executor.status()


@click.command(help='Cancels execution of tasks')
@click.argument('runfile', type=click.Path(exists=True))
@click.option('-f', '--force', is_flag=True)
@benchmark('Total execution time')
def cancel(runfile, force):
    _, executor = _create_executor_from_runfile(runfile)
    executor.cancel(force=force)


# ================================================================================
# helpers
# ================================================================================

def _create_workflow_from_funfile(runfile):
    global_config = load_global_config()
    return WorkflowLoader(global_config).load(runfile)


def _create_executor_from_runfile(runfile):
    global_config = load_global_config()
    workflow = WorkflowLoader(global_config).load(os.path.normpath(os.path.abspath(runfile)))
    executor = workflow.runfile.gpipe.executor_class(global_config, workflow)
    return workflow, executor
