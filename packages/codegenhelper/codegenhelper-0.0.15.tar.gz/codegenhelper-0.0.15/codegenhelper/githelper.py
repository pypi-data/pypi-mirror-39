from .log import log
import os
import subprocess

def get_tag(giturl, tag, location = os.getcwd(), ssh_key = None):
    def tag_cmd():
        return '-b "%s"' % tag

    def key_cmd():
        return "" if ssh_key == None else \
            'GIT_SSH_COMMAND="ssh -i %s"'% os.path.abspath(ssh_key)

    def git_cmd():
        return "git clone --single-branch --depth 1 %s" % giturl

    subprocess.call(log(__name__)("git cmd").debug(" ".join([key_cmd(), git_cmd(), tag_cmd()])), shell=True, cwd=location)
    
