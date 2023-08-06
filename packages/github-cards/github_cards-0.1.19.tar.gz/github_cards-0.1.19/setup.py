#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["Click>=6.0", "Jinja2", "github3.py"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Lars Rinn",
    author_email="lm.rinn@outlook.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Convert your GitHub issues into printable cards for your physical "
    "Scrum/Kanban board.",
    entry_points={"console_scripts": ["github_cards=github_cards.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="github_cards",
    name="github_cards",
    packages=find_packages(include=["github_cards"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/larsrinn/github_cards",
    version="0.1.19",
    zip_safe=False,
)
