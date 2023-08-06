# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    password.py
   Author :       Zhang Fan
   date：         2018/12/1
   Description :  密码工具
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import time
import random
import hashlib

from zassist import passwordlib


def _hash(text, way):
    way = getattr(hashlib, way)()
    way.update(text.encode('utf8'))
    return way.hexdigest()


def md5(text):
    return _hash(text, 'md5')


def md5_32(text):
    return md5(text)


def md5_16(text):
    return _hash(text, 'md5')[8:24]


def sha1(text):
    return _hash(text, 'sha1')


def sha224(text):
    return _hash(text, 'sha224')


def sha256(text):
    return _hash(text, 'sha256')


def sha384(text):
    return _hash(text, 'sha384')


def sha512(text):
    return _hash(text, 'sha512')


def blake2b(text):
    return _hash(text, 'blake2b')


def blake2s(text):
    return _hash(text, 'blake2s')


# 随机密码
def rand_pwd(length: int = 16, lower_letter=True, upper_letter=True, space=False, special=False):
    '''
    随机生成指定长度的密码
    :param length: 密码长度
    :param lower_letter: 是否允许小写字母
    :param upper_letter: 是否允许大写字母
    :param space: 是否允许空格
    :param special: 是否允许特殊符号
    '''
    text_num = '0123456789'
    text_lower = 'abcdefghijklmnopqrstuvwxyz'
    text_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text_space = ' '
    text_special = '~!@#$%^&*()+-=_./\\|;:<>,?[]{}\'"'
    text = ''.join([
        text_num,
        text_lower if lower_letter else '',
        text_upper if upper_letter else '',
        text_space if space else '',
        text_special if special else '',
    ])

    return ''.join(random.choices(text, k=length))


def _generate_dynamic_pwd(time_stamp: int, secret_key: str, precision: int = 30, iter_count=353):
    '''
    生成一个密码
    :param time_stamp: 时间戳
    :param secret_key: 密钥
    :param precision: 时间精度, 多少秒变化一次
    :param iter_count: md5计算迭代次数
    :return: 返回一个4位数的数字字符串
    '''
    hex_map = dict(a=10, b=11, c=12, d=13, e=14, f=15)
    for i in range(10):
        hex_map[str(i)] = i

    pwd_base = md5(str(time_stamp // precision) + secret_key)
    pwd_md5 = pwd_base
    for i in range(iter_count):
        pwd_md5 = md5(pwd_md5)

    buff = bytearray(16)
    for i in range(16):
        index = i * 2
        a = pwd_md5[index]
        b = pwd_md5[index + 1]
        buff[i] = hex_map[a] + hex_map[b] * 16

    result_list = []
    for i in range(4):
        index = i * 4
        num = buff[index] + buff[index + 1] + buff[index + 2] + buff[index + 3]
        result_list.append(str(num % 10))
    return ''.join(result_list)


def create_dynamic_pwd(secret_key: str, *, precision=30, iter_count=353):
    '''
    创建一个动态密码
    :param secret_key: 密钥
    :param precision: 时间精度, 多少秒变化一次
    :param iter_count: md5计算迭代次数
    :return: 返回一个4位数的数字字符串
    '''
    return _generate_dynamic_pwd(time_stamp=int(time.time()),
                                 secret_key=secret_key, precision=precision, iter_count=iter_count)


def check_dynamic_pwd(pwd: str, secret_key: str, pardon_level=1, *, precision=30, iter_count=353):
    '''
    检查动态密码
    :param pwd: 密码
    :param secret_key: 密钥
    :param pardon_level: 宽恕级别, 密码错误时, 检查当前时间前后产生多少次的密码
    :param precision: 时间精度
    :param iter_count: md5计算迭代次数
    :return: 成功返回True, 失败返回False
    '''
    time_stamp = int(time.time())
    src_pwd = _generate_dynamic_pwd(time_stamp=time_stamp,
                                    secret_key=secret_key, precision=precision, iter_count=iter_count)
    if pwd == src_pwd:
        return True

    for stamp in range(time_stamp - pardon_level * precision, time_stamp + pardon_level * precision + 1, precision):
        src_pwd = _generate_dynamic_pwd(time_stamp=stamp,
                                        secret_key=secret_key, precision=precision, iter_count=iter_count)
        print(src_pwd)
        if pwd == src_pwd:
            return True

    return False


def aes_encipher(text: str, secret_key: str):
    '''
    aes加密
    :param text: 要加密的文本
    :param secret_key: 密钥
    :return: 加密后的文本
    '''
    return passwordlib.aes_encipher(text, md5(secret_key))


def aes_decipher(text: str, secret_key: str):
    '''
    aes解密
    :param text: 要解密的文本
    :param secret_key: 密钥
    :return: 解密后的文本, 失败返回空文本
    '''
    return passwordlib.aes_decipher(text, md5(secret_key))


if __name__ == '__main__':
    src_text = '一二三四五六七八九十一二三四五六七八九十'
    secret_key = '密钥'

    en_text = aes_encipher(src_text, secret_key)
    de_text = aes_decipher(en_text, secret_key)
    print(src_text)
    print(en_text)
    print(de_text)
