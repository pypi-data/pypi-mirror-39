#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
import os
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

requirements = [ 'boto3', 'PyYAML', 'botocore']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Martin Schade",
    author_email='amazon-lex-bot-test@amazon.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Test Amazon Lex bots easily by defining business requirements through conversations.",
    install_requires=requirements,
    scripts=['bin/lex-bot-test'],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='amazon_lex_bot_test',
    name='amazon_lex_bot_test',
    packages=find_packages(include=['amazon_lex_bot_test']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aws-samples/amazon_lex_bot_test',
    version='0.1.1',
    zip_safe=False,
)
