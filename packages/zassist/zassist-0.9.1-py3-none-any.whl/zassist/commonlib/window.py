# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    window.py
   Author :       Zhang Fan
   date：         18/11/29
   Description :  窗口以及控件工具
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import win32con
import win32gui
import win32process

from zassist import windowlib
from zassist.commonlib.public_const import msg_icon


def find(title: str = None, class_name: str = None):
    '''
    搜索窗口
    :param title: 窗口的标题
    :param class_name: 窗口的类名
    :return: 成功返回窗口句柄, 失败返回0
    '''
    return win32gui.FindWindowEx(0, 0, class_name, title)


def find_control(parent_handle: int, title: str = None, class_name: str = None):
    '''
    搜索控件
    :param parent_handle: 父句柄(必须是要搜索的控件的直接父句柄)
    :param title: 标题
    :param class_name: 类名
    :return: 成功返回控件句柄, 失败返回0
    '''
    return win32gui.FindWindowEx(parent_handle, 0, class_name, title)


def hide(handle: int):
    '''
    隐藏一个控件
    :param handle: 句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_HIDE)


def show(handle: int):
    '''
    显示控件
    :param handle: 句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)


def enabled(handle: int, enable=True):
    '''
    启用或禁用一个句柄
    :param handle: 句柄
    :param enable: 是否启用(禁用后鼠标无法点击,键盘无法输入,控件显示灰色)
    '''
    win32gui.EnableWindow(handle, 1 if enable else 0)


def is_show(handle: int):
    '''
    判断一个句柄是否显示
    :param handle: 句柄
    '''
    return win32gui.IsWindowVisible(handle)


def is_enabled(handle: int):
    '''
    判断一个句柄是否启用(禁用的句柄控件显示灰色)
    :param handle: 句柄
    '''
    return win32gui.IsWindowEnabled(handle)


def set_min(handle: int):
    '''
    设置窗口最小化
    :param handle: 窗口句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_SHOWMINIMIZED)


def set_max(handle: int):
    '''
    设置窗口最大化
    :param handle: 窗口句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_SHOWMAXIMIZED)


