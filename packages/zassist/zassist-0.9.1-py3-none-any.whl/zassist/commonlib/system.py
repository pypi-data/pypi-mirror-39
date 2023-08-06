# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    system.py
   Author :       Zhang Fan
   date：         18/12/03
   Description :  操作系统常用功能
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os

import psutil

import win32api
import win32gui
import win32con
import win32clipboard

from zassist import systemlib


def lock_screen():
    '''
    系统锁屏
    '''
    systemlib.lock_screen()


def shutdown():
    '''
    关机
    '''
    win32api.ExitWindowsEx(1, 0)


def restart():
    '''
    重启
    '''
    win32api.ExitWindowsEx(2, 0)


def login_out():
    '''
    注销
    '''
    win32api.ExitWindowsEx(0, 0)


def set_volume_hige():
    '''
    提高音量
    '''
    win32api.SendMessage(win32gui.GetForegroundWindow(), 0x319, 0x30292, 0x0a0000)


def set_volume_low():
    '''
    降低音量
    '''
    win32api.SendMessage(win32gui.GetForegroundWindow(), 0x319, 0x30292, 0x090000)


def set_volume_mute():
    '''
    静音
    '''
    win32api.SendMessage(win32gui.GetForegroundWindow(), 0x319, 0x30292, 0x080000)


def set_clipboard(text: str):
    '''
    设置剪切板数据
    :param text: 要设置的文本
    '''
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()


def kill_by_pid(pid: int):
    '''
    杀死一个进程
    :param pid: 进程标识符
    :return: 返回是否成功
    '''
    try:
        handle = win32api.OpenProcess(0x0001, 0, pid)
        win32api.TerminateProcess(handle, 0)
        return True
    except:
        return False


def kill_by_name(name: str, maxcount: int = 0):
    '''
    杀死一个进程
    :param name: 进程名(注意大小写)
    :param maxcount: 如果有同名进程, 最多杀死多少个数量, 如果设为0则全部杀死
    '''
    kill_count = 0
    for proc in psutil.process_iter():
        if name == proc.name():
            kill_by_pid(proc.pid)
            kill_count += 1

            if maxcount and kill_count >= maxcount:
                return


def is_64bit():
    '''
    判断操作系统是否为64位
    :return: 是返回True, 不是返回False
    '''
    if 'PROCESSOR_ARCHITECTURE' in os.environ:
        return '64' in os.environ['PROCESSOR_ARCHITECTURE']
    return 'PROGRAMFILES(X86)' in os.environ


def get_local_pid():
    '''
    获取当前进程pid
    '''
    return win32api.GetCurrentProcessId()


def get_pid_path(pid: int):
    '''
    获取进程路径
    :param pid: 进程pid
    '''
    proc = psutil.Process(pid)
    return proc.exe()


def get_local_path():
    '''
    获取当前进程路径
    '''
    pid = win32api.GetCurrentProcessId()
    proc = psutil.Process(pid)
    return proc.exe()


def get_disktop_path():
    '''
    获取桌面图片路径
    '''
    return win32gui.SystemParametersInfo(0x0073)


def get_last_error():
    '''
    获取系统记录的上一次报错代码
    '''
    return win32api.GetLastError()


def get_error_describe(errcode: int):
    '''
    获取错误描述
    :param errcode: 错误代码
    '''
    return win32api.FormatMessage(errcode)


def raise_access_authority():
    '''
    提高进程权限
    :return: 返回True或False表示成功或失败
    '''
    return systemlib.raise_access_authority()


# def run_file(file: str, args: str = None, wait_exit: None or bool or float = None):
#     '''
#     运行一个文件
#     :param file: 文件路径(如果不是可执行文件exe则调用默认应用程序打开这个文件)
#     :param args: 参数
#     :param wait_exit: 是否等待这个程序退出, 如果为None或False则不等待.如果为True或0则等待直到进程退出.如果为其他数字则表示等待多少秒.
#     :return: 成功返回进程pid, 失败返回0
#     '''
#     if wait_exit is None or wait_exit is False:
#         wait_exit = -1
#     elif wait_exit is True:
#         wait_exit = 0
#     print(wait_exit)
#     return systemlib.run_file(file, args or '', wait_exit)


def create_user_process(file: str, args: str = None, wait_exit: None or bool or float = None):
    '''
    创建windows session ui层级的进程
    :param file: 文件路径(只能是可执行程序)
    :param args: 参数
    :param wait_exit: 是否等待这个程序退出, 如果为None或False则不等待.如果为True或0则等待直到进程退出.如果为其他数字则表示等待多少秒.
    :return: 成功返回进程pid, 失败返回0
    '''
    if wait_exit is None or wait_exit is False:
        wait_exit = -1
    elif wait_exit is True:
        wait_exit = 0

    return systemlib.create_user_process(file, args or '', wait_exit)


def create_process(file: str, args: str = None, wait_exit: None or bool or float = None):
    '''
    创建一个进程
    :param file: 文件路径(如果不是可执行文件exe则调用默认应用程序打开这个文件)
    :param args: 参数
    :param wait_exit: 是否等待这个程序退出, 如果为None或False则不等待.如果为True或0则等待直到进程退出.如果为其他数字则表示等待多少秒.
    :return: 成功返回进程pid, 失败返回0
    '''
    if wait_exit is None or wait_exit is False:
        wait_exit = -1
    elif wait_exit is True:
        wait_exit = 0

    return systemlib.create_process(file, args or '', wait_exit)


def allow_system_lock(enable: bool):
    '''
    是否允许系统锁屏
    :param enable: 是否允许
    '''
    systemlib.allow_system_lock(enable)


def get_allow_system_lock():
    '''
    获取是否允许系统锁屏
    :return: 是否允许
    '''
    return systemlib.get_allow_system_lock()


def run_cmd(command: str, work_path='c:/', wait_exit: None or bool or float = None):
    '''
    运行cmd命令
    :param command: 参数
    :param work_path: 工作目录
    :param wait_exit: 是否等待这个程序退出, 如果为None或False则不等待.如果为True或0则等待直到进程退出.如果为其他数字则表示等待多少秒.
    '''
    if wait_exit is None or wait_exit is False:
        wait_exit = -1
    elif wait_exit is True:
        wait_exit = 0

    systemlib.run_cmd(command, work_path, wait_exit)

if __name__ == '__main__':
    run_cmd('regedit', wait_exit=True)
