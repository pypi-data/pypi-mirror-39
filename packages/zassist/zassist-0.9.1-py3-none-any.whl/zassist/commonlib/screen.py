# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    screen.py
   Author :       Zhang Fan
   date：         18/11/30
   Description :  屏幕扫描
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import win32con

import win32api
import win32gui

from zassist import screenlib

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


def screenshot(x: int = 0, y: int = 0, w: int = 0, h: int = 0):
    '''
    截图
    :param x: x坐标
    :param y: y坐标
    :param w: 截图宽度
    :param h: 截图高度
    :return: png图片的流(可以直接写入文件的bytes)
    '''
    max_w = width - x
    max_h = height - y
    if w == 0 or w > max_w:
        w = max_w
    if h == 0 or h > max_h:
        h = max_h

    buff = screenlib.screenshot(x, y, w, h)
    return bytes(buff)


def screenshot_bg(handle: int, x: int = 0, y: int = 0, w: int = 0, h: int = 0):
    '''
    后台截图
    :param handle: 控件句柄
    :param x: x坐标
    :param y: y坐标
    :param w: 截图宽度
    :param h: 截图高度
    :return: png图片的流(可以直接写入文件的bytes)
    '''
    l, t, r, b = win32gui.GetWindowRect(handle)
    width = r - l
    height = b - t

    max_w = width - x
    max_h = height - y
    if w == 0 or w > max_w:
        w = max_w
    if h == 0 or h > max_h:
        h = max_h

    hdc = win32gui.GetWindowDC(handle)
    buff = screenlib.screenshot_bg(hdc, x, y, w, h)
    win32gui.ReleaseDC(handle, hdc)
    return bytes(buff)
