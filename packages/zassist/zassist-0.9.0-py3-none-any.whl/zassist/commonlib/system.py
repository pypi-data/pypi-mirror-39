# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    system.py
   Author :       Zhang Fan
   date：         18/12/03
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os

import psutil

import win32api
import win32gui
import win32con
import win32clipboard


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
    return  win32api.GetLastError()

def get_error_describe(errcode:int):
    '''
    获取错误描述
    :param errcode: 错误代码
    '''
    return win32api.FormatMessage(errcode)

# 提升进程权限
# 系统锁屏
# 打开一个文件
# 创建用户进程
# 创建进程
# 禁止系统锁屏
# 运行cmd命令

# 获取cpu序列号
# 获取硬盘序列号


if __name__ == '__main__':
    print(get_error_describe(400))
