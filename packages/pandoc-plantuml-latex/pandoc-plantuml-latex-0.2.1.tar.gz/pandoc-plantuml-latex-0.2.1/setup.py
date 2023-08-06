#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import setup, Command


here = os.path.abspath(os.path.dirname(__file__))

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


required = [
    'pandocfilters'
]


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='pandoc-plantuml-latex',
    version='0.2.1',
    description='Pandoc filter for PlantUML code blocks',
    long_description=open("README.md").read(),
    author='Claus Strasburger',
    author_email='info@ninjaneers.de',
    url='https://github.com/ninjaneers-team/pandoc-plantuml-filter',
    install_requires=required,
    py_modules=['pandoc_plantuml_filter'],
    entry_points={
        'console_scripts': [
            'pandoc-plantuml = pandoc_plantuml_filter:main'
        ]},
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
    cmdclass={
        'upload': UploadCommand,
    },
)
