# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    network.py
   Author :       Zhang Fan
   date：         18/12/03
   Description :  常用网络功能
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import re
import datetime
import json

import requests

from zassist import networklib


def ping(ip: str, timeout: float = 0.3):
    '''
    ping某个地址
    :param ip: ip地址
    :param timeout: 超时时间, 超时标记为失败
    :return: 返回是否成功
    '''
    return networklib.ping(ip, timeout)


def get_html_response(url, method='get', timeout=10, retry=3, **kwargs):
    '''
    获取网页数据
    :param url: 网址
    :param method: 请求方式
    :param retry: 重试次数
    :param kwargs: 其他参数
    :return: 成功返回Response对象, 失败返回None
    '''
    try:
        return getattr(requests, method)(url, timeout=timeout, **kwargs)
    except:
        if retry > 0:
            print({'msg': '无法获取到数据,还剩 %d 次重试次数' % retry, 'url': url})
            return get_html_response(url, method, retry - 1, **kwargs)
        else:
            print({'msg': '多次重试仍然无法获取到数据', 'url': url})


def get_html_text(url, method='get', encoding=None, timeout=10, retry=3, **kwargs):
    '''
    获取网页数据
    :param url: 网址
    :param method: 请求方式
    :param encoding: 文本解密方式
    :param timeout: 超时时间
    :param retry: 重试次数
    :param kwargs: 其他参数
    :return: 成功返回网页源码, 失败返回空文本
    '''
    res = get_html_response(url, method=method, timeout=timeout, retry=retry, **kwargs)
    if not res:
        return ''

    try:
        if encoding:
            res.encoding = encoding
        return res.text
    except:
        return ''


def get_network_ip():
    '''
    获取外网ip
    :return: 成功返回ip地址, 失败返回空文本
    '''
    base_url = 'http://www.ip138.com/ips138.asp'
    text = get_html_text(base_url, method='get', encoding='gbk')
    try:
        return re.search('您的IP地址是：\[(\d+\.\d+\.\d+\.\d+)\]', text).group(1)
    except:
        return ''


def get_network_time():
    '''
    获取网络时间
    :return: 成功返回datetime对象, 失败返回None
    '''
    base_url = 'http://api.k780.com:88/?app=life.time&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'
    text = get_html_text(base_url, method='get', encoding='utf8')
    if not text:
        return

    try:
        j = json.loads(text)
        return datetime.datetime.fromtimestamp(int(j['result']['timestamp']))
    except:
        pass


if __name__ == '__main__':
    print(type(get_network_time()))
