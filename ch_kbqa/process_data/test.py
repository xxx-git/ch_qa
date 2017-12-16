# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import json
from global_path import get_data_path
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')


def count_db_rel():
    data_path = get_data_path()
    kb_file = os.path.join(os.path.join(data_path, 'kb'), 'to_DB.json')
    with open(kb_file) as fin:
        kb_dict = json.load(fin, encoding='utf-8')
    print('load kb succeed!')

    statistics_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.rel_count')
    fout = open(statistics_file, 'wb')

    rel_dict = {}
    count = 0
    for k, value in kb_dict.iteritems():
        if value['infobox_linked']:
            for t in value['infobox_linked']:
                # if t[0] in rel_dict.keys():
                #     rel_dict[t[0]] += 1
                # else:
                #     rel_dict[t[0]] = 1
                rel_dict[t[0]] = rel_dict.get(t[0], 0) + 1
        if value['infobox_string']:
            for t in value['infobox_string']:
                # if t[0] in rel_dict.keys():
                #     rel_dict[t[0]] += 1
                # else:
                #     rel_dict[t[0]] = 1
                rel_dict[t[0]] = rel_dict.get(t[0], 0) + 1
        count += 1
        if count % 100000 == 0:
            print("%d : %d" % (count, len(rel_dict)))
    rel_list = sorted(rel_dict.iteritems(), key=lambda x: x[1], reverse=True)
    for key, value in rel_list:
        print>>fout, ("%s : %d" % (key, value)).encode('utf-8')


def merge_rel(rel_dict = None):
    data_path = get_data_path()
    rel_file = os.path.join(os.path.join(data_path, 'kb'), 'all_pro_map_labeled.json')
    with open(rel_file) as fin:
        rel_map_dict = json.load(fin, encoding='utf-8')
    print('load rel succeed!')
    # reversed_dict = {v: k for k, v in rel_map_dict.items()}
    # map_dict = rel_map_dict.copy()
    # map_dict.update(reversed_dict)
    # new_rel_dict = dict()
    # for rel, count in rel_dict.iteritems():
    #     if rel in rel_map_dict.keys():
    #         if rel_map_dict[rel] in rel_dict.keys():
    #             new_rel_dict[rel_map_dict[rel]] = rel_dict[rel_map_dict[rel]] + count
    #         else:
    #             new_rel_dict[rel_map_dict[rel]] = count
    #     else:
    #         new_rel_dict[rel] = count
    return rel_map_dict


def gen_rel_dict():
    rel_dict = {}
    rel_map_dict = merge_rel()
    data_path = get_data_path()
    statistics_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.all_rel')
    with open(statistics_file) as fin:
        count = 0
        for line in fin:
            count += 1
            if count % 10000 == 0:
                print(count)
                print(len(rel_dict))
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            rel = line.decode('utf-8').strip()
            if not rel:
                continue
            if rel in rel_map_dict.keys():
                rel = rel_map_dict[rel]
            if rel in rel_dict.keys():
                rel_dict[rel] += 1
            else:
                rel_dict[rel] = 1
    statistics_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.rel_count')
    fout = open(statistics_file, 'wb')
    for rel, count in rel_dict.iteritems():
        print>>fout, ('%s : %d' % (rel, count)).encode('utf-8')


def sort_dict():
    data_path = get_data_path()
    temp_file = os.path.join(os.path.join(data_path, 'statistics'), 'temp.txt')
    rel_set = set()
    rel_dict = dict()
    with open(temp_file) as fin:
        for line in fin:
            line = line.decode('utf-8').strip().split()
            if len(line) >= 2:
                count = int(line[0])
                rel = ' '.join(line[1:])
                if count <= 5:
                    rel_set.add(rel)
                else:
                    rel_dict[rel] = count
            else:
                print(line)
    rel_dict = sorted(rel_dict.items(), key=lambda x: x[1], reverse=True)
    rel_little_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.rel_little')
    rel_dict_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.rel_dict')
    fout1 = open(rel_little_file, 'wb')
    fout2 = open(rel_dict_file, 'wb')
    for rel in rel_set:
        print>>fout1, rel.encode('utf-8')
    for rel, count in rel_dict:
        print>>fout2, ('%s : %d' % (rel, count)).encode('utf-8')


def read_rel(file_name):
    rel_set = set()
    data_path = get_data_path()
    temp_file = os.path.join(os.path.join(data_path, 'statistics'), file_name)
    with open(temp_file) as fin:
        for line in fin:
            line = line.decode('utf-8').strip().split(':')
            rel = line[0].strip()
            rel_set.add(rel)
    return rel_set


def check_rel():
    data_path = get_data_path()
    kb_rel_file = os.path.join(os.path.join(data_path, 'statistics'), 'kb.rel_dict')
    rel_dict = {}
    with open(kb_rel_file) as fin:
        for line in fin:
            line = line.decode('utf-8').strip().split(':')
            if len(line) == 2:
                rel = line[0].strip()
                count = int(line[1].strip())
                # if count >= 10:
                rel_dict[rel] = count
            else:
                print(line)

    gen_rel = read_rel('gen_qa.rel_count_0.5')
    print(len(gen_rel))
    count_gen = 0
    for rel in gen_rel:
        if rel in rel_dict.keys():
            count_gen += 1
    print(count_gen)

    nlpcc_rel = read_rel('nlpcc_qa.rel_count')
    print(len(nlpcc_rel))
    count_nlpcc = 0
    for rel in nlpcc_rel:
        if rel in rel_dict.keys():
            count_nlpcc += 1
        else:
            print(rel)
    print(count_nlpcc)


def filter_rel():
    data_path = get_data_path()
    fin_file_path = os.path.join(data_path, 'statistics/diff_rel')
    fout_file_path = os.path.join(data_path, 'statistics/diff_rel_select')
    fout = open(fout_file_path, 'wb')

    with open(fin_file_path) as fin:
        count = 0
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            rel_list = ll['rel_set']
            question = ll['question']
            if len(rel_list) < 2:
                print(ll)
            ll['select_rel'] = ''
            for rel in rel_list:
                if rel in question:
                    ll['select_rel'] = rel
                    count += 1
                    break
            print>>fout, json.dumps(ll, encoding='utf-8', ensure_ascii=False)
    print(count)


if __name__ == '__main__':
    # count_db_rel()
    # gen_rel_dict()
    # sort_dict()
    # check_rel()
    filter_rel()

