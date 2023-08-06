# coding: utf-8

from setuptools import setup


setup(
    name="totembionet",
    version = "5",
    author = "Alexandre Clement",
    author_email = "alexandre.clement@etu.unice.fr",
    url = "https://github.com/clement-alexandre/TotemBionet",
    description = "TotemBionet interactive notebook.",
    py_modules = ["totembionet"],
    install_requires = ["docker", "docker-compose"],
    entry_points = {
        "console_scripts": [
            "totembionet = totembionet:main"
        ]
    }
)
