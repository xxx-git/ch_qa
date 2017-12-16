# -*- coding:utf-8 -*-
from data_manager import search_node_keyid
from get_entity import get_popular_entity
from unify_property_value import unify_value
from vector_manager import get_similarity
import norm_value
import json
import heapq
import time


def load_tag_dict():
    file_path = 'process_data/tag_dict'
    with open(file_path) as fin:
        tag_dict_list = json.load(fin, encoding='utf-8')
    return tag_dict_list
tag_dict_list = load_tag_dict()
# tag_dict_list = []


def load_entity_list(tag):
    entity_list = []
    file_path = 'process_data/mountain_entity'
    with open(file_path) as fin:
        for line in fin:
            entity_list.append(line.split(':')[0])
    return list(set(entity_list))
entity_list = load_entity_list('')
# entity_list = []


def load_mini_kb():
    file_path = 'process_data/kb_mini'
    with open(file_path) as fin:
        kb_mini = json.load(fin, encoding='utf-8')
    print('load kb_mini succeed!')
    return kb_mini
kb_mini = load_mini_kb()


def choose_tag_predicate(entity_tag, rel_str):
    tag_sim_score = 0
    tag_dict_max = None
    for tag_dict in tag_dict_list:
        tag_list = tag_dict['tag_list']
        for tag in tag_list:
            score = get_similarity(tag, entity_tag)
            if score > tag_sim_score:
                tag_dict_max = tag_dict
                tag_sim_score = score
    print(','.join(tag_dict_max['tag_list']))

    pre_cmp_dict = tag_dict_max['predicate_compare']
    pre_sim_score = 0
    pre_list_max = None
    for predicate, pre_list in pre_cmp_dict.iteritems():
        score = get_similarity(predicate, rel_str)
        # print(predicate)
        # print(score)
        if score > pre_sim_score:
            pre_sim_score = score
            pre_list_max = pre_list
    return tag_dict_max['tag_list'], pre_list_max


def search_entity_by_tag(tag_list, entity_range):
    ret_entity_dict_list = []
    tag_key = ' '.join(tag_list)
    if tag_key in kb_mini.keys():
        for key, entity_dict in kb_mini[tag_key].iteritems():
            # print(entity_dict['description'])
            if entity_range in entity_dict['description']:
                ret_entity_dict_list.append(entity_dict)

    # for entity_keyid in entity_list:
    #     print(time.asctime(time.localtime(time.time())))
    #     tag_flag = False
    #     entity_dict = search_node_keyid(entity_keyid)[0]
    #     for tag in tag_list:
    #         if tag in entity_dict['taglist']:
    #             tag_flag = True
    #             break
    #     if not tag_flag:
    #         continue
    #     ret_entity_dict_list.append(entity_dict)
        # if not entity_range and 'description' in entity_dict.keys() and entity_range in entity_dict['description']:
        #     ret_entity_dict_list.append(entity_dict)
    return ret_entity_dict_list


def get_order_from_str(order_str):
    order = 0
    for key, val in num_dict.iteritems():
        if key in order_str:
            order = val
    return order

num_dict= {u'第一': 0, u'第二': 1, u'第三': 2, u'第四': 3, u'第五': 4,
           u'第六': 5, u'第七': 6, u'第八': 7, u'第九': 8, u'第十': 9,
           u'第十一': 10, u'第十二': 11, u'第十三': 12, u'第十四': 13, u'第十五': 14}


