# -*- coding:utf-8 -*-
from data_manager import tag_dict, kb_mini
from get_entity import get_popular_entity
from unify_property_value import unify_value
from vector_manager import get_similarity
import heapq


def choose_tag_predicate(entity_tag, rel_str):
    tag_sim_score = 0
    rel_dict_max = None
    tag_list_max = None

    for tag_str, rel_dict in tag_dict.iteritems():
        tag_list = tag_str.split()
        for tag in tag_list:
            score = get_similarity(tag, entity_tag)
            if score > tag_sim_score:
                rel_dict_max = rel_dict
                tag_list_max = tag_list
                tag_sim_score = score
    print('tag: ' + ','.join(tag_list_max))

    pre_sim_score = 0
    pre_list_max = None
    for pred_str, pre_list in rel_dict_max.iteritems():
        pred_list = pred_str.split()
        for predicate in pred_list:
            score = get_similarity(predicate, rel_str)
            if score > pre_sim_score:
                pre_sim_score = score
                pre_list_max = pre_list
    print('predicate: ' + ','.join(pre_list_max))
    return tag_list_max, pre_list_max


def search_entity_by_tag(tag_list, entity_range):
    ret_entity_dict_list = []
    tag_key = ' '.join(tag_list)
    if tag_key in kb_mini.keys():
        for key, entity_dict in kb_mini[tag_key].iteritems():
            # print(entity_dict['description'])
            if entity_range in entity_dict['description']:
                ret_entity_dict_list.append(entity_dict)
    return ret_entity_dict_list


def get_order_from_str(order_str):
    order = 0
    for key, val in num_dict.iteritems():
        if key in order_str:
            order = val
    return order
num_dict = {u'第一': 0, u'第二': 1, u'第三': 2, u'第四': 3, u'第五': 4,
           u'第六': 5, u'第七': 6, u'第八': 7, u'第九': 8, u'第十': 9,
           u'第十一': 10, u'第十二': 11, u'第十三': 12, u'第十四': 13, u'第十五': 14}


def delete_repeat(ranked_list):
    last_name = None
    last_value = None
    ret_list = []
    for res in ranked_list:
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
    return ret_list


def count_most_question(entity_range, order_str, tag_list, rel_list, top_k=20):
    order = get_order_from_str(order_str)
    entity_dict_list = search_entity_by_tag(tag_list, entity_range)
    res_list = []
    for entity_dict in entity_dict_list:
        for pre in rel_list:
            if pre in entity_dict.keys():
                if '[HD]' in entity_dict[pre]:
                    continue
                _a, value, _b = unify_value(pre, entity_dict[pre])
                if _a and value and _b:
                    res_list.append([entity_dict['neoId'], entity_dict['name'], float(value[0]), entity_dict['label'], pre])
                break
    rank_res_list = heapq.nlargest(top_k, res_list, key=lambda x: x[2])
    ret_list = delete_repeat(rank_res_list)
    for item in ret_list:
        print(' '.join((item[0], item[1], str(item[2]))))
    result = {}
    result['target'] = order
    result['triples'] = []
    for item in ret_list:
        result['triples'].append([{'neoId': item[0], 'name': item[1], 'label': item[3]}, item[4], item[2]])
    return result


# def count_most_question(entity_range, entity_tag, rel_str, order_str):
#     order = get_order_from_str(order_str)
#     tag_list, pre_list_max = choose_tag_predicate(entity_tag, rel_str)
#     # print('-------------1------------')
#     # print(' '.join(pre_list_max))
#     entity_dict_list = search_entity_by_tag(tag_list, entity_range)
#     # print('-------------2------------')
#     # print(entity_dict_list)
#     res_list = []
#     for entity_dict in entity_dict_list:
#         for pre in pre_list_max:
#             if pre in entity_dict.keys():
#                 _a, value, _b = unify_value(pre, entity_dict[pre])
#                 if _a and value and _b:
#                     res_list.append([entity_dict['keyId'], entity_dict['name'], float(value[0])])
#                 break
#     rank_res_list = heapq.nlargest(20, res_list, key=lambda x: x[2])
#     # rank_res_list = sorted(res_list, key=lambda x: x[2], reverse=True)
#     # print(rank_res_list)
#     ret_list = delete_repeat(rank_res_list)
#     for item in ret_list:
#         print(' '.join((item[0], item[1], str(item[2]))))
#     return ' '.join((ret_list[order][0], ret_list[order][1], str(ret_list[order][2])))


def count_population_diff(country_1, country_2):
    node_1 = get_popular_entity(country_1)
    node_2 = get_popular_entity(country_2)
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
        if population_1 > population_2:
            flag = True
            population_diff = population_1 - population_2
        else:
            flag = False
            population_diff = population_2 - population_1
        ret_node1 = [{'neoId': node_1['neoId'], 'name': node_1['name'], 'label': node_1['label']}, u'人口数量', node_1[u'人口数量']]
        ret_node2 = [{'neoId': node_2['neoId'], 'name': node_2['name'], 'label': node_2['label']}, u'人口数量', node_2[u'人口数量']]
        return flag, population_diff, ret_node1, ret_node2
    return None


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
        if height_1 > height_2:
            flag = True
            height_diff = height_1 - height_2
        else:
            flag = False
            height_diff = height_2 - height_1
        ret_node1 = [{'neoId': node_1['neoId'], 'name': node_1['name'], 'label': node_1['label']}, u'身高', node_1[u'身高']]
        ret_node2 = [{'neoId': node_2['neoId'], 'name': node_2['name'], 'label': node_2['label']}, u'身高', node_2[u'身高']]
        return flag, height_diff, ret_node1, ret_node2
    return None


def count_age_diff(entity_1, entity_2):
    node_1 = get_popular_entity(entity_1)
    node_2 = get_popular_entity(entity_2)
    birth_1 = None
    birth_2 = None
    pre_1 = None
    pre_2 = None
    if u'出生日期' in node_1.keys():
        birth_1 = node_1[u'出生日期']
        pre_1 = u'出生日期'
    elif u'出生年月' in node_1.keys():
        birth_1 = node_1[u'出生年月']
        pre_1 = u'出生年月'
    if u'出生日期' in node_2.keys():
        birth_2 = node_2[u'出生日期']
        pre_2 = u'出生日期'
    elif u'出生年月' in node_2.keys():
        birth_2 = node_2[u'出生年月']
        pre_2 = u'出生年月'
    if birth_1 and birth_2:
        _, birth_list_1, _ = unify_value(pre_1, birth_1)
        _, birth_list_2, _ = unify_value(pre_2, birth_2)
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
        ret_node1 = [{'neoId': node_1['neoId'], 'name': node_1['name'], 'label': node_1['label']}, pre_1, node_1[pre_1]]
        ret_node2 = [{'neoId': node_2['neoId'], 'name': node_2['name'], 'label': node_2['label']}, pre_2, node_2[pre_2]]
        return flag, year, month, ret_node1, ret_node2
    else:
        return None


if __name__ == '__main__':

    search_entity_by_tag([u'山', u'山峰', u'山脉'], None)
