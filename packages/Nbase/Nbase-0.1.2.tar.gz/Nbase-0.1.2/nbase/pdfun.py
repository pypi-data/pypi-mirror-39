#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/9 下午7:59

import pandas as pd


# https://zhuanlan.zhihu.com/p/28531346
def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)


def object_as_category(df_data):
    """
    dataframe object to category
    :param df_data:
    :return:
    """
    for col in df_data.columns:
        if df_data[col].dtype != 'object':
            continue
        num_unique_values = len(df_data[col].unique())
        num_total_values = len(df_data[col])
        if not num_total_values:
            return df_data
        if num_unique_values / num_total_values < 0.5:
            df_data.loc[:, col] = df_data[col].astype('category')
    return df_data


def read_sql(sql, con):
    """
    封装pandas的read_sql，object -> category来优化内存
    :param sql:
    :param con:
    :return:
    """
    df_data = pd.read_sql(sql, con)
    df_data = object_as_category(df_data)
    return df_data
