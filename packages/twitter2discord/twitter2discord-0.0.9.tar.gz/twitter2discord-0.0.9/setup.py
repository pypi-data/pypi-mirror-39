#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re

from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__), 'twitter2discord', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_readme():
    return get_file(os.path.dirname(__file__), 'README.md')


def install():
    setup(
        name='twitter2discord',
        version=get_version(),
        description='Twitter to Discord Webhook',
        long_description=get_readme(),
        long_description_content_type='text/markdown',
        license='MIT',
        author='poipoii',
        author_email='earth.sama@gmail.com',
        url='https://github.com/poipoii/twitter2discord',
        classifiers=['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Topic :: Software Development :: Libraries',
                     ],
        packages=find_packages(exclude=['docs', 'tests']),
        keywords='twitter discord webhook',
        install_requires=[
            'ggtrans',
            'requests==2.20.0',
            'tweepy==3.7.0',
        ],
        extras_require={},
        tests_require=[
            'tox',
            'flake8',
            'nose',
        ],
        scripts=[]
    )


if __name__ == "__main__":
    install()