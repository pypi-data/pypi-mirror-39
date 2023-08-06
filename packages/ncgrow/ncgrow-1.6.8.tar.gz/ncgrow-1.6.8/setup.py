import codecs
import os
import re
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='ncgrow',
    version=find_version(".", "ncgrow.py"),
    author = 'Brian Højen-Sørensen',
    author_email = 'brs@fcoo.dk',
    description="tool for extrapolating NetCDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['ncgrow'],
    packages=find_packages(),
    url='https://gitlab.com/FCOO/ncgrow',
    install_requires=[
        'netCDF4',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    license='GPLv3'
)
