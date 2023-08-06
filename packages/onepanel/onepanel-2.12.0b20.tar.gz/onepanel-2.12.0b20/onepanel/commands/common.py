import os
import subprocess
import sys

import click

from onepanel.commands import jobs
from onepanel.commands.datasets import datasets_clone, datasets_download, DatasetViewController, general_push
from onepanel.commands.jobs import jobs_download_output, JobViewController
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
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.pass_context
@login_required
def clone(ctx, path, directory,quiet):
    entity_type = get_entity_type(path)
    if entity_type == 'project':
        projects_clone(ctx, path, directory)
    elif entity_type == 'dataset':
        datasets_clone(ctx, path, directory,quiet)
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
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b','--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.pass_context
@login_required
def download(ctx, path, directory,archive,quiet,background):
    entity_type = get_entity_type(path)
    if entity_type == 'dataset':
        datasets_download(ctx, path, directory,quiet,background)
    elif entity_type == 'job':
        jobs_download_output(ctx, path, directory,archive)
    else:
        click.echo('Invalid path.')

@click.command('push', help='Push changes to onepanel')
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Datasets only: Add a message to this version. Up to 255 chars.\"text\".'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Datasets only: Add a name to this version. Use \"text\".'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b','--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.pass_context
@login_required
def push(ctx, message, name,quiet,background):
    home = os.getcwd()
    # Are we uploading job output? A project? Or Dataset?
    if os.path.isfile(JobViewController.JOB_OUTPUT_FILE):
        jobs.upload_output(ctx,quiet)
    elif os.path.isfile(ProjectViewController.PROJECT_FILE):
        if message is not None or name is not None:
            click.echo(
                "Projects do not support these arguments. Remove arguments and try again.")
            return
        GitWrapper().push(home)
    elif os.path.isfile(DatasetViewController.DATASET_FILE):
        if background:
            close_fds = False
            cmd_list = ['onepanel','dataset-background-push']
            if message is not None:
                cmd_list.append('--message')
                cmd_list.append('\"'+message+'\"')
            if name is not None:
                cmd_list.append('--name')
                cmd_list.append('\"'+name+'\"')
            if quiet:
                cmd_list.append('-q')
            if background:
                cmd_list.append('-b')
            if sys.platform != 'win32':
                cmd_list.insert(0, 'nice')
                cmd_list.insert(0, 'nohup')
                close_fds = True
            else:
                # /i so that windows doesn't create "%SYSTEM_DRIVE%" folder
                cmd_list.insert(0, 'start /b /i')
            cmd = ' '.join(cmd_list)
            if sys.platform != 'win32':
                subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True, close_fds=close_fds,preexec_fn=os.setpgrp)
            else:
                # Windows specific instructions
                # https://docs.microsoft.com/en-us/windows/desktop/ProcThread/process-creation-flags
                CREATE_NO_WINDOW = 0x08000000
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True, close_fds=close_fds,
                                 creationflags=CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP)

            click.echo("Starting upload in the background.")
        else:
            general_push(ctx, message, name,quiet,background)
    else:
        click.echo("Cannot determine if you are trying to push job output, dataset files, or project files. Are you in the right directory?")

@click.command('dataset-background-push', help='This is to be called by a python sub-process.',hidden=True)
@click.option(
    '-m', '--message',
    type=str,
    default=None,
    help='Datasets only: Add a message to this version. Up to 255 chars.\"text\".'
)
@click.option(
    '-n', '--name',
    type=str,
    default=None,
    help='Datasets only: Add a name to this version. Use \"text\".'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Minimize chatter from executed commands.'
)
@click.option(
    '-b','--background',
    is_flag=True,
    help='Run the download in the background. Will work even if SSH session is terminated.'
)
@click.pass_context
@login_required
def background_dataset_push(ctx,message,name,quiet,background):
    general_push(ctx, message, name, quiet, background)

@click.command('pull', help='Pull changes from onepanel (fetch and merge)')
@click.pass_context
@login_required
def pull(ctx):
    home = os.getcwd()
    GitWrapper().pull(home)
