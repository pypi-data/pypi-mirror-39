# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    regedit.py
   Author :       Zhang Fan
   date：         18/12/03
   Description :  注册表操作
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os
from zassist import regeditlib

from zassist.commonlib.public_const import regedit_primary


class regedit():
    '''
    注册表对象
    '''

    def __init__(self, regedit_type: regedit_primary):
        self._base = regeditlib.regedit(regedit_type.value)
        self._path = None

    @property
    def path(self):
        '''返回当前使用的路径'''
        return self._path

    @path.setter
    def path(self, path):
        '''
        打开并进入一个目录
        :param path: 路径, 如果没有这个路径则自动创建, 如果路径存在则忽略大小写
        '''
        self._path = path
        self._base.open(path)

    def open(self, path: str):
        '''
        打开并进入一个目录
        :param path: 路径, 如果没有这个路径则自动创建, 如果路径存在则忽略大小写
        '''
        self._path = path
        self._base.open(path)

    def get_value(self, name: str, default=None):
        '''
        获取当前路径下某个数据的值
        :param name: 数据名, 忽略大小写
        :param default: 默认值
        :return: 数据值, 失败返回默认值
        '''
        try:
            return self._base.get_value(name)
        except:
            return default

    def set_value(self, name: str, value):
        '''
        创建一个数据或者设置数据的值
        :param name: 数据名, 如果数据名已存在则忽略大小写
        :param value: 数据的值
        '''
        self._base.set_value(name, value)

    def __del__(self):
        self._base.close()


def __is_64bit():
    if 'PROCESSOR_ARCHITECTURE' in os.environ:
        return '64' in os.environ['PROCESSOR_ARCHITECTURE']
    return 'PROGRAMFILES(X86)' in os.environ


def is_auto_run(name: str):
    '''
    某个程序是否开机启动
    :param name: 唯一名称
    :return: 返回True或False
    '''
    return regeditlib.is_auto_run(name, __is_64bit())


def add_auto_run(name: str, file: str, args=None):
    '''
    添加开机启动项
    :param name: 唯一名称(如果已存在则失败)
    :param file: 程序名
    :param args: 参数
    :return: 返回True或False表示成功或失败
    '''
    return regeditlib.add_auto_run(name, file, args, __is_64bit())


def del_auto_run(name: str):
    '''
    删除开机启动项
    :param name: 唯一名称
    :return: 返回True或False表示成功或失败
    '''
    return regeditlib.del_auto_run(name, __is_64bit())
