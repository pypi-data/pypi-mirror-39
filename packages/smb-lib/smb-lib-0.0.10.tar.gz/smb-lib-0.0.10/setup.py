# -*- coding: utf8 -*-

from setuptools import setup, find_packages

setup(name="smb-lib",
    version='0.0.10',
    author = "Mohamed Chennouf",
    author_email = "mohamed.chennouf@etu.unice.fr",
    url = "https://github.com/clement-alexandre/TotemBionet",
    description = "smbionet librairie python",
    long_description = open("README.rst").read(),
    install_requires = ["py4j"],
    license="WTFPL",
    include_package_data = True,
    packages = find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords="jupyter, computational systems biology",
)