#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import re
#零一二三四五六七八九 或者 零壹贰叁肆伍陆柒捌玖-0123456789
def string_translation_one(matched):
    value = matched.group('value')
    if value == '零':
        return str(0)
    elif value == '一'or value == '壹':
        return str(1)
    elif value == '二'or value == '贰':	
        return str(2)
    elif value == '三'or value == '叁':
        return str(3)
    elif value == '四'or value == '肆':
        return str(4)
    elif value == '五'or value == '伍':
        return str(5)
    elif value == '六'or value == '陆':
        return str(6)
    elif value == '七'or value == '柒':
        return str(7)
    elif value == '八'or value == '捌':
        return str(8)
    elif value == '九'or value == '玖':
        return str(9)


def string_translation_two(string_data):
    string = re.sub('(?P<value>\零)', string_translation_one,string_data)
    string = re.sub('(?P<value>\一)', string_translation_one,string)
    string = re.sub('(?P<value>\二)', string_translation_one,string)
    string = re.sub('(?P<value>\三)', string_translation_one,string)
    string = re.sub('(?P<value>\四)', string_translation_one,string)
    string = re.sub('(?P<value>\五)', string_translation_one,string)
    string = re.sub('(?P<value>\六)', string_translation_one,string)
    string = re.sub('(?P<value>\七)', string_translation_one,string)
    string = re.sub('(?P<value>\八)', string_translation_one,string)
    string = re.sub('(?P<value>\九)', string_translation_one,string)
    string = re.sub('(?P<value>\壹)', string_translation_one,string)
    string = re.sub('(?P<value>\贰)', string_translation_one,string)
    string = re.sub('(?P<value>\叁)', string_translation_one,string)
    string = re.sub('(?P<value>\肆)', string_translation_one,string)
    string = re.sub('(?P<value>\伍)', string_translation_one,string)
    string = re.sub('(?P<value>\陆)', string_translation_one,string)
    string = re.sub('(?P<value>\柒)', string_translation_one,string)
    string = re.sub('(?P<value>\捌)', string_translation_one,string)
    string = re.sub('(?P<value>\玖)', string_translation_one,string)

    return string


def get_pop_value(string_data):
    reg = r'^\D*(?!-)(\d+\.?\d*)亿\D*$|^\D*(?!-)(\d+\.?\d*)千万\D*$|^\D*(?!-)(\d+\.?\d*)百万\D*$|^\D*(?!-)(\d+\.?\d*)十万\D*$|^\D*(?!-)(\d+\.?\d*)万\D*$'   #只考虑以“亿，千万，百万，十万，万”为单位的人口，单位统一于万
    p = re.compile(reg)
    m = p.search(string_data)
    if m:
        if m.group(1):
            pop = float(m.group(1))
            pop = 10000*pop
        elif m.group(2):
            pop = float(m.group(2))
            pop = 1000*pop
        elif m.group(3):
            pop = float(m.group(3))
            pop = 100*pop
        elif m.group(4):
            pop = float(m.group(4))
            pop = 10*pop
        else:
            pop = float(m.group(5))
        return pop
        
string = string_translation_two('13.6782亿人')
pop = get_pop_value(string)
print pop