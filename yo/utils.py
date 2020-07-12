import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click

from yo.models.logger import Logger

logger = Logger()


def get_current_jira(location=""):
    """Get a jira from current location, will get from current branch name then first commit message"""
    if location:
        os.chdir(location)

    success, branch_name = run_command('git rev-parse --abbrev-ref HEAD')
    logger.vlog(f'branch name: {branch_name}')
    if not success or "not a git repo" in branch_name:
        return

    jira_id = get_jira_id(branch_name)
    if not jira_id:
        _, last_commit = run_command("git log -1 --pretty=%B")
        return get_jira_id(last_commit)


def get_jira_url(jira_id_str=""):
    """Get a jira url smartly from current location or provided string."""
    jira_home = "https://jira/secure/Dashboard.jspa"
    jira_view = "https://jira/browse/{}"

    if jira_id_str:
        jira_id = get_jira_id(jira_id_str)
    else:
        jira_id = get_current_jira()

    if not jira_id:
        return jira_home
    else:
        return jira_view.format(jira_id)


def get_jira_id(jira_id_str: str):
    """Get jira id from provided string, using regex matching"""
    logger.vlog(f'Get jira id from {jira_id_str}')
    if not jira_id_str:
        return "Yo, nothing?"
    jira_pattern = r'(([A-Z][A-Z\d_]*)-(\d+))'
    m = re.search(jira_pattern, jira_id_str.upper())
    return m.group() if m else None


def get_current_bb(location="", repo_only=True):
    """Get current bitbucket project via git"""
    if location:
        os.chdir(location)

    success, remote_url = run_command("git config --get remote.origin.url")

    if not success or "not a git repo" in remote_url:
        return

    if repo_only:
        return remote_url.split('/')[-2:]
    else:
        return remote_url


def get_bb_url(project_name="", repo_name=""):
    """Get bitbucket url smartly"""
    bb_home = 'https://bitbucket/dashboard'
    bb_view = 'https://bitbucket/projects/{}/repos/{}'

    if not project_name or not repo_name:
        repo = get_current_bb()
        if repo:
            project_name = repo[0] if not project_name else project_name
            repo_name = repo[1][:-5] if not repo_name else repo_name

    if project_name and repo_name:
        return bb_view.format(project_name.upper(), repo_name)
    else:
        return bb_home


def open_url(url: str):
    """
    The ugly way to open a url in Citi.
    :param url:
    :return:
    """
    if "win" not in sys.platform:
        click.launch(url)
        return

    # so far this is my tested way to open a url in Citi
    browsers = [r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Internet Explorer\iexplore.exe",
                r"C:\Program Files\internet explorer\iexplore.exe"
                ]

    browser_exe = [b for b in browsers if os.path.exists(b)]
    if not browser_exe:
        click.echo("Yo, cannot find a browser on your system :(")
        return

    browser_exe = browser_exe[0]
    url_batch = f'@"{browser_exe}" "{url}"\r\n@exit'
    cmd_file = tempfile.mktemp(suffix=".bat")
    Path(cmd_file).write_text(url_batch)
    os.system(f'start /b cmd /c "{cmd_file}"')


def run_command(command, wait=True):
    """
    If wait, will return success flag and output, use it like this:

    is_success,output= run_command(cmd)

    If not wait, will return the output line by line, use it like this:

    for line in run_command(cmd):
      print(line.decode())


    :param command:
    :param wait:
    :return:
    """
    success = True
    output = ''
    try:
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        output_iter = iter(p.stdout.readline, b'')

        if wait:
            for line in output_iter:
                line = line.decode()
                output = f"{output}{line}"

        else:
            return output_iter
    except Exception as e:
        success = False
        output = str(e)

    return success, output


def get_disabled_cli_modules():
    names = []
    if os.environ.get('YO_DEBUG', 'false').lower() == 'false':
        names.append('example')

    return names


def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


def detail_error(exception: Exception):
    return f'{type(exception).__name__}: {exception}'
