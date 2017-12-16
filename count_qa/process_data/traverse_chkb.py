# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import unify_property_value
import neo4j_data
from collections import defaultdict
import json


def gen_tag_entity_dict():
    kb_path = '../../data/to_DB.json'
    with open(kb_path) as fin:
        kb_dict = json.load(fin, encoding='utf-8')
    print('load kb succeed')

    tag_entity_dict = defaultdict(list)
    for key, value in kb_dict.iteritems():
        tag_list = value['taglist'].split(',')
        for tag in tag_list:
            if tag:
                tag = tag.replace('\n', '')
                tag_entity_dict[tag].append(key)
    out_path = 'tag_entity_dict'
    with open(out_path, 'wb') as fout:
        for tag, entity_list in tag_entity_dict.iteritems():
            print>>fout, json.dumps({tag: entity_list}, encoding='utf-8', ensure_ascii=False)


def read_data(data_path, out_path):
    with open(data_path) as fin:
        kb_dict = json.load(fin, encoding='utf-8')
    print('load kb succeed')
    tag_count = {}
    for key, value in kb_dict.iteritems():
        tag_list = value['taglist'].split(',')
        for tag in tag_list:
            tag_count[tag] = tag_count.get(tag, 0)+1
    res = sorted(tag_count.items(), key=lambda x:x[1], reverse=True)
    with open(out_path, 'wb') as fout:
        for tag, count in res:
            print>>fout, ' '.join((tag, str(count))).encode('utf-8')


def get_entity():
    kb_path = '../../data/to_DB_part.json'
    with open(kb_path) as fin:
        kb_dict = json.load(fin, encoding='utf-8')
    print('load kb succeed')
    tag_path = '../../data/qa_concept_entity.json'
    tag_dict = {}
    with open(tag_path) as fin:
        for line in fin:
            tmp_dict = json.loads(line, encoding='utf-8')
            for key, value in tmp_dict.iteritems():
                tag_dict[key] = value

    print('load tag succeed')
    m_entity_list = set()
    if u'山峰' in tag_dict.keys():
        # print(tag_dict[u'山峰'])
        for item in tag_dict[u'山峰']:
            m_entity_list.add(item)
    if u'山脉' in tag_dict.keys():
        for item in tag_dict[u'山脉']:
            m_entity_list.add(item)
    if u'山' in tag_dict.keys():
        for item in tag_dict[u'山']:
            m_entity_list.add(item)
    out_path = 'mountain_entity'
    fout = open(out_path, 'wb')
    for entity in m_entity_list:
        print>>fout, ':'.join((entity, kb_dict[entity]['name'])).encode('utf-8')


def get_rel():
    # kb_path = '../../data/to_DB.json'
    # with open(kb_path) as fin:
    #     kb_dict = json.load(fin, encoding='utf-8')
    # print('load kb succeed')
    type_dict = {}
    # rel_count = {}
    file_path = 'mountain_entity'
    with open(file_path) as fin:
        for line in fin:
            entity_id, entity_name = line.decode('utf-8').strip().split(':')
            inf_dict = neo4j_data.search_node_neo4j(entity_id)
            for rel, value in inf_dict.iteritems():
                # print(' '.join((rel, value)))
                ret_rel, ret_value, value_type = unify_property_value.unify_value(rel, value)
                if ret_rel and ret_value and value_type:
                    if value_type not in type_dict.keys():
                        type_dict[value_type] = {}
                        type_dict[value_type][ret_rel] = 1
                    else:
                        type_dict[value_type][ret_rel] = type_dict[value_type].get(ret_rel, 0)+1
                    # rel_count[ret_rel] = rel_count.get(ret_rel, 0) + 1
            # inf_list = kb_dict[entity_id]['infobox_string']
            # for inf in inf_list:
            #     print(' '.join((inf[0], inf[1])))
            #     ret_rel, ret_value = unify_property_value.unify_value(inf[0], inf[1])
            #     if ret_rel and ret_value:
            #         rel_count[ret_rel] = rel_count.get(ret_rel, 0) + 1

    # res = sorted(rel_count.items(), key=lambda x: x[1], reverse=True)
    # print_type_dict(type_dict)
    return type_dict


def print_type_dict(type_dict):
    out_path = 'mountain_rel'
    fout = open(out_path, 'wb')
    for value_type, rel_count in type_dict.iteritems():
        res = sorted(rel_count.items(), key=lambda x: x[1], reverse=True)
        print>>fout, (value_type+':').encode('utf-8')
        for rel, count in res:
            print>>fout, ' '.join((rel, str(count))).encode('utf-8')
        print>>fout


def gen_tag_dict():
    type_dict = get_rel()
    tag_dict_list = []
    tag_dict= {}
    tag_dict['tag_list'] = [u'山', u'山峰', u'山脉']
    tag_dict['predicate_compare'] = {}
    for value_type, rel_count in type_dict.iteritems():
        res = sorted(rel_count.items(), key=lambda x: x[1], reverse=True)
        rel_list = []
        rel_tmp = []
        for rel, count in res:
            if count >= 5:
                rel_tmp.append(rel)
                rel_list.append(rel)
            if count >= 2:
                rel_list.append(rel)
        for rel in rel_tmp:
            tag_dict['predicate_compare'][rel] = rel_list
    tag_dict_list.append(tag_dict)
    fout = open('tag_dict', 'wb')
    print>>fout, json.dumps(tag_dict_list, ensure_ascii=False, indent=1).encode('utf-8')


def get_entity_by_tag(tag_list):
    file_path = 'tag_entity_dict'
    tag_entity_dict = {}
    with open(file_path) as fin:
        for line in fin:
            # print(line.decode('utf-8'))
            tmp_dict = json.loads(line.decode('utf-8').strip())
            tag_entity_dict.update(tmp_dict)
    ret_list = []
    for tag in tag_list:
        if tag in tag_entity_dict.keys():
            entity_list = tag_entity_dict[tag]
            ret_list.extend(entity_list)
    print(len(ret_list))
    kb_mini = {}
    tag_key = ' '.join(tag_list)
    kb_mini[tag_key] = {}
    for entity_keyid in ret_list:
        entity_dict = neo4j_data.search_node_neo4j(entity_keyid)
        kb_mini[tag_key][entity_keyid] = entity_dict
    out_path = 'kb_mini'
    with open(out_path, 'wb') as fout:
        json.dump(kb_mini, fout, encoding='utf-8', ensure_ascii=False)


if __name__ == '__main__':
    # read_data('../../data/to_DB.json', '../../data/tag_count')
    # get_entity()
    # get_rel()
    # gen_tag_dict()
    # get_entity_by_tag([u'山', u'山峰', u'山脉'])
    # gen_tag_entity_dict()
    pass
