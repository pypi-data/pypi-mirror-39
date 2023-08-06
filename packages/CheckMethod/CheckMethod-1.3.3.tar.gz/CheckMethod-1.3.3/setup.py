#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='CheckMethod',
    version='1.03.03',
    description=(
        '飞马主柜台上场文件合规检测'
    ),
    long_description=open('README.rst').read(),
    author='WangZhp',
    author_email='huoyingkk@163.com',
    maintainer='WangZhp',
    maintainer_email='huoyingkk@163.com',
    license='BSD License',
    packages=['CheckMethod', 'Files'],
    platforms=["all"],
    url='http://www.mirrorcffex.cn',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'pandas>=0.22.0',
        'paramiko>=2.4.2',
    ],
)
