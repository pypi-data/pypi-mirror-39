# -*- coding: utf-8 -*-
from setuptools import setup

from gitcepter import VERSION

setup(
    name='gitcepter',
    version='.'.join(str(v) for v in VERSION),
    url='http://appinstall.aiyoumi.com:8282/qinchao/gitcepter.git',
    packages=['gitcepter', 'gitcepter.client', 'gitcepter.server'],
    author='chao',
    author_email='qch5240@163.com',
    license='MIT',
    platforms='POSIX',
    description='Git interceptor to check commits and code style',
    long_description="",
    keywords=(
        'syntax-checker git git-hook python'
    ),
    entry_points={
        'console_scripts': [
            'gitcepter=gitcepter.client.gitcepter:main',
            'gitcepter-server=gitcepter.server.gitcepter:main',
            'gitcepter-install=gitcepter.install:main'
        ],
    },
)