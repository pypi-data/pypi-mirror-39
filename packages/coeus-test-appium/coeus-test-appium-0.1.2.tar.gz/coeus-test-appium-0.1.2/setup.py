#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

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
    description="Appium bindings for the coeus-pythong-framework.",
    install_requires=required,
    license="BSD 3-Clause License",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='coeus-test-appium',
    name='coeus-test-appium',
    packages=['coeus_appium'],
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/AgeOfLearning/coeus-appium-bindings',
    version='0.1.2',
    zip_safe=False,
)