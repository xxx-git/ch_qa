# -*- coding:utf-8 -*-
import re
from get_entity import parse_sentence
import count_function
import time
from data_manager import tag_dict, key_dict_format
import vector_manager


chinese = re.compile(u'[\u4e00-\u9fa5]')
# person_height_compare = u'^(.* )?(.+)/nr|z.* 比/p(.* )?(.+)/n.* (高|矮)/a .*$'

person_height_compare = u'^(.* )?(.+)/nr.* 比/p(.* )?(.+)/n.* (高|矮)/.* .*$'
person_age_compare = u'^(.* )?(.+)/nr.* 比/p(.* )?(.+)/n.* (大|小)/.* .*$'

country_population_compare = u'(.+)/n(s|z)(.*)?人口(.*)?比/p(.* )?(.+)/ns(.*)?多/.*(.*)?'

entity_rank = u'^(.+)/n(s|z)? .*( .+)/n(s|z)?$'


def t_rank_entity_question(seg_list, ques_pos, ner_list):
    tag_key_dict = key_dict_format(tag_dict)
    _, tag_key, score = vector_manager.get_max_similarity(seg_list, tag_key_dict)
    rel_dict = tag_dict[tag_key]
    rel_key_dict = key_dict_format(rel_dict)
    _, rel_key, score = vector_manager.get_max_similarity(seg_list, rel_key_dict)
    entity_range = ''
    order_str = None
    if u'/a' or u'/m' in ques_pos:
        word_pos_list = ques_pos.split()
        for i, word_pos in enumerate(word_pos_list):
            word, pos = word_pos.split('/')
            if ner_list[i] == 'B' and not entity_range:
                entity_range = word
            if pos == 'm':
                order_str = word
    if not order_str:
        if u'最' in ques_pos:
            order_str = u'第一'
    print(tag_key)
    print(rel_key)
    rel_list = rel_dict[rel_key]
    tag_list = tag_key.split()
    print(' '.join((entity_range, order_str, rel_key, tag_key)))
    return count_function.t_count_most_question(entity_range, order_str, tag_list, rel_list)


def rank_entity_question(match, ques_pos, ner_list):
    # entity_range = match.group(1)
    entity_tag = match.group(3).strip()

    entity_range = None
    rel_str = None
    order_str = None
    if u'/a' or u'/m' in ques_pos:
        word_pos_list = ques_pos.split()
        for i, word_pos in enumerate(word_pos_list):
            word, pos = word_pos.split('/')
            if ner_list[i] == 'B' and not entity_range:
                entity_range = word
            if pos == 'a':
                rel_str = word
            if pos == 'm':
                order_str = word
    if not rel_str:
        rel_str = entity_tag
    if not order_str:
        if u'最' in rel_str:
            order_str = u'第一'
    print(' '.join([entity_range, entity_tag, rel_str, order_str]))
    count_function.count_most_question(entity_range, entity_tag, rel_str, order_str)


def compare_country_population(match, ques_pos, ner_list):
    country_1 = match.group(1)
    country_2 = match.group(6)
    population_diff = count_function.count_population_diff(country_1, country_2)
    if population_diff > 0:
        ans = u'%s的人口数量比%s多%d' % (country_1, country_2, population_diff)
    elif population_diff < 0:
        ans = u'%s的人口数量比%s少%d' % (country_1, country_2, -population_diff)
    else:
        ans = u'%s和%s的人口数量一样多' % (country_1, country_2)
    return ans


def compare_person_height(match, ques_pos, ner_list):
    person_1 = match.group(2)
    person_2 = match.group(4)
    print(person_1)
    print(person_2)
    height_diff = count_function.count_height_diff(person_1, person_2)
    if height_diff > 0:
        ans = u'%s比%s高%scm' % (person_1, person_2, height_diff)
    elif height_diff == 0:
        ans = u'%s和%s一样高' % (person_1, person_2)
    else:
        ans = u'%s比%s高%scm' % (person_2, person_1, -height_diff)
    return ans


def compare_person_age(match, ques_pos, ner_list):
    flag = False
    for word in age_words:
        if word in ques_pos:
            flag = True
    if not flag:
        return None
    person_1 = match.group(2)
    person_2 = match.group(4)
    print(person_1)
    print(person_2)
    flag, year, month = count_function.count_age_diff(person_1, person_2)
    if year == 0 and month == 0:
        ans = u'%s和%s一样大' % (person_1, person_2)
    else:
        if flag:
            if year == 0:
                ans = u'%s比%s大%s个月' % (person_1, person_2, month)
            elif month == 0:
                ans = u'%s比%s大%s岁' % (person_1, person_2, year)
            else:
                ans = u'%s比%s大%s岁%s个月' % (person_1, person_2, year, month)
        else:
            if year == 0:
                ans = u'%s比%s大%s个月' % (person_2, person_1, month)
            elif month == 0:
                ans = u'%s比%s大%s岁' % (person_2, person_1, year)
            else:
                ans = u'%s比%s大%s岁%s个月' % (person_2, person_1, year, month)
    return ans
age_words = [u'年龄', u'年纪', u'岁']

pattern_dict = {
    person_height_compare: compare_person_height,
    person_age_compare: compare_person_age,
    country_population_compare: compare_country_population,
    # entity_rank: rank_entity_question
}


def classify_ques(question):
    parse_data = parse_sentence(question)
    seg_list = parse_data['seg']
    pos_list = parse_data['pos']
    ner_list = parse_data['ner']
    ques_pos = ' '.join(['/'.join((seg_list[i], pos_list[i]))for i in range(len(seg_list))])
    print(ques_pos)
    print(' '.join(ner_list))
    ans = None
    if u'最' in ques_pos:
        ans = t_rank_entity_question(seg_list, ques_pos, ner_list)
        return ans
    for pattern_str, target_function in pattern_dict.iteritems():
        pattern = re.compile(pattern_str)
        m = pattern.match(ques_pos)
        if m:
            print(target_function)
            ans = target_function(m, ques_pos, ner_list)
            if ans:
                break
    return ans


if __name__ == '__main__':
   # ques = sys.argv[1]
   # print(classify_ques(ensure_unicode(ques)))
   #  for i in range(5
   localtime = time.asctime(time.localtime(time.time()))
   print(localtime)
   print(classify_ques(u'门票最贵的山'))
   print('------------------------------')
   # print(classify_ques(u'中国最高的山'))
   # print('------------------------------')
   # print(classify_ques(u'中国最高的山是哪一座'))
   # print('------------------------------')
   # print(classify_ques(u'美国人口比印度多多少'))
   # print('------------------------------')
   # print(classify_ques(u'杨洋比鹿晗大多少岁'))
   # print('------------------------------')
   # print(classify_ques(u'杨洋比鹿晗高多少'))