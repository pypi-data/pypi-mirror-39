#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='vbox-cli',
    version='0.0.2',
    description='Wrapper for VBoxManage to list, start and stop VMs. Also can attach/detach ISOs',
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