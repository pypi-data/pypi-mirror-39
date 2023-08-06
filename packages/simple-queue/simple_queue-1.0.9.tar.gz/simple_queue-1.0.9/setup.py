# -*- coding: utf-8 -*-
"""
Simple queue setup script;
"""
from setuptools import setup, find_packages
# builds the project dependency list
install_requires = None
with open('requirements.txt', 'r') as f:
        install_requires = f.readlines()

# setup function call
setup(
    name="simple_queue",
    version="1.0.9",
    author="Luis Felipe Muller",
    author_email="luisfmuller@gmail.com",
    description=(
        "A lightweight and ready to use "
        "SQS worker implementation."
    ),
    keywords="queue, AWS, SQS, Worker",
    # Install project dependencies
    install_requires=install_requires,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', "*.json", "*.zip"],
    },
    include_package_data=True,
    packages=find_packages(exclude=["*tests"])
)
