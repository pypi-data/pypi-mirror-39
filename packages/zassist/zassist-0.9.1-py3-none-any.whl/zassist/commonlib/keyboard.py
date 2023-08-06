# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    keyboard.py
   Author :       Zhang Fan
   date：         2018/12/1 0001
   Description :  键盘模拟工具
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import time

import win32api

from zassist.commonlib.public_const import keyboard_button


def get_state(button: keyboard_button):
    '''
    获取按键状态
    :param button: 按键类型
    :return:
    '''
    state = win32api.GetAsyncKeyState(button.value)
    return not (state == 0 or state == 1)


def press(button: keyboard_button):
    '''
    按下某个按键
    :param button: 按键类型
    '''
    win32api.keybd_event(button.value, win32api.MapVirtualKey(button.value, 0), 0, 0)


def uplift(button: keyboard_button):
    '''
    抬起某个按键
    :param button: 按键类型
    '''
    win32api.keybd_event(button.value, win32api.MapVirtualKey(button.value, 0), 2, 0)


def click(button: keyboard_button, wait: float = 0.02):
    '''
    按下并抬起某个按键
    :param button: 按键类型
    :param wait: 按下和抬起之间的间隔
    '''
    press(button)
    if wait:
        time.sleep(wait)
    uplift(button)


def shear():
    '''
    按下ctrl+x剪切
    '''
    press(keyboard_button.VK_CTRL)
    press(keyboard_button.VK_X)
    uplift(keyboard_button.VK_X)
    uplift(keyboard_button.VK_CTRL)


def copy():
    '''
    按下ctrl+c复制
    '''
    press(keyboard_button.VK_CTRL)
    press(keyboard_button.VK_C)
    uplift(keyboard_button.VK_C)
    uplift(keyboard_button.VK_CTRL)


def paste():
    '''
    按下ctrl+v粘贴
    '''
    press(keyboard_button.VK_CTRL)
    press(keyboard_button.VK_V)
    uplift(keyboard_button.VK_V)
    uplift(keyboard_button.VK_CTRL)


def repair_except():
    '''
    如果使用了拦截键盘按键, 在关闭进程后可能会造成按键异常, 使用这个函数可以修复按键异常
    '''
    for code in range(255):
        win32api.keybd_event(code, win32api.MapVirtualKey(code, 0), 2, 0)
