# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    __init__.py.py
   Author :       Zhang Fan
   date：         18/11/29
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os

import clr


def __get_assistlib():
    base_path = os.path.abspath(os.path.dirname(__file__))
    dll_file = os.path.abspath(os.path.join(os.path.join(base_path, 'dll'), 'assistlib.dll'))
    assert os.path.isfile(dll_file), '文件<{}>不存在'.format(dll_file)
    clr.AddReference(dll_file)
    return __import__('assistlib')

assistlib = __get_assistlib()
networklib = assistlib.networklib
passwordlib = assistlib.passwordlib
regeditlib = assistlib.regeditlib
screenlib = assistlib.screenlib
systemlib = assistlib.systemlib
windowlib = assistlib.windowlib

if __name__ == '__main__':
    print(windowlib.msg_retry('123','aaa'))

