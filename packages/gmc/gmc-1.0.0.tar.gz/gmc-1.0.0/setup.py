from setuptools import setup, find_packages
import os
import re
import ast

def long_description():
    BASE_PATH = os.path.dirname(__file__)
    with open(os.path.join(BASE_PATH, "README.md"), encoding='utf-8') as fh:
        return fh.read()

def get_requirements():
    BASE_PATH = os.path.join(os.path.dirname(__file__), 'requirements')
    with open(os.path.join(BASE_PATH, 'base.txt')) as f:
        rv = f.read().splitlines()
        return rv

def get_version(file):
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    with open(file, 'rb') as f:
        version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
        return version


setup(
    name="gmc",
    version=get_version('gmc/__init__.py'),
    author="Kirk Erickson",
    author_email="ekirk0+gitlab@gmail.com",
    description="GMC Geiger counter api",
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url="https://gitlab.com/slippers/gmc",
    install_requires=get_requirements(),
    tests_require=['pytest'],
    test_suite='gmc/test',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