def count_most_question(entity_range, entity_tag, rel_str, order_str):
    order = get_order_from_str(order_str)
    # if order_str == u'第一':
    #     order = 1
    tag_list, pre_list_max = choose_tag_predicate(entity_tag, rel_str)
    # print('-------------1------------')
    # print(' '.join(pre_list_max))
    entity_dict_list = search_entity_by_tag(tag_list, entity_range)
    # print('-------------2------------')
    # print(entity_dict_list)
    res_list = []
    for entity_dict in entity_dict_list:
        for pre in pre_list_max:
            if pre in entity_dict.keys():
                _a, value, _b = unify_value(pre, entity_dict[pre])
                if _a and value and _b:
                    res_list.append([entity_dict['keyId'], entity_dict['name'], float(value[0])])
                break
    rank_res_list = heapq.nlargest(20, res_list, key=lambda x: x[2])
    # rank_res_list = sorted(res_list, key=lambda x: x[2], reverse=True)
    # print(rank_res_list)
    last_name = None
    last_value = None
    ret_list = []
    for res in rank_res_list:
        if not last_name and not last_value:
            last_name = res[1]
            last_value = res[2]
            ret_list.append(res)
        else:
            if res[1] == last_name or res[2] == last_value:
                continue
            else:
                ret_list.append(res)
                last_name = res[1]
                last_value = res[2]
    for item in ret_list:
        print(' '.join((item[0], item[1], str(item[2]))))
    return ' '.join((ret_list[order][0], ret_list[order][1], str(ret_list[order][2])))


def count_population_diff(country_1, country_2):
    print(country_1)
    print(country_2)
    node_1 = get_popular_entity(country_1)
    node_2 = get_popular_entity(country_2)
    # print(node_1)
    # print(node_2)
    population_1 = None
    population_2 = None
    if u'人口数量' in node_1.keys():
        print(node_1[u'人口数量'])
        _, population_1, _ = unify_value(u'人口数量', node_1[u'人口数量'])
    if u'人口数量' in node_2.keys():
        print(node_2[u'人口数量'])
        _, population_2, _ = unify_value(u'人口数量', node_2[u'人口数量'])
    if population_1 and population_2:
        population_1 = int(population_1[0])
        population_2 = int(population_2[0])
        return population_1 - population_2


def count_height_diff(entity_1, entity_2):
    node_1 = get_popular_entity(entity_1)
    node_2 = get_popular_entity(entity_2)
    height_1 = None
    height_2 = None
    if u'身高' in node_1.keys():
        _, height_1, _ = unify_value(u'身高', node_1[u'身高'])
    if u'身高' in node_2.keys():
        _, height_2, _ = unify_value(u'身高', node_2[u'身高'])
    if height_1 and height_2:
        height_1 = float(height_1[0].strip())
        height_2 = float(height_2[0].strip())
        return height_1 - height_2
    return None


def count_age_diff(entity_1, entity_2):
    node_1 = get_popular_entity(entity_1)
    # for key, val in node_1.iteritems():
    #     print('%s: %s' % (key, val))
    node_2 = get_popular_entity(entity_2)
    # for key, val in node_2.iteritems():
    #     print('%s: %s' % (key, val))
    birth_1 = None
    birth_2 = None
    if u'出生日期' in node_1.keys():
        birth_1 = node_1[u'出生日期']
    if u'出生日期' in node_2.keys():
        birth_2 = node_2[u'出生日期']
    if birth_1 and birth_2:
        birth_list_1 = norm_value.get_date_value(birth_1)
        birth_list_2 = norm_value.get_date_value(birth_2)
        # birth_list_1 = unify_value(u'出生日期',birth_1)
        # birth_list_2 = unify_value(u'出生日期',birth_2)
        if birth_list_1[0] > birth_list_2[0]:
            flag = False
            if birth_list_1[1] >= birth_list_2[1]:
                month = birth_list_1[1] - birth_list_2[1]
                year = birth_list_1[0] - birth_list_2[0]
            else:
                month = birth_list_1[1] + 12 - birth_list_2[1]
                year = birth_list_1[0] - birth_list_2[0] - 1
        else:
            flag = True
            if birth_list_1[1] > birth_list_2[1]:
                month = birth_list_2[1] + 12 - birth_list_1[1]
                year = birth_list_2[0] - birth_list_1[0] - 1
            else:
                month = birth_list_2[1] - birth_list_1[1]
                year = birth_list_2[0] - birth_list_1[0]
        return flag, year, month
    else:
        return None


# def choose_node(node_list):
#     ret_node = None
#     max_popularity = 0
#     for node in node_list:
#         # if node['subname'] == 'NO_SUBNAME':
#         tmp_pop = len(node)
#         if tmp_pop > max_popularity:
#             max_popularity = tmp_pop
#             ret_node = node
#     return ret_node


if __name__ == '__main__':

    search_entity_by_tag([u'山', u'山峰', u'山脉'], None)
