# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from r53ddns import __version__, __description__

requires = [
    'boto3==1.9.66'
]

setup(
    name='r53ddns',
    description='Route 53 Dynamic DNS Update Client',
    long_description=__description__,
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
