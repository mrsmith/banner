from datetime import datetime
import os
import sys

import subprocess as sp

def git(*args):
    try:
        return sp.check_output('git ' + ' '.join(args), shell=True).strip()
    except sp.CalledProcessError:
        return '<unkonwn>'

def git_state():
    ec = sp.call('git diff HEAD --exit-code',
            shell=True, stdout=open(os.devnull, 'w'))
    return 'clean' if ec == 0 else 'dirty'

def get_cwd():
    git_root = git('rev-parse --show-toplevel')
    cwd = os.getcwd()

    common = os.path.commonprefix((cwd, git_root))
    return cwd[len(common) + len(os.path.sep) :] or '.'

def get_cmd():
    return ' '.join(sys.argv)

def banner(width = 80, indent = 4):
    template = '''\
{_: >{indent}}-- {autogenerated:-^{width}} --
{_: >{indent}}-- {date: <{width}} --
{_: >{indent}}-- {repo: <{width}} --
{_: >{indent}}-- {pwd: <{width}} --
{_: >{indent}}-- {cmd: <{width}} --
{_: >{indent}}-- {git_rev: <{width}} --
{_: >{indent}}-- {_:-^{width}} --\
'''

    return template.format(
        _ = '',
        autogenerated = ' AUTOGENERATED ',
        date    = 'date:    {}'.format(datetime.now().strftime('%Y-%m-%d %X')),
        repo    = 'origin:  {}'.format(git('config --get remote.origin.url')),
        pwd     = 'pwd:     {}'.format(get_cwd()),
        cmd     = 'cmd:     {}'.format(get_cmd()),
        git_rev = 'git-rev: {} ({})'.format(git('rev-parse --short HEAD'), git_state()),
        indent = indent,
        width = width - indent - 6
    )

if __name__ == '__main__':
    print banner()
