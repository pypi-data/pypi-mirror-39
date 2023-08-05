#!/usr/bin/env python3

import logging
import os
import sys

import click
import click_log

from clusterone import commands
from clusterone.commands.run.local import local_command
from clusterone import ClusteroneException
from clusterone import __version__
from clusterone import authenticate
from clusterone import client
from clusterone.persistance.session import Session
from clusterone.utilities import log_click_error, UncaughtExceptionHandler
from clusterone.utils import render_table, info

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = os.getcwd()

SENTRY_DSN = "https://d556ac76dafb418b9bde5de7167d7b0f:c274a7b0bbe747adb981d719f1a7226a@sentry.tensorport.com/22"
DEBUG_MODE = os.environ.get("JUST_DEBUG")

# Bunch of global messages
glob_session = Session()
glob_session.__init__()
glob_session.load()

if glob_session.get('username') is None:
    owner_help_message = 'Specify owner by usernames'
else:
    owner_help_message = 'Specify owner by username, default: %s' % glob_session.get(
        'username')

pass_config = click.make_pass_decorator(Session, ensure=True)


class Context(object):
    def __init__(self, client, session, cwd):
        self.client = client
        self.session = session
        self.cwd = cwd


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(context):
    """
    Welcome to the Clusterone Command Line Interface.
    """

    session = Session()
    session.load()
    context.obj = Context(client, session, cwd=HOME_DIR)


def main():
    try:
        cli()
    except ClusteroneException as e:
        log_click_error(e)
        sys.exit(e.exit_code)
    except Exception as e:
        remote_handler = UncaughtExceptionHandler(enable_sentry=False,
                                                  sentry_dsn=SENTRY_DSN,
                                                  release=__version__)
        remote_handler.handle_exception(e)


# ---------------------------------------

@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
def get(context):
    """
    < project(s) | dataset(s) | job(s) | events >
    """
    pass


@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
def create(context):
    """
    < project | dataset | notebook | job >
    """
    pass


@cli.group()
@click.pass_obj
def rm(context):
    """
    < project | dataset | job >
    """
    pass


@create.group(name="job")
@click.pass_obj
def create_job(context):
    """
    < single | distributed >
    """

    pass


@cli.group()
@click.pass_context
def init(context):
    """
    < project | dataset >
    """
    pass


@cli.group()
@click.pass_context
def ln(config):
    """
    < project | dataset >
    """
    pass


@ln.group(name='dataset')
@click.pass_context
def ln_dataset(context):
    """
    < gcs | gitlab>
    """
    pass


@cli.group()
@click.pass_obj
def start(config):
    """
    < job | notebook >
    """
    pass


@cli.group()
@click.pass_context
def stop(config):
    """
    < job | notebook >
    """
    pass


@cli.group()
@click.pass_obj
def run(config):
    """
    < local | job >
    """

    pass


@run.group(name="job")
@click.pass_context
def run_job(context):
    """
    < single | distributed >
    """

    pass


@cli.group()
@click.pass_obj
def download(config):
    """
    < job  >
    """
    pass


get.add_command(commands.get.job.command, 'job')
get.add_command(commands.get.jobs.command, 'jobs')
get.add_command(commands.get.notebooks.command, 'notebooks')
get.add_command(commands.get.events.command, 'events')

create.add_command(commands.create.project.command, 'project')
create.add_command(commands.create.notebook.command, 'notebook')

create_job.add_command(commands.create.job.single.command, 'single')
create_job.add_command(commands.create.job.distributed.command, 'distributed')

rm.add_command(commands.rm.job.command, 'job')
rm.add_command(commands.rm.project.command, 'project')
rm.add_command(commands.rm.dataset.command, 'dataset')

get.add_command(commands.get.project.command, 'project')
get.add_command(commands.get.dataset.command, 'dataset')

init.add_command(commands.init.project.command, 'project')

# ln.add_command(commands.ln.project.command, 'project')

# ln_dataset.add_command(commands.ln.dataset.command, 'gitlab')
# ln_dataset.add_command(commands.ln.dataset.gcs_command, 'gcs')

start.add_command(commands.start.job.command, 'job')
start.add_command(commands.start.notebook.command, 'notebook')

create.add_command(commands.create.dataset.command, 'dataset')

download.add_command(commands.download.job.command, 'job')

stop.add_command(commands.stop.job.command, 'job')
stop.add_command(commands.stop.notebook.command, 'notebook')

cli.add_command(commands.login.command, 'login')
cli.add_command(commands.logout.command, 'logout')

cli.add_command(commands.matrix.command, 'matrix')
cli.add_command(commands.config.command, 'config')

run.add_command(local_command, 'local')

run_job.add_command(commands.run.job.single.command, 'single')
run_job.add_command(commands.run.job.distributed.command, 'distributed')


# ------------------------

@click.command()
@authenticate()
@click.pass_obj
@click.option('--owner')
def get_projects(context, owner=None):
    """
    List projects
    """
    client = context.client
    projects = client.get_projects(owner)

    if projects:
        click.echo(info('All projects:'))

        headers = ['#', 'Project', 'Created at', 'Description']
        data = [headers]

        for idx, project in enumerate(projects):
            try:
                owner_name = project.get('owner')['username']
                project_name = project.get('name')
                project_path = "%s/%s" % (owner_name, project_name)
                creation_date = project.get('created_at')[:19]
                description = project.get('description')
                record = [idx, project_path, creation_date, description]
                data.append(record)
            except Exception as e:
                pass

        table = render_table(data, 36)
        click.echo(table.table)

        return projects
    else:
        click.echo(info("No projects found. Use 'just create project' to start a new one."))
        return None


get.add_command(get_projects, 'projects')


@click.command()
@click.option('--owner')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@click.pass_obj
@authenticate()
def get_datasets(context, owner=None):
    """
    List datasets
    """
    client = context.client
    datasets = client.get_datasets(owner)

    if datasets:
        click.echo(info('All datasets:'))

        header = ['#', 'Dataset', 'Modified at', 'Description']
        data = [header]

        for idx, project in enumerate(datasets):
            try:
                owner_name = project.get('owner')['username']
                dataset_name = project.get('name')
                dataset_path = "%s/%s" % (owner_name, dataset_name)
                modification_date = project.get('modified_at')[:19]
                description = project.get('description')
                record = [idx, dataset_path, modification_date, description]
                data.append(record)
            except Exception as e:
                pass

        table = render_table(data, 36)
        click.echo(table.table)

        return datasets
    else:
        click.echo(
            "It doesn't look like you have any datasets yet. You can create a new one with 'just create dataset'.")
        return None


get.add_command(get_datasets, 'datasets')

if __name__ == '__main__':
    main()
