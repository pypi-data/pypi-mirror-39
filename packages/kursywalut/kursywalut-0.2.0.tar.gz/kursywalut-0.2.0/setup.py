#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['lxml>=4.2.5', 'requests>=2.21.0', 'six>=1.12.0', ]

setup_requirements = ['setuptools_scm', ]

test_requirements = ['pytest', 'pytest-runner', 'pytest-html', ]

setup(
    author="Bart Grzybicki",
    author_email='bgrzybicki@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Program do wyświetlania i przeliczania aktualnych kursów walut.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kursywalut',
    name='kursywalut',
    packages=find_packages(include=['kursywalut']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bartgee/kursywalut',
    version='0.2.0',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'kursywalut = kursywalut.__main__:main'
        ]
    }
)
