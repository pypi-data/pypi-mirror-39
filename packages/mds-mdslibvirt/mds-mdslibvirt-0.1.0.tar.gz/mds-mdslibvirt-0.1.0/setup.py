""" get access to libvirtd using Python
""" 

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))
MODULE = 'mdslibvirt'
PREFIX = 'mds'

def read(fname):
    return open(path.join(here, fname), 'r', 'utf-8').read()

def get_version():
    init = read(path.join(MODULE, '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", init).group(1)

# Get the long description from the README file
long_description = read('README.rst')
    
requires = []

setup(name='mds-mdslibvirt',
    version=get_version(),
    description='get access to libvirtd using Python',
    long_description=long_description,
    author='martin-data services',
    author_email='service@m-ds.de',
    url='https://www.m-ds.de/',
    install_requires=requires,
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='GPL-3',
    keywords='libvirt qemu kvm python',
)
