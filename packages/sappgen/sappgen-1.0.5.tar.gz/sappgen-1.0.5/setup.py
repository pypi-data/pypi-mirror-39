"""Setup script for sappgen"""

import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="sappgen",
    version="1.0.5",
    description="Simple App Generator - Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aayushuppal/sappgen",
    author="Aayush Uppal",
    author_email="aayuppal@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(exclude=("tests")),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={"console_scripts": ["sappgen=sappgen.sappgen:main"]},
)
