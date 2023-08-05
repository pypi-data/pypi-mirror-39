#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/7 下午4:09

import datetime
import time
import pytz

TZONE = 'Asia/Shanghai'
DT_STYLE = '%Y-%m-%d %H:%M:%S'

utc_0 = int(time.mktime(datetime.datetime(1970, 1, 1).timetuple()))


def str_to_datetime(str_date, style=DT_STYLE, tzstr=TZONE):
    """
    style:格式字符串是python的标准日期格式码，例如：
        %Y-%m-%d %H:%M:%S
        %Y-%m-%d
    """
    dt = datetime.datetime.strptime(str_date, style)
    dt = pytz.timezone(tzstr).localize(dt)
    return dt


def get_datetime_str(dt, style="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(style)


def get_now_datetime_str(style="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(style)


def get_last_day_str(dt_str, style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.strptime(dt_str, style)
    dt_last = dt - datetime.timedelta(days=1)
    return dt_last.strftime(style)


def get_next_day_str(dt_str, style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.strptime(dt_str, style)
    dt_next = dt + datetime.timedelta(days=1)
    return dt_next.strftime(style)


def get_last_sunday_str(style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.today()
    idx = dt.weekday() + 1
    dt_last = dt - datetime.timedelta(days=idx)
    return dt_last.strftime(style)


def get_yesterday_str(style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    dt -= datetime.timedelta(days=1)
    return get_datetime_str(dt, style=style)


def get_today_yesterday_str(style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    dt_yest = dt - datetime.timedelta(days=1)
    dt_str = get_datetime_str(dt, style=style)
    dt_yest_str = get_datetime_str(dt_yest, style=style)
    return dt_yest_str, dt_str


def get_today_yesterday_0_str(style="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    dt_yest = dt - datetime.timedelta(days=1)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_yest = dt_yest.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_str = get_datetime_str(dt, style=style)
    dt_yest_str = get_datetime_str(dt_yest, style=style)
    return dt_yest_str, dt_str


def get_start_end_date_dict(date_time, style="%Y-%m-%d"):
    """
    获取start_date, end_date字典
    :param date_time:
    :param style:
    :return:
    """
    start_dt = datetime.datetime.strptime(date_time, style)
    end_dt = start_dt + datetime.timedelta(days=1)
    start_date = start_dt.strftime(DT_STYLE)
    end_date = end_dt.strftime(DT_STYLE)
    start_date_s = date_str2s(start_date)
    end_date_s = date_str2s(end_date)
    utc_start_date = get_utc_time_str_from_s(start_date_s)
    utc_end_date = get_utc_time_str_from_s(end_date_s)
    return {
        'date_time': date_time,
        'start_date': start_date,
        'end_date': end_date,
        'utc_start_date': utc_start_date,
        'utc_end_date': utc_end_date,
        'start_date_s': start_date_s,
        'end_date_s': end_date_s,
        'start_date_ms': start_date_s * 1000,
        'end_date_ms': end_date_s * 1000
    }


def get_latest_days_dict(date_time, days=1, style='%Y-%m-%d'):
    """
    获取近7天的日期dict
    :param date_time:
    :param days:
    :param style:
    :return:
    """
    start_dt = datetime.datetime.strptime(date_time, style)
    end_dt = start_dt + datetime.timedelta(days=1)
    start_dt = end_dt - datetime.timedelta(days=days)
    start_date = start_dt.strftime(DT_STYLE)
    end_date = end_dt.strftime(DT_STYLE)
    start_date_s = date_str2s(start_date)
    end_date_s = date_str2s(end_date)
    utc_start_date = get_utc_time_str_from_s(start_date_s)
    utc_end_date = get_utc_time_str_from_s(end_date_s)
    return {
        'date_time': date_time,
        'start_date': start_date,
        'end_date': end_date,
        'utc_start_date': utc_start_date,
        'utc_end_date': utc_end_date,
        'start_date_s': start_date_s,
        'end_date_s': end_date_s,
        'start_date_ms': start_date_s * 1000,
        'end_date_ms': end_date_s * 1000
    }


def get_last_hour_dt_str(style='%Y-%m-%d %H:%M:%S'):
    """
    获取上一个小时的datetime str
    :return:
    """
    dt_now = datetime.datetime.now()
    dt_last_h = dt_now - datetime.timedelta(hours=1)
    return dt_last_h.strftime(style)


def get_utc_millis():
    """
    获取系统从1970-1-1至今的utc毫秒数
    :return:
    """
    return datetime_to_utc_ms(datetime.datetime.utcnow())


def get_utc_s():
    """
    获取系统从1970-1-1至今的utc秒数
    :return:
    """
    return int(datetime_to_utc_ms(datetime.datetime.utcnow()) / 1000)


def get_unix_curdate():
    """
    获取今天的0点的时间戳
    :return:
    """
    return int(time.mktime(datetime.date.today().timetuple())) * 1000


def date_str2ms(date_str, style='%Y-%m-%d %H:%M:%S'):
    """
    日期str转utc时间戳
    :param date_str:
    :param style:
    :return:
    """
    dt = str_to_datetime(date_str, style=style)
    return datetime_to_utc_ms(dt)


def date_str2s(date_str, style='%Y-%m-%d %H:%M:%S'):
    """
    日期str转utc时间戳
    :param date_str:
    :param style:
    :return:
    """
    dt = str_to_datetime(date_str, style=style)
    return datetime_to_utc_s(dt)


def datetime_to_utc_ms(dt):
    """
    转化为utc的毫秒数
    :param dt:
    :return:
    """
    return int((time.mktime(dt.utctimetuple()) - utc_0) * 1000) + int(dt.microsecond / 1000)


def datetime_to_utc_s(dt):
    """
    转化为utc的秒数
    :param dt:
    :return:
    """
    return int(time.mktime(dt.utctimetuple()) - utc_0)


def get_utc_time_from_ms(ms):
    """
    获取国际标准时
    :param ms:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(int(ms) / 1000)


def get_utc_time_str_from_ms(ms, style='%Y-%m-%d %H:%M:%S'):
    """
    获取国际标准时
    :param ms:
    :param style:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(int(ms) / 1000).strftime(style)


def get_utc_time_from_s(s):
    """
    获取国际标准时
    :param s:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(s)


def get_utc_time_str_from_s(s, style='%Y-%m-%d %H:%M:%S'):
    """
    获取国际标准时
    :param s:
    :param style:
    :return:
    """
    return datetime.datetime.utcfromtimestamp(s).strftime(style)


def get_china_time_from_ms(ms):
    """
    获取中国时间
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000.0, pytz.timezone(TZONE))


def get_china_time_from_s(s):
    """
    获取中国时间
    :param s:
    :return:
    """
    return datetime.datetime.fromtimestamp(s, pytz.timezone(TZONE))


def get_china_time_str_from_ms(ms, style="%Y-%m-%d %H:%M:%S"):
    """
    获取中国日期字符串
    :param ms:
    :param style:
    :return:
    """
    dt_china = get_china_time_from_ms(ms)
    return dt_china.strftime(style)


def get_china_time_str_from_s(s, style="%Y-%m-%d %H:%M:%S"):
    """
    获取中国日期字符串
    :param s:
    :param style:
    :return:
    """
    dt_china = get_china_time_from_s(s)
    return dt_china.strftime(style)


def get_datetime_by_ms_timezone(ms, tzstr):
    """
    获取中国时间
    :param ms: UTC毫秒数
    :param tzstr 字符串: Asia/Shanghai  US/Eastern
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000.0, pytz.timezone(tzstr))


def get_datetime_ymd(dt):
    """
    获取年月日的整数值
    :param dt:
    :return:
    """
    year = dt.year
    month = dt.month
    day = dt.day
    return year, month, day


def get_datetime_str_with_ms(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
