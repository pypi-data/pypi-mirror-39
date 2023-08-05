# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    public_const.py
   Author :       Zhang Fan
   date：         2018/12/1 0001
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from enum import Enum


class mouse_button(Enum):
    left = 1
    right = 2
    middle = 3


class keyboard_button(Enum):
    VK_LBUTTON = 1  # 鼠标的左键
    VK_RBUTTON = 2  # 鼠标的右键
    VK_CANCEL = 3  # Ctrl+Break(通常不需要处理)
    VK_MBUTTON = 4  # 鼠标中键
    VK_BACK = 8  # Backspace键
    VK_TAB = 9
    VK_CLEAR = 12  # Clear键（Num Lock关闭时的数字键盘5）
    VK_RETURN = 13  # Enter
    VK_SHIFT = 16
    VK_CONTROL = 17  # Ctrl键
    VK_MENU = 18  # Alt键
    VK_PAUSE = 19
    VK_CAPITAL = 20  # Caps Lock键
    VK_ESCAPE = 27
    VK_SPACE = 32
    VK_PRIOR = 33  # Page Up键
    VK_NEXT = 34  # Page Domw键
    VK_END = 35
    VK_HOME = 36
    VK_LEFT = 37
    VK_UP = 38
    VK_RIGHT = 39
    VK_DOWN = 40
    VK_Select = 41
    VK_PRINT = 42
    VK_EXECUTE = 43
    VK_SNAPSHOT = 44  # Print Screen键（抓屏）
    VK_Insert = 45
    VK_Delete = 46
    VK_HELP = 47
    VK_0 = 48
    VK_1 = 49
    VK_2 = 50
    VK_3 = 51
    VK_4 = 52
    VK_5 = 53
    VK_6 = 54
    VK_7 = 55
    VK_8 = 56
    VK_9 = 57
    VK_A = 65
    VK_B = 66
    VK_C = 67
    VK_D = 68
    VK_E = 69
    VK_F = 70
    VK_G = 71
    VK_H = 72
    VK_I = 73
    VK_J = 74
    VK_K = 75
    VK_L = 76
    VK_M = 77
    VK_N = 78
    VK_O = 79
    VK_P = 80
    VK_Q = 81
    VK_R = 82
    VK_S = 83
    VK_T = 84
    VK_U = 85
    VK_V = 86
    VK_W = 87
    VK_X = 88
    VK_Y = 89
    VK_Z = 90
    VK_NUMPAD0 = 96
    VK_NUMPAD1 = 97
    VK_NUMPAD2 = 98
    VK_NUMPAD3 = 99
    VK_NUMPAD4 = 100
    VK_NUMPAD5 = 101
    VK_NUMPAD6 = 102
    VK_NUMPAD7 = 103
    VK_NUMPAD8 = 104
    VK_NUMPAD9 = 105
    VK_MULTIPLY = 106  # 数字键盘上的*键
    VK_ADD = 107  # 数字键盘上的+键
    VK_SEPARATOR = 108
    VK_SUBTRACT = 109  # 数字键盘上的-键
    VK_DECIMAL = 110  # 数字键盘上的.键
    VK_DIVIDE = 111  # 数字键盘上的/键
    VK_F1 = 112
    VK_F2 = 113
    VK_F3 = 114
    VK_F4 = 115
    VK_F5 = 116
    VK_F6 = 117
    VK_F7 = 118
    VK_F8 = 119
    VK_F9 = 120
    VK_F10 = 121
    VK_F11 = 122
    VK_F12 = 123
    VK_NUMLOCK = 144  # Num Lock 键
    VK_SCROLL = 145  # Scroll Lock键
