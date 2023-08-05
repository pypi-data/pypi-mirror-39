#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup_requirements = ["pytest-runner"]
test_requirements = ["pytest"]

setup(
    author="Devon Klompmaker",
    author_email='devon.klompmaker@aofl.com',
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
    description="Unity commands and responses for coeus-python-framework.",
    install_requires=required,
    license="BSD 3-Clause License",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='coeus-test-unity',
    name='coeus-test-unity',
    packages=['coeus_unity'],
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/AgeOfLearning/coeus-unity-python-framework',
    version='0.1.8',
    zip_safe=False,
)