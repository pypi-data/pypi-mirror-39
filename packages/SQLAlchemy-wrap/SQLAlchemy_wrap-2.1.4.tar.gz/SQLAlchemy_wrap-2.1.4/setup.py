#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2017 by Lev Lazinskiy
:license: MIT, see LICENSE for more details.
"""
import os
import sys
from setuptools import setup
from setuptools.command.install import install
import subprocess

# 要部署, 必须设置当前分支的git tag和VERSION一样.
VERSION = "2.1.4"


# 流程:
# 1. 增加tag: git tag -a [版本号] -m "说明文字"
# 2. 修改VENSION: VERSION = [版本号]
# 3. git提交: git add setup.py && git commit -m "upload pypi"
# 3. 提交tag: git push origin --follow-tags   // origin可修改为你的其它分支

# todo: 待测试
# todo: 写脚本!!!!
def get_git_latest_tag():
    def _minimal_ext_cmd(cmd: str):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd("git describe --abbrev=0 --tags")
        git_tag = out.strip().decode('ascii')
    except OSError:
        git_tag = "Unknown"

    return git_tag


def readme():
    """读取README.md文件"""
    with open('README.md', encoding="utf-8") as f:
        return f.read()


class VerifyVersionCommand(install):
    """确定当前分支的最新tag是否和VERSION变量一致,不一致则报错"""
    description = 'verify that the git tag matches our version'

    def run(self):
        git_latest_tag = get_git_latest_tag()
        if git_latest_tag != VERSION:
            info = "Git tag: {0} does not match the version of this project: {1}".format(git_latest_tag, VERSION)
            sys.exit(info)


setup(
    name="SQLAlchemy_wrap",
    version=VERSION,
    description="Python wrapper for the CircleCI API",
    long_description=readme(),
    author="Jefung",
    author_email="865424525@qq.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords='circleci ci cd api sdk',
    packages=[],
    install_requires=[
        'requests==2.18.4',
    ],
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
