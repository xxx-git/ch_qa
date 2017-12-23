# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import unify_property_value
import neo4j_data
from collections import defaultdict
import json


def load_tag(tag_list):
    file_path = 'tag_entity_dict'
    tag_entity_dict = {}
    with open(file_path) as fin:
        for line in fin:
            # print(line.decode('utf-8'))
            tmp_dict = json.loads(line.decode('utf-8').strip())
            tag_entity_dict.update(tmp_dict)
    print('load tag succeed!')
    ret_list = []
    for tag in tag_list:
        if tag in tag_entity_dict.keys():
            entity_list = tag_entity_dict[tag]
            ret_list.extend(entity_list)
    return ret_list


def load_kb():
    kb_path = '../../data/new_data_labeled.json'
    with open(kb_path) as fin:
        kb_dict = json.load(fin, encoding='utf-8')
    print('load kb succeed')
    return kb_dict


def load_kb_mini():
    kb_mini_path = 'kb_mini_test'
    kb_mini = {}
    with open(kb_mini_path) as fin:
        for line in fin:
            line_dict = json.loads(line.decode('utf-8').strip())
            for key, value in line_dict.iteritems():
                kb_mini[key] = value
    return kb_mini


def gen_kb_mini(tag_list, entity_list):
    tmp_dict = {}
    for entity_keyid in entity_list:
        entity_dict = neo4j_data.search_node_neo4j(entity_keyid)
        tmp_dict[entity_keyid] = entity_dict
    print(len(tmp_dict))
    out_path = 'kb_mini_test'
    tag_key = ' '.join(tag_list)
    with open(out_path, 'a') as fout:
        print>>fout, json.dumps({tag_key: tmp_dict}, encoding='utf-8', ensure_ascii=False)


def get_rel(tag_list):
    type_dict = {}
    kb_mini = load_kb_mini()
    tag_key = ' '.join(tag_list)
    entity_dict = kb_mini[tag_key]
    for entity_keyid, inf_dict in entity_dict.iteritems():
        for rel, value in inf_dict.iteritems():
            ret_rel, ret_value, value_type = unify_property_value.unify_value(rel, value)
            if ret_rel and ret_value and value_type:
                if value_type not in type_dict.keys():
                    type_dict[value_type] = {}
                    type_dict[value_type][ret_rel] = 1
                else:
                    type_dict[value_type][ret_rel] = type_dict[value_type].get(ret_rel, 0) + 1
    out_path = 'tmp_rel'
    fout = open(out_path, 'wb')
    for value_type, rel_count in type_dict.iteritems():
        res = sorted(rel_count.items(), key=lambda x: x[1], reverse=True)
        print>>fout, (value_type+':').encode('utf-8')
        for rel, count in res:
            print>>fout, ' '.join((rel, str(count))).encode('utf-8')
        print>>fout
    return type_dict


def gen_rel_dict(type_dict):
    rel_dict = {}
    for value_type, rel_count in type_dict.iteritems():
        res = sorted(rel_count.items(), key=lambda x: x[1], reverse=True)
        rel_key_list = []
        rel_list = []
        for rel, count in res:
            if count < 2:
                continue
            rel_list.append(rel)
            if count >= 5:
                rel_key_list.append(rel)
        rel_key_list = list(set(rel_key_list))
        rel_list = list(set(rel_list))
        if rel_key_list:
            rel_dict[' '.join(rel_key_list)] = rel_list
    return rel_dict


def get_entity_from_tag(tag_list):
    # kb_dict = load_kb()
    entity_list = load_tag(tag_list)
    gen_kb_mini(tag_list, entity_list)


def get_entity_from_label(label_list):
    label_file_path = '../../data/new_label.json'
    with open(label_file_path) as fin:
        entity_label_dict = json.load(fin, encoding='utf-8')
    entity_list = []
    for entity_keyid, label in entity_label_dict.iteritems():
        if label in label_list:
            entity_list.append(entity_keyid)
    gen_kb_mini(label_list, entity_list)


def gen_tag_rel_dict(tag_list, tag_label):
    if tag_label == 'tag':
        get_entity_from_tag(tag_list)
    elif tag_label == 'label':
        get_entity_from_label(tag_list)
    type_dict = get_rel(tag_list)
    rel_dict = gen_rel_dict(type_dict)
    out_path = 'tag_rel_dict_test'
    with open(out_path, 'a') as fout:
        print>>fout, json.dumps({' '.join(tag_list): rel_dict}, encoding='utf-8', ensure_ascii=False, indent=4)


def read_kb_mini():
    in_path = 'kb_mini_test'
    kb_mini = {}
    with open(in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip(), encoding='utf-8')
            for key, value in ll.iteritems():
                kb_mini[key] = value
                print(key)


def change_kb_mini():
    in_path = 'kb_mini_test'
    kb_mini = {}
    with open(in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip(), encoding='utf-8')
            for key, value in ll.iteritems():
                kb_mini[key] = value
    out_path = 'kb_mini_test'
    with open(out_path, 'w') as fout:
        for key, value in kb_mini.iteritems():
            if key != u'国家':
                print>>fout, json.dumps({key: value}, encoding='utf-8', ensure_ascii=False)


def change_tag_entity_dict():
    in_path = 'tag_entity_dict'
    out_path = 'tag_entity_dict_test'
    fout = open(out_path, 'wb')
    with open(in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip(), encoding='utf-8')
            for key, value in ll.iteritems():
                if key:
                    print>> fout, json.dumps({key: value}, ensure_ascii=False, encoding='utf-8')


def gen_tag_entity_dict():
    kb = load_kb()
    tag_entity_dict = {}
    for entity_keyid, infor_dict in kb.iteritems():
        if 'taglist' in infor_dict.keys():
            tag_list = infor_dict['taglist'].split(',')
        if not tag_list:
            continue
        for tag in tag_list:
            if tag in tag_entity_dict.keys():
                tag_entity_dict[tag].append(entity_keyid)
            else:
                tag_entity_dict[tag] = [entity_keyid]
    out_path = 'tag_entity_dict'
    with open(out_path, 'w') as fout:
        for tag, entity_keyid_list in tag_entity_dict.iteritems():
            print>>fout, json.dumps({tag:entity_keyid_list}, ensure_ascii=False, encoding='utf-8')


if __name__ == '__main__':
    # gen_tag_entity_dict()
    # tag_list = [u'国家']
    # get_entity(tag_list)
    # change_kb_mini()

    # label_list = [u'国家']
    # get_entity_from_label(label_list)

    # tag_list = [u'国家']
    # get_rel(tag_list)
    # read_kb_mini()
    # gen_tag_rel_dict([u'山', u'山峰', u'山脉'], 'tag')
    # gen_tag_rel_dict([u'国家'], 'label')
    change_tag_entity_dict()