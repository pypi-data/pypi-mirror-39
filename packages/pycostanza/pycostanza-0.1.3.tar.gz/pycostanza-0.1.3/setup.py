#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'scipy>=1.0.0',
                'mahotas>=1.4.4',
                'numpy>=1.9.0',
                'scikit-image>=0.14',
                'networkx>=1.11',
                'matplotlib<3.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Henrik Ahl",
    author_email='hpa22@cam.ac.uk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python version of Costanza",
    entry_points={
        'console_scripts': [
            'pycostanza=pycostanza.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pycostanza',
    name='pycostanza',

    packages=find_packages(include=['pycostanza']),
    setup_requires=setup_requirements,

    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/slcu/teamHJ/henrik_aahl/pycostanza',
    version='0.1.3',
    zip_safe=False,
)
