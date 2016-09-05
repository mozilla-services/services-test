#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

REQUIREMENTS = [
    'fabric',
    'twilio',
    'pexpect',
    'setuptools',
    'six',
    'docopt',
    'requests==2.7.0',
    'requests-hawk',
    'PyBrowserID'
]

setup(
    name='msisdn-gateway-e2e-test',
    version='0.0.1',
    description='msisdn-gateway-e2e-test',
    long_description="",
    author='Koki Yoshida',
    author_email='kreamkorokke@gmail.com',
    url='https://github.com/services-test/msisdn-gateway',
    license="MIT",
    install_requires=REQUIREMENTS,
    keywords=['msisdn-gateway', 'e2e-test'],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'msisdn-cli = msisdn_cli:main',
        ]
    }

)
