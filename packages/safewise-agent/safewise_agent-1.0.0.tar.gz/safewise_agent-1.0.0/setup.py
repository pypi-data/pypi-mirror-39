#!/usr/bin/env python
from setuptools import setup

setup(
    name='safewise_agent',
    version='1.0.0',
    description='Using SafeWISE as hardware SSH/GPG agent',
    author='CoinWISE',
    author_email='safewise@coinwise.io',
    url='http://github.com/coinwise-io/safewise-agent',
    scripts=['safewise_agent.py'],
    install_requires=[
        'safewiseagentlib>=1.0.0',
        'safewise[hidapi]>=1.0.0'
    ],
    platforms=['POSIX'],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Utilities',
    ],
    entry_points={'console_scripts': [
        'safewise-agent = safewise_agent:ssh_agent',
        'safewise-gpg = safewise_agent:gpg_tool',
        'safewise-gpg-agent = safewise_agent:gpg_agent',
    ]},
)
