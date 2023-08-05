# -*- coding: utf-8 -*-


import os
from setuptools import setup

import riga


this_dir = os.path.dirname(os.path.abspath(__file__))

keywords = []

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
]

# read the readme file
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()

# load installation requirements
with open(os.path.join(this_dir, "requirements.txt"), "r") as f:
    install_requires = [line.strip() for line in f.readlines() if line.strip()]

setup(
    name=riga.__name__,
    version=riga.__version__,
    author=riga.__author__,
    author_email=riga.__email__,
    description=riga.__doc__.strip(),
    license=riga.__license__,
    url=riga.__contact__,
    keywords=keywords,
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=2.7",
    zip_safe=False,
    py_modules=[riga.__name__],
    data_files=[(".", ["LICENSE", "requirements.txt", "README.md"])],
)
