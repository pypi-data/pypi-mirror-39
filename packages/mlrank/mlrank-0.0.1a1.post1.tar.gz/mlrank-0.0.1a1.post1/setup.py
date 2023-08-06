#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlrank",
    version="0.0.1a1.post1",
    author="Prabakaran Kumaresshan",
    author_email="k_prabakaran@hotmail.com",
    description="Python client to submit output to evaluation server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nixphix/mlrank",
    packages=setuptools.find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'requests >= 2.20.0',
        'pandas >= 0.22.0'
    ],
    python_requires='>=3.5',
    package_data={
        'mlrank': ['tc.dat', 'eda.dat'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
)
