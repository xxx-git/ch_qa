#-*-encoding:utf-8-*-
#coding=utf8
__author__ = 'hw'

'''
本文件的作用：以属性名 和 属性值作为参数，返回规范化的结果
'''

import sys
from collections import defaultdict
import re
import codecs
import math

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#长度、重量、面积、体积、货币单位
unit_dict = {u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}
length_unit = {u'米':'m',u'厘米':'cm', u'分米':'dm', u'毫米':'mm', u'公里':'km', u'千米':'km',u'尺':'chi',u'寸':'cun'}
centimeter_change = {'m':100, 'dm':10, 'cm':1, 'mm':0.1, 'km':100000, 'chi':33.3, 'cun':3.33}   #所有长度单位向厘米转换
meter_change = {'m':1, 'dm':0.1, 'cm':0.01, 'mm':0.001, 'km':1000, 'chi':0.33, 'cun':0.033}
weight_unit = {u'公斤':'kg', u'千克':'kg', u'克':'g', u'毫克':'mg', u'吨':'t', u'斤':'catty',u'两':'liang',u'磅':'lb'}
weight_change = {'mg':0.0000001, 'g':0.001, 'kg':1, 't':1000, 'catty':0.5, 'liang':0.1, 'lb':0.4536}   #所有重量单位向kg转换
area_unit = {u'平方公里':'square_km',u'平方千米':'square_km',u'平方米':'square_m',u'平方分米':'square_dm',u'平方厘米':'square_cm',u'平方毫米':'square_mm', u'公顷':'ha',u'公亩':'are',u'亩':'mu',u'英亩':'acre'}
area_change = {'square_km':1, 'square_m':1e-6,'square_dm':1e-8,'square_cm':1e-10, 'square_mm':1e-12, 'ha':0.01, 'are':0.0001,'mu':0.0006667,'acre':0.0040469}
volume_unit = {u'立方米':'cube_m',u'立方分米':'cube_dm',u'立方厘米':'cube_cm',u'立方毫米':'cube_mm',u'升':'l',u'毫升':'ml'}
volume_change = {'cube_m':1, 'cube_dm':0.001,'cube_cm':1e-6, 'cube_mm':1e-9, 'l':0.001,'ml':1e-6}
currency_unit = {u'美金':'dollar', u'美元':'dollar', u'美分':'cent', u'港元':'HK_dollar',u'港币':'HK_dollar', u'澳元':'au_dollar', u'澳币':'au_dollar', u'加元':'can_dollar',u'加拿大元':'can_dollar', u'英镑':'pound', u'欧元':'Euro', u'人民币':'rmb', u'元':'yuan'}
currency_change = {'dollar':6.64, 'cent':0.0664, 'HK_dollar':0.85, 'au_dollar':5.08, 'can_dollar':5.17, 'pound':8.72, 'Euro':7.73, 'rmb':1, 'yuan':1}

def check_all_chinese(check_str):
    '''判断一个字符串是否全是中文字符'''
    for ch in check_str.decode('utf-8'):
        if  ch < u'\u4e00' or ch > u'\u9fff':
            return False
    return True

def unit2num(str_value):
    '''转换 万元 亿元...(前面不含数字)'''
    i = 0
    num_value = 1
    end = i + 1
    while i < len(str_value) and str_value[i:end] in unit_dict:
        num_value *= unit_dict[str_value[i:end]]
        i = end
        end = i+1
    return num_value, str_value[i:]

def chinese2number(str_value):
    '''转换 纯中文数字'''
    chinese_num = {u'零':0,u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9}
    tran_ch = {u'壹':1,u'贰':2,u'叁':3,u'肆':4,u'伍':5,u'陆':6,u'柒':7,u'捌':8,u'玖':9}
    i = 0
    num_value = 0
    cur_num = 0
    end = i + 1
    while i < len(str_value) and (str_value[i:end] in chinese_num or str_value[i:end] in unit_dict or str_value[i:end] in tran_ch):
        if str_value[i:end] in chinese_num:
            num_value += cur_num
            cur_num = chinese_num[str_value[i:end]]
        elif str_value[i:end] in tran_ch:
            num_value += cur_num
            cur_num = tran_ch[str_value[i:end]]
        else:    #说明在unit_dict中
            if num_value + cur_num < unit_dict[str_value[i:end]]:
                cur_num += num_value
                num_value = 0
            cur_num *= unit_dict[str_value[i:end]]
        i = end
        end = i+1
    num_value += cur_num
    if num_value == 0:
        return str_value
    else:
        return str(num_value) + str_value[i:]

