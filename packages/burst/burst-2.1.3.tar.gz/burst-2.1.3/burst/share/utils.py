# -*- coding: utf-8 -*-

import functools

from .six import string_types
from .log import logger


def safe_call(func, *args, **kwargs):
    """
    安全调用
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error('exc occur. e: %s, func: %s', e, func, exc_info=True)
        # 调用方可以通过 isinstance(e, BaseException) 来判断是否发生了异常
        return e


def safe_func(func):
    """
    把函数变为安全的
    """
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        return safe_call(func, *args, **kwargs)
    return func_wrapper


def ip_str_to_bin(ip_str):
    """
    转化ip格式，从str转为bin
    支持ipv4/ipv6
    :param ip_str:
    :return: client_ip_num, ipv6
    """
    import socket
    if ':' in ip_str:
        client_ip_num = socket.inet_pton(socket.AF_INET6, ip_str)
        ipv6 = True
    else:
        client_ip_num = socket.inet_pton(socket.AF_INET, ip_str)
        ipv6 = False

    return client_ip_num, ipv6

def import_module_or_string(src):
    """
    按照模块导入或者字符串导入
    :param src:
    :return:
    """
    from .config import import_string
    return import_string(src) if isinstance(src, string_types) else src
