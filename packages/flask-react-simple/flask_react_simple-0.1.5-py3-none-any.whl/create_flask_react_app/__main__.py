#!/usr/bin/env python
# encoding=utf-8

import os, sys
import click
import shutil
import subprocess

import flask_reactjs


def _ignore(src, names):
    names = [
        n for n in names if '__pycache__' in src or '__pycache__' in n
    ]
    return names


@click.command()
@click.argument('project_name')
@click.option('-N', '--no-install')
def create(project_name, no_install):
    cwd = os.getcwd()

    dirpath = os.path.join(cwd, project_name)

    if os.path.exists(dirpath):
        print(f'{dirpath} already exists!')
        return

    pkgdir = sys.modules['create_flask_react_app'].__path__[0]

    shutil.copytree(pkgdir, dirpath, ignore=_ignore)

    if not no_install:
        subprocess.call("yarn install", shell=True, cwd=dirpath)


if __name__ == '__main__':
    create()
