# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    screen.py
   Author :       Zhang Fan
   date：         18/11/30
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import win32con

import win32api
import win32gui

width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


def refresh_size():
    '''
    如果改变了屏幕大小, 请使用这个函数刷新width和height的值
    '''
    global width
    global height
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


def get_dc(handle: int):
    '''
    获取一个控件句柄的绘图设备句柄, 不使用的时候必须使用release_dc释放它
    :param handle: 句柄, 如果设为0则返回桌面的设备句柄
    '''
    return win32gui.GetDC(handle)


def get_window_dc(handle: int):
    '''
    获取的句柄包含窗体标题栏在内, 不使用的时候必须使用release_dc释放它
    :param handle: 句柄, 如果设为0则返回桌面的设备句柄
    '''
    return win32gui.GetWindowDC(handle)


def release_dc(handle: int, hdc: int):
    '''
    释放绘图设备句柄
    :param handle: 控件句柄
    :param hdc: 绘图设备句柄
    '''
    win32gui.ReleaseDC(handle, hdc)


def get_color(hdc: int, x: int, y: int):
    '''
    取色
    :param hdc: 绘图设备句柄(最好使用get_window_dc获取到的dc)
    :param x: 屏幕横向坐标
    :param y: 屏幕纵向坐标
    :return: 如果返回-1则取色失败, 成功返回一个颜色值
    '''
    try:
        return win32gui.GetPixel(hdc, x, y)
    except:
        return -1

#截图
#后台截图
