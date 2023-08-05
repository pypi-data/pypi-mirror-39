#!/usr/bin/env/ python
from setuptools import setup, find_packages
import os

# retrieve the version
try:
    versionfile = os.path.join('beadalize', '__version__.py')
    f = open(versionfile, 'r')
    content = f.readline()
    splitcontent = content.split('\'')
    version = splitcontent[1]
    f.close()
except:
    raise Exception('Could not determine the version from batchpy/__version__.py')


# run the setup command
setup(
    name='beadalize',
    version=version,
    license='GPLv3',
    description='A package to create ironing bead patterns from images',
    long_description=open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read(),
    url='https://github.com/BrechtBa/beadalize',
    author='Brecht Baeten',
    author_email='brecht.baeten@gmail.com',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    classifiers=['Programming Language :: Python :: 3.6'],
)