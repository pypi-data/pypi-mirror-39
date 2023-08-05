from os import path
from setuptools import setup, find_packages


#this should hopefully allow us to have a more pypi friendly, always up to date readme
readMeDir = path.abspath(path.dirname(__file__))
with open(path.join(readMeDir, 'README.rst')) as readFile:
    long_desc = readFile.read()


VERSION = '1.0.2'

setup(
    name='filtration',
    version=VERSION,
    author='Steve McMaster',
    author_email='mcmaster@hurricanelabs.com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/HurricaneLabs/filtration',
    description='A python library for filtering stuff',
    long_description=long_desc,
    install_requires=[
        'pyparsing'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 5 - Production/Stable',
    ],
    bugtrack_url='https://github.com/HurricaneLabs/filtration/issues',
)
