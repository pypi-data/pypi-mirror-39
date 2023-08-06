"""
Setup script.
"""

import subprocess
from distutils.core import Command # pylint: disable=no-name-in-module,import-error
from setuptools import setup


class Coverage(Command):
    """
    Coverage command setup.
    """

    description = (
        "Run test suite against single instance of"
        "Python and collect coverage data."
    )
    user_options = []

    # pylint: disable=W0107
    def initialize_options(self):
        """
        Initialize command options.
        """
        pass

    # pylint: disable=W0107
    def finalize_options(self):
        """
        Finalize command options.
        """
        pass

    # pylint: disable=R0201
    def run(self):
        """
        Run command.
        """
        import coverage
        import unittest

        cov = coverage.coverage(config_file='.coveragerc')
        cov.erase()
        cov.start()

        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(start_dir='tests')
        unittest.TextTestRunner().run(test_suite)

        cov.stop()
        cov.save()
        cov.report()
        cov.html_report()

class Lint(Command):
    """
    Lint command setup.
    """

    description = (
        "Run lint tools against Python module to enforce check"
        "code quality and style rules."
    )
    user_options = []

    # pylint: disable=W0107
    def initialize_options(self):
        """
        Initialize command options.
        """
        pass

    # pylint: disable=W0107
    def finalize_options(self):
        """
        Finalize command options.
        """
        pass

    # pylint: disable=R0201
    def run(self):
        """
        Run command.
        """
        import pylint.lint

        pylint.lint.Run(['-j', '0', 'setup.py', 'orbital_mechanics'])

setup(
    author='Hutson Betts',
    author_email='hutson@hyper-expanse.net',
    description='orbital-mechanics',
    download_url='',
    cmdclass={
        'coverage': Coverage,
        'lint': Lint,
    },
    install_requires=[
    ],
    license='Apache License (2.0)',
    name='orbital-mechanics',
    packages=[
        'orbital_mechanics',
    ],
    scripts=[],
    test_suite='tests',
    tests_require=[
        'coverage>=4.0.3,<5.0.0',
        'pylint>=2.1.1,<3.0.0',
        'Sphinx>=1.4.1,<2.0.0',
        'tox>=3.5.3,<4.0.0',
    ],
    url='',
    version=(subprocess
             .Popen(['git', 'tag', '--points-at', 'HEAD'], stdout=subprocess.PIPE)
             .stdout.read().rstrip().decode('utf-8').split() or ['0.0.0'])[-1]
)
