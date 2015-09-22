# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requires = [
    'sqlalchemy',
    'six',
    'beautifulsoup4>=4.4.0',
    'requests',
    'AppDirs',
    'purl',
    'rdflib',
    'uritemplate',
    'html5lib',
]

setup(
    name='clldclient',
    version="1.3.0",
    description='A python wrapper for the API exposed by clld apps',
    author='Robert Forkel',
    author_email='xrotwang@googlemail.com',
    url='https://github.com/clld/clldclient',
    install_requires=requires,
    license='Apache 2',
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
    entry_points="""\
        [console_scripts]
        clld-download-table = clldclient.cli:download_table
    """)
