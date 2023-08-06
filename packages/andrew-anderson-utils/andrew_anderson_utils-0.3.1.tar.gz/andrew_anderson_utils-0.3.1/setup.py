#!/usr/bin/python3

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='andrew_anderson_utils',
    version='0.3.1',
    author='Andrew Anderson',
    author_email='andrew-anderson.neo@yandex.ru',
    description='A package with Andrew Anderson\'s modules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mr-Andersen/andrew_anderson_utils',
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    install_requires=['pycrypto', 'requests']
)
