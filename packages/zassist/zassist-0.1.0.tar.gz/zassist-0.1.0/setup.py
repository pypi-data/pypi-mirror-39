#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zassist',
    version='0.1.0',
    py_modules=[],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='制作游戏辅助常用模块, 本次发布并没有任何功能, 只是为了占名字',
    long_description=open('README.md', 'r', encoding='utf8').read(),  # 项目介绍
    long_description_content_type='text/markdown',
    url='https://pypi.org/',
    license='GNU GENERAL PUBLIC LICENSE',
    platforms=['all'],
    scripts=[],  # 额外的文件
    install_requires=['pywin32'],  # 依赖库
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)
