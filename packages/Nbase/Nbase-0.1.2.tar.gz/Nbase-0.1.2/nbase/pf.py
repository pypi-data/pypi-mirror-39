#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/4/9 下午12:03

import base64
import hmac
import re
import json
import uuid


def isEmail(mail):
    """
    是否是邮件地址
    :param mail:
    :return:
    """
    if re.search(r'[\w.-]+@[\w.-]+.\w+', mail):
        return True
    else:
        return False


def isString(val):
    """
    是否是字符串
    :param val:
    :return:
    """
    if isinstance(val, str):
        return True
    return False


def isNumberAndAlpha(txt):
    """
    判定字符串是否在 [0-9][a-z]
    :param txt:
    :return:
    """
    if re.match('^[0-9a-z]+$', txt.lower()):
        return True
    else:
        return False


def check_array_str(arrayStr):
    """
    判断字符串是否为list对象
    :param arrayStr:
    :return:
    """
    r = re.compile(r'^\[\s*((\d+)\s*\,??\s*)+?\]$')
    return r.match(arrayStr)


def str2int(value):
    """
    转换为整数
    :param value:
    :return:
    """
    try:
        return int(float(value))
    except Exception as e:
        print(e)
        return 0


def removeHCandHH(txt):
    """
    去掉回车换行符
    :param txt:
    :return:
    """
    txt = txt.replace('\r', '')
    txt = txt.replace('\n', '')
    return txt


def to_json(doc):
    """
    转换成utf-8的json字符串
    :param doc:
    :return:
    """
    return json.dumps(doc, ensure_ascii=False)


def json_to_map(j):
    """
    把json字符串转化为obj
    :param j:
    :return:
    """
    if isinstance(j, str):
        if j:
            return json.loads(j)
        return {}
    return j


def str_sha(vs):
    """
    计算输入字符串的sha后的base64编码
    :param vs:
    :return:
    """
    sec_key = b"mb*we0pgn!z!z9t&ftet%w3npri3fci%mlxiy5*!q94q-3v7tz"
    h = hmac.new(sec_key)
    if isinstance(vs, str):
        h.update(vs)
    else:
        h.update(vs.encode('ascii', 'xmlcharrefreplace'))
    return base64.urlsafe_b64encode(h.digest())


def base64ToFile(fn, cont):
    """
    base64字符串转为二进制文件流,写到tmp目录
    :param cont:
    :return:
    """
    fname = "/tmp/" + fn
    g = open(fname, "w")
    g.write(base64.decodebytes(cont))
    g.close()
    return fname


def fileToBase64(filename):
    """
    二进制文件流转换为base64
    :param cont:
    :return:
    """
    with open(filename, "rb") as bin_file:
        return base64.encodebytes(bin_file.read())


def create_uuid_str():
    return str(uuid.uuid4())


def obj2dict(obj):
    """
    class 属性转化为字典
    :param obj:
    :return:
    """
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


def add_int_to_list_rm_exist(val, lst):
    """
    去重加入list
    :param val:
    :param lst:
    :return:
    """
    if val:
        itmp = str2int(val)
        if itmp not in lst:
            lst.append(itmp)


def add_str_to_list_rm_exist(val, lst):
    """
    去重加入list
    :param val:
    :param lst:
    :return:
    """
    if val:
        stmp = str(val).strip()
        if stmp not in lst:
            lst.append(stmp)


def check_time_conflict(st1, et1, st2, et2):
    """
    检测时间冲突
    :param st1:
    :param et1:
    :param st2:
    :param et2:
    :return:
    """
    # 1.尾部冲突
    if st1 < et2 <= et1:
        return True
    # 2.头部冲突
    if st1 <= st2 < et1:
        return True
    # 3. 2包含1
    if st2 <= st1 and et2 >= et1:
        return True
    return False
