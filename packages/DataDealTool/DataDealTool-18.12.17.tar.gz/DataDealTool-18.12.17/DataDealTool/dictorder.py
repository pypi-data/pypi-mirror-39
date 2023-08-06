#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   dictorder.py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-12-17
Description:
    the file for ordering dictionary.
"""
import collections
import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)


def sorted_dict(data, key=None, reverse=False):
    """
    :param data: the type of data is dict
    :param key: this is a function for sorting
    :param reverse: whether reverse
    :return: return a dict by ordered
    """
    order_dict = collections.OrderedDict()
    l = sorted(data.items(), key=key, reverse=reverse)
    for one in l:
        k = one[0]
        v = one[1]
        order_dict[k] = v
    return order_dict
