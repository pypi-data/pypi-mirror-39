# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    mouse.py
   Author :       Zhang Fan
   date：         18/11/30
   Description :  鼠标模拟工具
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import time

import win32con
import win32api
import win32gui

from zassist.commonlib import screen
from zassist.commonlib.public_const import mouse_button


def _MAKE_LPARAM(wLow: int, wHigh: int):
    return wHigh * 0x10000 + wLow


def get_pos():
    '''
    获取鼠标位置
    :return: 返回一个元组 (x坐标, y坐标)
    '''
    return win32api.GetCursorPos()


def move(x: int, y: int):
    '''
    鼠标移动
    :param x: x坐标
    :param y: y坐标
    :return:
    '''
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
        x * 65535 // screen.width,
        y * 65535 // screen.height,
        0, 0
    )


def move_relative(r: int, d: int):
    '''
    鼠标相对当前位置移动
    :param r: 向右移动距离
    :param d: 向下移动距离
    '''
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
        (x + r) * 65535 // screen.width,
        (y + d) * 65535 // screen.height,
        0, 0
    )


def press(button: mouse_button):
    '''
    鼠标按下
    :param button: 鼠标按键类型
    '''
    button = button.value
    if button == 1:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    elif button == 2:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    elif button == 3:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)


def uplift(button: mouse_button):
    '''
    鼠标抬起
    :param button: 鼠标按键类型
    '''
    button = button.value
    if button == 1:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif button == 2:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    elif button == 3:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)


def click(button: mouse_button, wait: float = 0.02):
    '''
    鼠标单击
    :param button:  鼠标按键类型
    :param wait: 按下和抬起之间的间隔
    '''
    press(button)
    if wait:
        time.sleep(wait)
    uplift(button)


def click_pos(button: mouse_button, x: int, y: int,
              go_back=True, user_move_valid=True, wait: float = 0.02):
    '''
    鼠标单击屏幕的某个位置
    :param button: 鼠标按键类型
    :param x: x坐标
    :param y: y坐标
    :param go_back: 鼠标单击任务完成后回到之前的位置
    :param user_move_valid: 在执行鼠标单击任务的过程中, 如果用户移动了鼠标, 是否在返回的时候相对移动(这样会让用户感到舒适)
    :param wait: 按下和抬起之间的间隔
    '''
    old_x, old_y = win32api.GetCursorPos()

    move(x, y)
    click(button, wait)

    if not go_back:
        return

    if wait:
        time.sleep(wait)

    if user_move_valid:
        now_x, now_y = win32api.GetCursorPos()
        move(now_x - x + old_x, now_y - y + old_y)
    else:
        move(old_x, old_y)


def click_window(handle: int, button: mouse_button, x: int, y: int,
                 go_back=True, user_move_valid=True, wait: float = 0.02):
    '''
    鼠标单击窗口的某个位置
    :param handle: 窗口句柄
    :param button: 鼠标按键类型
    :param x: x坐标
    :param y: y坐标
    :param go_back: 鼠标单击任务完成后回到之前的位置
    :param user_move_valid: 在执行鼠标单击任务的过程中, 如果用户移动了鼠标, 是否在返回的时候相对移动(这样会让用户感到舒适)
    :param wait: 按下和抬起之间的间隔
    '''
    l, t, r, b = win32gui.GetWindowRect(handle)
    click_pos(button=button, x=l + x, y=y + x,
              go_back=go_back, user_move_valid=user_move_valid, wait=wait)


def press_bg(handle: int, button: mouse_button, x: int = 0, y: int = 0):
    '''
    对某个控件模拟鼠标按下, 不改变实际鼠标状态
    :param handle: 句柄
    :param button: 鼠标按键类型
    :param x: x坐标
    :param y: y坐标
    '''
    button = button.value
    if button == 1:
        win32api.PostMessage(handle, win32con.BM_CLICK, _MAKE_LPARAM(x, y), None)
    elif button == 2:
        win32api.PostMessage(handle, win32con.WM_RBUTTONDOWN, _MAKE_LPARAM(x, y), None)
    elif button == 3:
        win32api.PostMessage(handle, win32con.WM_MBUTTONDOWN, _MAKE_LPARAM(x, y), None)


def uplift_bg(handle: int, button: mouse_button, x: int = 0, y: int = 0):
    '''
    对某个控件模拟鼠标抬起, 不改变实际鼠标状态
    :param handle: 句柄
    :param button: 鼠标按键类型
    :param x: x坐标
    :param y: y坐标
    '''
    button = button.value
    if button == 1:
        win32api.PostMessage(handle, win32con.BM_CLICK, _MAKE_LPARAM(x, y), None)
    elif button == 2:
        win32api.PostMessage(handle, win32con.WM_RBUTTONUP, _MAKE_LPARAM(x, y), None)
    elif button == 3:
        win32api.PostMessage(handle, win32con.WM_MBUTTONUP, _MAKE_LPARAM(x, y), None)


def click_bg(handle: int):
    '''
    对某个控件模拟鼠标单击, 不改变实际鼠标状态
    :param handle: 句柄
    '''
    win32api.PostMessage(handle, win32con.BM_CLICK, None, None)


def lock_rect(x, y, width, height):
    '''
    将鼠标锁定在某个区域, 注意如果切换了窗口会自动取消锁定
    :param x: x坐标
    :param y: y坐标
    :param width: 宽度
    :param height: 高度
    '''
    win32api.ClipCursor((x, y, x + width, y + height))


def unlock_rect():
    '''
    取消鼠标的区域锁定
    '''
    win32api.ClipCursor(0)
