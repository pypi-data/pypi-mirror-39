# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    util.py
   Author :       Zhang Fan
   date：         18/11/29
   Description :  屏幕工具
-------------------------------------------------
"""
__author__ = 'Zhang Fan'


def color_from_rgb(r: int, g: int, b: int):
    '''
    返回一个颜色值
    :param r: 红色0~255
    :param g: 绿色0~255
    :param b: 蓝色0~255
    '''
    return b * 65536 + g * 256 + r # - 16777216


def rgb_from_color(color_value: int):
    '''
    解析颜色的rgb
    :param color_value: 颜色值
    :return: 返回一个元组 (红色, 绿色, 蓝色)
    '''
    return color_value & 0x0000ff, (color_value & 0x00ff00) >> 8, (color_value & 0xff0000) >> 16
