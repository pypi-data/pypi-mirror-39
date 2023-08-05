#! /usr/bin/env python

"""
Setup information to allow installation with pip.
"""
from setuptools import setup


def version():
    with open("VERSION") as version_file:
        return version_file.read().strip()


def readme():
    """
    Define the README text used by PyPI to build the package homepage.
    """
    # Set to use the text in README.md
    with open("README.md") as readme_file:
        return readme_file.read()


def requirements():
    with open("requirements.txt") as req_file:
        return req_file.read().splitlines()


# Add the package metadata and specify which files to include in the
# distribution. Full list of available classifiers:
# https://pypi.org/pypi?%3Aaction=list_classifiers
setup(
    name="xsec",
    version=version(),
    description="xsec: the cross section evaluation code",
    long_description=readme(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2.7",
        #   'Programming Language :: Python :: 3',
        "Intended Audience :: Science/Research",
    ],
    url="https://github.com/jeriek/xsec",
    maintainer="Jeriek Van den Abeele",
    maintainer_email="jeriekvda@fys.uio.no",
    license="GPLv3+",
    packages=["xsec"],
    #   py_modules=[],
    install_requires=requirements(),
    include_package_data=False,
)
