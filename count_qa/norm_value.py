#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import datetime

data_reg = u'\D*(\d+)年(\d+)月(\d+)日|\D*(\d+)\.(\d+)\.(\d+)'  # 正则表达式


def get_date_value(data_str):
    p = re.compile(data_reg)
    m = p.search(data_str)
    if m:
        if re.search('\.', data_str):
            year, month, day = m.group(4), m.group(5), m.group(6)
        else:
            year, month, day = m.group(1), m.group(2), m.group(3)
        ret_list = [int(year), int(month), int(day)]
        return ret_list
    return None


# list1 = get_date_value(u'1982年2月26日')
# local = datetime.datetime.now().year
#
# year = ('year', list1[0])
# month = ('month', list1[1])
# day = ('day', list1[2])
# age = local - int(list1[0])
# info = (year, month, day, ('age', age))
# print info