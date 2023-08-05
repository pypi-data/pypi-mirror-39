from setuptools import setup, find_packages

version = "1.0.1"

long_description = open("README.rst").read()

setup(
    name = "filtration",
    version = version,
    description = "A python library for filtering stuff",
    long_description = long_description,
    url = "https://github.com/HurricaneLabs/filtration",
    author = "Steve McMaster",
    author_email = "mcmaster@hurricanelabs.com",
    package_dir = {"":"src"},
    packages = find_packages("src"),
)
