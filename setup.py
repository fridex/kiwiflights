#!/usr/bin/env python3

from setuptools import setup


def get_requirements():
    with open('requirements.txt') as fd:
        return fd.read().splitlines()

setup(
    name='kiwiflights',
    version='0.1.0rc1',
    packages=['kiwiflights'],
    scripts=['kiwiflights-cli'],
    install_requires=get_requirements(),
    author='Fridolin Pokorny',
    author_email='fridex.devel@gmail.com',
    maintainer='Fridolin Pokorny',
    maintainer_email='fridex.devel@gmail.com',
    description='kiwi week homework solution',
    url='https://github.com/fridex/kiwiflights',
    license='GPL',
    keywords='kiwi flights',
)
