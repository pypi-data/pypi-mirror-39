#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='vbox-cli',
    version='0.0.1',
    description='Wrapper for VBoxManage to list, start, stop and attach/detach ISOs',
    url='https://github.com/manuelcarrizo/vbox',
    author='Manuel Carrizo',
    author_email='manuelcarrizo@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vbox=src.vbox:main'
        ]
    }
)