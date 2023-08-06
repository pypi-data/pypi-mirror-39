# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from r53ddns import __version__, __description__

requires = [
    'boto3==1.9.66'
]


def join_relpath(file):
    return os.path.join(os.path.dirname(__file__), file)


with open(join_relpath('README.rst'), 'r') as fd:
    long_description = fd.read().strip()


setup(
    name='r53ddns',
    description='Route 53 Dynamic DNS Update Client',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    install_requires=requires,
    version=__version__,
    entry_points={
        'console_scripts': ['r53ddns=r53ddns.r53ddns:run']
    },
    author='Zachery Brady',
    author_email='bradyzp@dynamicgravitysytems.com',
    url='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
    ]
)
