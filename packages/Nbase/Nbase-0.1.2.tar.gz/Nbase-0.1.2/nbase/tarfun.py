#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/9/13 下午3:14

import tarfile


def untar_file(file, dir):
    """
    解压文件
    :param file:
    :param dir:
    :return:
    """
    with tarfile.open(file, 'r:gz') as t:
        t.extractall(path=dir)
        names = t.getnames()
    return names[0] if names else ''
