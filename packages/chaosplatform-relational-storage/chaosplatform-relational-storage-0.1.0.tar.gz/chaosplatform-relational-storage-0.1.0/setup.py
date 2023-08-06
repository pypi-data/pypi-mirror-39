#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import re
import sys
from os.path import abspath, dirname, join, normpath

from setuptools import find_packages, setup


def get_version_from_package() -> str:
    """
    Read the package version from the source without importing it.
    """
    path = join(dirname(__file__), "chaosplt_relational_storage/__init__.py")
    path = normpath(abspath(path))
    with open(path) as f:
        for line in f:
            if line.startswith("__version__"):
                token, version = line.split(" = ", 1)
                version = version.replace("'", "").strip()
                return version


def read(*names, **kwargs) -> str:
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


needs_pytest = set(['pytest', 'test']).intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
test_require = []
with io.open('requirements-dev.txt') as f:
    test_require = [l.strip() for l in f if not l.startswith('#')]


setup(
    name='chaosplatform-relational-storage',
    version=get_version_from_package(),
    license='Apache Software License 2.0',
    description='A library for relational database access from the Chaos Platform',
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author='ChaosIQ',
    author_email='contact@chaosiq.io',
    url='https://github.com/chaostoolkit/chaoshub-relational-storage',
    packages=find_packages(),
    include_package_data=True,
    tests_require=test_require,
    setup_requires=pytest_runner,
    zip_safe=False,
    python_requires='>=3.6.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ]
)
