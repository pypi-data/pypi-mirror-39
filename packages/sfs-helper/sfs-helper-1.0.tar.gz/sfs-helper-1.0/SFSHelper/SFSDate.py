#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time


def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday


def get_tomorrow():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow


def get_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_time():
    return int(time.time())


def differ_seconds(dt1, dt2):
    if len(str(dt1)) == 10:
        dt1 = str(dt1) + ' 00:00:00'
    if len(str(dt2)) == 10:
        dt2 = str(dt2) + ' 00:00:00'
    dt1 = datetime.datetime.strptime(str(dt1), '%Y-%m-%d %H:%M:%S')
    dt2 = datetime.datetime.strptime(str(dt2), '%Y-%m-%d %H:%M:%S')
    diff = dt2 - dt1
    print('diff.seconds', diff.seconds)
    return diff.seconds


# 计算根据当前时间的多少天前后


def now_plus_day(days):
    import datetime
    now_time = datetime.datetime.now()
    x_time = now_time + datetime.timedelta(days=days)
    x_day = x_time.strftime('%Y-%m-%d')
    return x_day


# 计算根据当前时间的多少小时后


def now_plus_hour(h):
    import datetime
    now_time = datetime.datetime.now()
    x_time = now_time + datetime.timedelta(hours=h)
    x_day = x_time.strftime('%Y-%m-%d %H:%M:%S')
    return x_day


# 计算未来的一个日期与当前日期的时间差


def fature_minus_now(dt):
    if len(str(dt)) == 10:
        dt = str(dt) + ' 00:00:00'
    # 构造一个将来的时间
    future = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S')
    # 当前时间
    now_time = datetime.datetime.now()
    # 求时间差
    delta = future - now_time
    hour = delta.seconds / 60 / 60
    minute = (delta.seconds - hour * 60 * 60) / 60
    seconds = delta.seconds - hour * 60 * 60 - minute * 60
    return {
        'day': delta.days,
        'hour': hour,
        'minute': minute,
        'seconds': seconds
    }


# 计算两个日期之间的时间差


def differ_two_days(dt1, dt2):
    if len(str(dt1)) == 10:
        dt1 = str(dt1) + ' 00:00:00'
    if len(str(dt2)) == 10:
        dt2 = str(dt2) + ' 00:00:00'
    # 构造一个将来的时间
    c1 = datetime.datetime.strptime(str(dt1), '%Y-%m-%d %H:%M:%S')
    c2 = datetime.datetime.strptime(str(dt2), '%Y-%m-%d %H:%M:%S')
    # 求时间差
    delta = c2 - c1
    hour = delta.seconds / 60 / 60
    minute = (delta.seconds - hour * 60 * 60) / 60
    seconds = delta.seconds - hour * 60 * 60 - minute * 60
    return {
        'day': delta.days,
        'hour': hour,
        'minute': minute,
        'seconds': seconds
    }
