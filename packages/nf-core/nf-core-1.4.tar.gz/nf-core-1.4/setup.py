#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

version = '1.4'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = 'nf-core',
    version = version,
    description = 'Helper tools for use with nf-core Nextflow pipelines.',
    long_description = readme,
    long_description_content_type='text/markdown',
    keywords = ['nf-core', 'nextflow', 'bioinformatics', 'workflow', 'pipeline', 'biology', 'sequencing', 'NGS', 'next generation sequencing'],
    author = 'Phil Ewels',
    author_email = 'phil.ewels@scilifelab.se',
    url = 'https://github.com/nf-core/tools',
    license = license,
    scripts = ['scripts/nf-core'],
    install_requires = [
        'cookiecutter',
        'click',
        'GitPython',
        'pyyaml',
        'requests',
        'requests_cache',
        'tabulate'
    ],
    setup_requires=[
        'twine>=1.11.0',
        'setuptools>=38.6.',
    ] + ([] if sys.version_info.minor == 4 else ['wheel>=0.31.0']),
    packages = find_packages(exclude=('docs')),
    include_package_data = True,
    zip_safe = False
)
