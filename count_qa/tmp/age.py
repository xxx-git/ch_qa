#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import re
import datetime
def string_translation_one(matched):#零一二三四五六七八九 或者 零壹贰叁肆伍陆柒捌玖-0123456789
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
	string = re.sub('(?P<value>\零)',string_translation_one,string_data)
	string = re.sub('(?P<value>\一)',string_translation_one,string)
	string = re.sub('(?P<value>\二)',string_translation_one,string)
	string = re.sub('(?P<value>\三)',string_translation_one,string)
	string = re.sub('(?P<value>\四)',string_translation_one,string)
	string = re.sub('(?P<value>\五)',string_translation_one,string)
	string = re.sub('(?P<value>\六)',string_translation_one,string)
	string = re.sub('(?P<value>\七)',string_translation_one,string)
	string = re.sub('(?P<value>\八)',string_translation_one,string)
	string = re.sub('(?P<value>\九)',string_translation_one,string)
	string = re.sub('(?P<value>\壹)',string_translation_one,string)
	string = re.sub('(?P<value>\贰)',string_translation_one,string)
	string = re.sub('(?P<value>\叁)',string_translation_one,string)
	string = re.sub('(?P<value>\肆)',string_translation_one,string)
	string = re.sub('(?P<value>\伍)',string_translation_one,string)
	string = re.sub('(?P<value>\陆)',string_translation_one,string)
	string = re.sub('(?P<value>\柒)',string_translation_one,string)
	string = re.sub('(?P<value>\捌)',string_translation_one,string)
	string = re.sub('(?P<value>\玖)',string_translation_one,string)
	return string	

def date_valid(year,month,day):
	if year<=datetime.datetime.now().year and (month>=1 and month<=12) and (day>=1 and day<=31):#日期的合法性检查
		return True

def get_date_value(string_data):
	reg = r'^\w*(?!-)(\d{4})年(\d{1,2})月(\d{1,2})日\w*$|^(?!-)(\d{2,4})\.(\d{1,2})\.(\d{1,2})\w*$' #控制不能输出负年份
	p = re.compile(reg)
	m = p.search(string_data)
	if m:
		if  re.search('\.',string_data):
			year ,month , day = int(m.group(4)),int(m.group(5)),int(m.group(6))
			if date_valid(year,month,day):
			    list = [year,month,day]
			    return list
			return None    
		else :
			year ,month ,day = int(m.group(1)),int(m.group(2)),int(m.group(3))
			if date_valid(year,month,day):
			    list = [year,month,day]
			    return list
			return None    
	return None

def get_date_valid(year,month,day):  #计算年龄，精确到日，输出与年龄格式为：（年岁，月，日）
	year_now = datetime.datetime.now().year
	month_now = datetime.datetime.now().month
	day_now = datetime.datetime.now().day
	if  month<=month_now and day<=day_now:
		year_compare = year_now-year
		month_compare = month_now-month
		day_compare = day_now-day
		list1 = (year_compare,month_compare,day_compare)
		return list1
	elif year<year_now and month>month_now and day<=day_now:
		year_compare = year_now-year-1
		month_compare = month_now+12-month
		day_compare = day_now-day
		list = (year_compare,month_compare,day_compare)
		return list	
	elif   month<month_now and day>day_now:
	    year_compare = year_now-year
	    month_compare = month_now-month-1
	    day_compare = day_now+30-day
	    list = (year_compare,month_compare,day_compare)
	    return list	
	elif year<year_now and month>=month_now and day>day_now:    		
	    year_compare = year_now-year-1
	    month_compare = month_now+11-month
	    day_compare = day_now+30-day
	    list = (year_compare,month_compare,day_compare)
	    return list
	else:
		return None

string = string_translation_two('一九32年肆月5日')
list1 = get_date_value(string)
list2 = get_date_valid(list1[0],list1[1],list1[2])
year = ('year',list1[0])
month = ('month',list1[1])
day = ('day',list1[2])    
info = (year,month,day,('age',list2))
print info