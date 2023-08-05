import os

import click

from onepanel.commands.datasets import datasets_clone, datasets_download, DatasetViewController, general_push
from onepanel.commands.jobs import jobs_download_output
from onepanel.commands.login import login_required
from onepanel.commands.projects import projects_clone, ProjectViewController
from onepanel.gitwrapper import GitWrapper


def get_entity_type(path):
    dirs = path.split('/')
    entity_type = None
    if len(dirs) == 3:
        account_uid, dir, uid = dirs
        if dir == 'projects':
            entity_type = 'project'
        elif dir == 'datasets':
            entity_type = 'dataset'
    elif len(dirs) == 5:
        account_uid, parent, project_uid, dir, uid = dirs
        if parent == 'projects' and dir == 'jobs':
            entity_type = 'job'
    return entity_type

@click.command('clone', help='Clone project or dataset from server.')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '-i', '--include',
    type=str,
    help='Regex pattern to include lfs objects'
)
@click.option(
    '-x', '--exclude',
    type=str,
    help='Regex pattern to exclude lfs objects (Default to * for projects)'
)
@click.pass_context
@login_required
def clone(ctx, path, directory, include, exclude):
    entity_type = get_entity_type(path)
    if entity_type == 'project':
        projects_clone(ctx, path, directory, include, exclude)
    elif entity_type == 'dataset':
        datasets_clone(ctx, path, directory, include, exclude)
    else:
        click.echo('Invalid project or dataset path.')

@click.command('download', help='Download a dataset')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '--archive',
    type=bool,
    is_flag=True,
    default=False,
    help='Download the output as a compressed file.'
)
@click.pass_context
@login_required
def download(ctx, path, directory,archive):
    entity_type = get_entity_type(path)
    if entity_type == 'dataset':
        datasets_download(ctx, path, directory)
    elif entity_type == 'job':
        jobs_download_output(ctx, path, directory,archive)
    else:
        click.echo('Invalid path.')

@click.command('push', help='Push changes to onepanel')
@click.pass_context
@login_required
def push(ctx):
    home = os.getcwd()
    # Figure out if we are dealing with a project or dataset
    if os.path.isfile(ProjectViewController.PROJECT_FILE):
        GitWrapper().push(home)
    elif os.path.isfile(DatasetViewController.DATASET_FILE):
        general_push(ctx)
    else:
        click.echo("Cannot determine if you are trying to push a dataset or project. Are you in the right directory?")

@click.command('pull', help='Pull changes from onepanel (fetch and merge)')
@click.pass_context
@login_required
def pull(ctx):
    home = os.getcwd()
    GitWrapper().pull(home)