def standardize(num, unit, unit_map, change_map, standard_unit):
    if unit in unit_map:
        unit = unit_map[unit]
    new_num = num
    if unit in change_map:
        new_num = change_map[unit] * float(num)
        unit = standard_unit
    return new_num, unit

def pre_process(value):
    '''对属性值进行预处理：删除括号等特殊字符'''
    if value.find(u'约') != -1:
        value = value[value.index(u'约')+1:]
    if value.find(u'(') != -1:
        value = value[:value.index(u'(')]
    if value.find(u'（') != -1:
        value = value[:value.index(u'（')]
    value = value.replace(',','').replace(u'，','').replace(' ','')
    value = chinese2number(value)  ##把属性值其中的中文数字转为纯数字
    return value
                 
def unify_date(date_str):
    '''将所有的日期类型的属性值进行规范'''
    chinese_num = {u'零':'0',u'一':'1',u'二':'2',u'三':'3',u'四':'4',u'五':'5',u'六':'6',u'七':'7',u'八':'8',u'九':'9'}
    tran_ch = {u'壹':'1',u'贰':'2',u'叁':'3',u'肆':'4',u'伍':'5',u'陆':'6',u'柒':'7',u'捌':'8',u'玖':'9'}
    i = 0
    end = i + 1
    new_date_str = ""
    if date_str.isdigit():
        return (-int(date_str), None, None)
    elif date_str.find(u'前')!=-1 and date_str[date_str.index(u'前')+1:].isdigit():
        return (-int(date_str[date_str.index(u'前')+1:]), None, None)
    while i < len(date_str):
        if date_str[i:end] in chinese_num:
            new_date_str += chinese_num[date_str[i:end]]
        elif date_str[i:end] in tran_ch:
            new_date_str += tran_ch[date_str[i:end]]
        else:
            new_date_str += date_str[i:end]
        i = end
        end = i + 1
    date_str = new_date_str
    pattern_all1 = re.compile(ur'(\d+)年(\d+)月(\d+)日')
    pattern_all2 = re.compile(ur'^(\d+)[\./-](\d+)[\./-](\d+)')
    #findall()返回的是括号所匹配到的结果,如果没有括号就返回就返回整条语句所匹配到的结果
    date_all1 = re.findall(pattern_all1, date_str)
    date_all2 = re.findall(pattern_all2, date_str)
    if date_all1 or date_all2:
        if date_all2:
            return (int(date_all2[0][0]), int(date_all2[0][1]), int(date_all2[0][2]))
        elif date_str.find(u'前') != -1:
            return (-int(date_all1[0][0]), int(date_all1[0][1]), int(date_all1[0][2]))
        else:
            return (int(date_all1[0][0]), int(date_all1[0][1]), int(date_all1[0][2]))

    pattern_year_month1 = re.compile(ur'(\d+)年(\d+)月')
    pattern_year_month2 = re.compile(ur'^(\d+)[\./-](\d+)')
    date_year_month1 = re.findall(pattern_year_month1, date_str)
    date_year_month2 = re.findall(pattern_year_month2, date_str)
    if date_year_month1 or date_year_month2:
        if date_year_month2:
            return (int(date_year_month2[0][0]), int(date_year_month2[0][1]), None)
        elif date_str.find(u'前') != -1:
            return (-int(date_year_month1[0][0]), int(date_year_month1[0][1]), None)
        else:
            return (int(date_year_month1[0][0]), int(date_year_month1[0][1]), None)

    pattern_month_day = re.compile(ur'(\d+)月(\d+)日')
    date_month_day = re.findall(pattern_month_day, date_str)
    if date_month_day and date_str.find(u'前') != -1:
        return (None, -int(date_month_day[0][0]), int(date_month_day[0][1]))
    elif date_month_day:
        return (None, int(date_month_day[0][0]), int(date_month_day[0][1]))
    pattern_year = re.compile(ur'(\d+)年')
    date_year = re.findall(pattern_year, date_str)
    if date_year and date_str.find(u'前') != -1:
        return (-int(date_year[0]), None, None)
    elif date_year:
        return (int(date_year[0]), None, None)

    return date_str

