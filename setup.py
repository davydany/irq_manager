#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0', 
    'Flask>=1.0',
    'mongoengine>=0.15',
    'pymongo>=3.7',
    'terminaltables>=3.1.0'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="David G. Daniel",
    author_email='davydany@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Views and Manage CPU Affinity for Interrupt Requests",
    entry_points={
        'console_scripts': [
            'irq_manager=irq_manager.cli:irq_manager',
            'irq_client=irq_manager.cli:irq_client',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='irq_manager',
    name='irq_manager',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/davydany/irq_manager',
    version='0.1.0',
    zip_safe=False,
)
