# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requires = [
    'sqlalchemy',
    'six',
    #'docopt',
    'requests',
    'AppDirs',
    'purl',
]


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='clldclient',
    version="0.1",
    description='A python wrapper for the API exposed by clld apps',
    long_description=read("README.md"),
    author='Robert Forkel',
    author_email='xrotwang@googlemail.com',
    url='https://github.com/clld/clldclient',
    install_requires=requires,
    license=read("LICENSE"),
    zip_safe=False,
    keywords='linguistics',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages(),
    tests_require=['nose', 'coverage', 'mock', 'httmock'],
)