def unify_number(pro, value, num):
    segs = re.split(r'\d+\.?\d*', value)
    unit = segs[-1]   #进制、单位
    num = num[0]      #数值
    value_type = None
    if check_all_chinese(unit):
        temp_num, unit = unit2num(unit)
        num = float(num) * int(temp_num)
    unit = unit.lower()
    if u'价' in pro or u'费用' in pro or 'GDP' in pro or u'总计' in pro or u'总值' in pro:
        if unit == '$' or value.find('$')!=-1:
            unit = 'dollar'
        elif unit == u'￡' or value.find(u'￡')!=-1:
            unit = 'pound'
        elif unit == u'￥' or value.find(u'￥')!=-1:
            unit = 'rmb'
        elif unit == u'€' or value.find(u'€')!=-1:
            unit = 'Euro'
        num, unit = standardize(num, unit, currency_unit, currency_change, '元')
        value_type = 'money'
    elif u'身高' in pro or u'身长' in pro or u'体长' in pro:
        num, unit = standardize(num, unit, length_unit, centimeter_change, '厘米')
        value_type = 'tall'
    elif u'海拔' in pro or u'海岸线' in pro or u'长' in pro or u'高' in pro in u'宽' in pro:
        num, unit = standardize(num, unit, length_unit, meter_change, '米')
        value_type = 'height'
    elif u'重' in pro or u'质量' in pro:
        num, unit = standardize(num, unit, weight_unit, weight_change, '公斤')
        value_type = 'weight'
    elif u'面积' in pro or u'占地' in pro:
        num, unit = standardize(num, unit, area_unit, area_change, '平方公里')
        value_type = 'area'
    elif u'体积' in pro or u'容量' in pro or u'库容' in pro or u'流量' in pro or u'容积' in pro:
        num, unit = standardize(num, unit, volume_unit, volume_change, '立方米')
        value_type = 'volume'
    else:
        return None, None
    if isinstance(num, unicode):
        num = float(num)
    return (str([str(num),int(num)][int(num)==num]), unit), value_type

def unify_value(pro, old_value):
    if isinstance(pro, str) == True:
        pro = pro.decode('utf-8')
    if isinstance(old_value, str) == True:
        old_value = old_value.decode('utf-8')
    date_pro = [u"时间", u"日", u"年月", u'日期']
    if pro.find(date_pro[0])!=-1 or pro.find(date_pro[1])!=-1 or pro.find(date_pro[2])!=-1 or pro.find(date_pro[3])!=-1:
        year_month_day = unify_date(old_value)
        return pro, year_month_day, 'time'

    if u'价' in pro or u'费用' in pro or 'GDP' in pro or u'总计' in pro or u'总值' in pro \
        or u'身高' in pro or u'身长' in pro or u'体长' in pro \
        or u'海拔' in pro or u'海岸线' in pro or u'长' in pro or u'高' in pro in u'宽' in pro \
        or u'重' in pro or u'质量' in pro or u'面积' in pro or u'占地' in pro \
        or u'体积' in pro or u'容量' in pro or u'库容' in pro or u'流量' in pro or u'容积' in pro:
        value = pre_process(old_value)   #对属性值进行预处理
        num = re.findall(r'\d+\.?\d*', value)
        if num != []:
            value, value_type = unify_number(pro, value, num)
            return pro, value, value_type
        else:
            return None, None, None
            # return pro, old_value
    else:
        return None, None, None
        # return pro, old_value



if __name__ == '__main__':
    # pro_key = sys.argv[1]
    # pro_value = sys.argv[2]
    # pro_key, pro_value = unify_value(pro_key, pro_value)
    # print pro_key, pro_value

    p = "海拔"
    a = "500m"
    b = '1.9864m'
    c = '成人255港元'
    d = '1318km2'
    pro, value, value_type = unify_value(p, a)
    print pro, value, value_type
    pro, value, value_type = unify_value('重点景点', "三个")
    print pro, value, value_type
    pro, value, value_type = unify_value("逝世时间", '一八九九年1月1日(1977年)')
    print pro, value, value_type