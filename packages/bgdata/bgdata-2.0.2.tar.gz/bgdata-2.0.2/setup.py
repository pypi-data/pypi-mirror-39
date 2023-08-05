import sys
from setuptools import setup, find_packages
from os import path

if sys.hexversion < 0x02070000:
    raise RuntimeError('This package requires Python 2.7 or later.')

requires = ['', ]
if sys.hexversion < 0x03000000:
    requires += ['future']

directory = path.dirname(path.abspath(__file__))
with open(path.join(directory, 'requirements.txt')) as f:
    required = f.read().splitlines()

__version__ = '2.0.2'

setup(
    name="bgdata",
    version=__version__,
    packages=find_packages(),
    author='Barcelona Biomedical Genomics Lab',
    description="Simple data repository managment.",
    license="Apache License 2",
    keywords=["data", "managment", "repository"],
    url="https://bitbucket.org/bgframework/bgdata",
    download_url="https://bitbucket.org/bgframework/bgdata/get/"+__version__+".tar.gz",
    install_requires=required,
    classifiers=[],
    package_data={'': ['*.template', '*.template.spec']},
    entry_points={
        'console_scripts': [
            'bg-data = bgdata.command:cmdline',
            'bgdata = bgdata.command:cmdline'
        ]
    }
)