def set_default_size(handle: int):
    '''
    设置窗口为默认大小
    :param handle: 窗口句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)


def set_parent(handle: int, parent: int):
    '''
    将一个控件强制绑定到另一个控件中
    :param handle: 要设置的句柄
    :param parent: 父句柄, 如果设为0则取消绑定
    '''
    win32gui.SetParent(handle, parent)


def get_desktop_handle():
    '''
    获取桌面句柄
    '''
    return win32gui.GetDesktopWindow()


def set_mouse_penetrate(handle: int, through=True):
    '''
    设置鼠标穿透一个窗口
    :param handle: 窗口句柄
    :param through: 是否穿透
    '''
    if through:
        win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(handle,
                                                      win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED)
    else:
        win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) ^ win32con.WS_EX_TRANSPARENT)


def set_color_transparent(handle: int, color_value: int, alpha: float = 1):
    '''
    设置窗口某个颜色完全透明
    :param handle: 窗口句柄
    :param color_value: 颜色值
    :param alpha: 窗口整体透明度0~1
    '''
    assert 0 <= alpha <= 1
    win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(handle, color_value, int(alpha * 255),
                                        win32con.LWA_COLORKEY | win32con.LWA_ALPHA)


def set_transparent(handle: int, alpha: float):
    '''
    设置窗口整体透明
    :param handle: 窗口句柄
    :param alpha: 窗口整体透明度0~1
    '''
    assert 0 <= alpha <= 1
    win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(handle, 0, int(alpha * 255), win32con.LWA_ALPHA)


def set_transparent_cancel(handle: int):
    '''
    取消窗口透明
    :param handle: 窗口句柄
    '''
    win32gui.SetWindowLong(handle, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE) ^ win32con.WS_EX_LAYERED)


def set_z_top(handle: int):
    '''
    设置窗口置顶
    :param handle:窗口句柄
    '''
    win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def set_z_bottom(handle: int):
    '''
    设置窗口置底
    :param handle: 窗口句柄
    '''
    win32gui.SetWindowPos(handle, win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def set_z_cancel(handle: int):
    '''
    取消窗口置顶置底
    :param handle: 窗口句柄
    '''
    win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


def get_front_window():
    '''
    获取当前激活窗口(当前鼠标和键盘操作的窗口)
    '''
    return win32gui.GetForegroundWindow()


def set_front_window(handle: int):
    '''
    将一个控件设为激活窗口(将鼠标和键盘操作转移到这个窗口)
    :param handle: 控件句柄
    '''
    win32gui.SetForegroundWindow(handle)


def get_pid(handle: int):
    '''
    获取窗口的pid标识符
    :param handle: 窗口句柄
    '''
    thread_id, process_id = win32process.GetWindowThreadProcessId(handle)
    return process_id


def get_handle_from_pos(x: int, y: int, only_window=True):
    '''
    根据坐标点获取一个控件句柄
    :param x: 从显示器左上角向右数的像素位置(从0开始)
    :param y: 从显示器左上角向下数的像素位置(从0开始)
    :param only_window: 只获取窗口的句柄
    :return: 如果only_window为False, 将返回实际句柄, 它可能是某个窗口的一个控件, 如按钮, 文本框等
    '''
    handle = win32gui.WindowFromPoint((x, y))
    if only_window:
        return get_top_parent_handle(handle)
    return handle


def get_parent_handle(handle: int):
    '''
    获取一个句柄的父句柄
    :param handle: 句柄
    :return: 如果返回0表示它没有父
    '''
    return win32gui.GetParent(handle)


def get_top_parent_handle(handle: int):
    '''
    获取一个控件句柄的顶级父句柄
    :param handle: 控件句柄
    :return: 顶级父句柄一定是一个窗口
    '''
    handle_buff = top_handle = handle
    while handle_buff > 0:
        top_handle = handle_buff
        handle_buff = get_parent_handle(handle_buff)
    return top_handle


def get_title(handle: int):
    '''
    获取一个句柄的标题
    :param handle: 句柄
    '''
    return win32gui.GetWindowText(handle)


def get_class_name(handle: int):
    '''
    获取一个句柄的类名
    :param handle: 句柄
    '''
    return win32gui.GetClassName(handle)


def is_valid(handle: int):
    '''
    检查这个句柄是否有效
    :param handle: 句柄
    '''
    return win32gui.IsWindow(handle)


def get_rect(handle: int):
    '''
    获取一个句柄的矩形
    :param handle: 句柄
    :return: 返回一个元组 (x坐标, y坐标, 宽度, 高度
    '''
    l, t, r, b = win32gui.GetWindowRect(handle)
    return l, t, r - l, b - t


def active(handle: int):
    '''
    激活一个窗口(显示这个窗口>设置为前台窗口>设置为激活窗口>赋予这个窗口输入焦点)
    :param handle: 窗口句柄
    '''
    win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(handle)
    win32gui.SetActiveWindow(handle)
    win32gui.SetFocus(handle)


def close(handle: int):
    '''
    关闭一个窗口
    :param handle: 窗口句柄
    '''
    win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)


def msg(text: str, title: str = '', icon: msg_icon = msg_icon.none):
    '''
    弹窗(一个确定窗口)
    :param text: 弹窗显示文本
    :param title: 弹窗显示标题
    :param icon: 弹窗显示图标
    '''
    windowlib.msg(text, title, icon.value)


def msg_ok(text: str, title: str = '', icon: msg_icon = msg_icon.none, default_ok=True):
    '''
    弹窗(显示[确定]和[取消]按钮)
    :param text: 弹窗显示文本
    :param title: 弹窗显示标题
    :param icon: 弹窗显示图标
    :param default_ok: 默认选择确定按钮
    :return: 选择了[确定]按钮返回True, 选择了[取消]按钮返回False
    '''
    return windowlib.msg_ok(text, title, icon.value, default_ok)


def msg_yes(text: str, title: str = '', icon: msg_icon = msg_icon.none, default_ok=True):
    '''
    弹窗(显示[是]和[否]按钮)
    :param text: 弹窗显示文本
    :param title: 弹窗显示标题
    :param icon: 弹窗显示图标
    :param default_ok: 默认选择确定按钮
    :return: 选择了[是]按钮返回True, 选择了[否]按钮返回False
    '''
    return windowlib.msg_yes(text, title, icon.value, default_ok)


def msg_retry(text: str, title: str = '', icon: msg_icon = msg_icon.none, default_ok=True):
    '''
    弹窗(显示[重试]和[取消按钮)
    :param text: 弹窗显示文本
    :param title: 弹窗显示标题
    :param icon: 弹窗显示图标
    :param default_ok: 默认选择确定按钮
    :return: 选择了[重试]按钮返回True, 选择了[取消]按钮返回False
    '''
    return windowlib.msg_retry(text, title, icon.value, default_ok)


def msg_input(text: str, title: str = '', default: str = ''):
    '''
    弹出输入框(让用户输入文本)
    :param text: 弹窗显示文本
    :param title: 标题
    :param default: 默认输入文本
    :return: 如果用户点击[确定]按钮则返回用户输入的文本, 如果用户点击[取消]按钮则返回空文本
    '''
    return windowlib.msg_input(text, title, default)


if __name__ == '__main__':
    print(msg_ok('内容', '标题'))
