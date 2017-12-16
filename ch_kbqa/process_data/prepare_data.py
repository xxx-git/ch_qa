# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import json
import re
from global_path import get_data_path
from ch_kbqa.process_data.data_manager import search_node_neo4j
from ch_kbqa.utils import ensure_unicode
reload(sys)
sys.setdefaultencoding('utf-8')


def get_triple(out_file_name):
    data_path = get_data_path()
    fout_path = os.path.join(data_path, out_file_name)
    fout = open(fout_path, 'wb')
    score_dict = {'0.5': 0, '1.0': 0, '1.5': 0, '2.0': 0, '>2.0': 0}
    data_dir_path = os.path.join(data_path, 'gen_qa/cqa_triple_match')
    file_list = os.listdir(data_dir_path)
    file_path_list = []
    for f in file_list:
        file_path_list.append(os.path.join(data_dir_path, f))
    triple_set = set()
    for file in file_path_list:
        with open(file) as fin:
            for line in fin:
                line = line.decode('utf-8').strip().split('\t')
                score = float(line[-1])
                if score < 0.5:
                    score_dict['0.5'] += 1
                elif 0.5 <= score < 1.0:
                    score_dict['1.0'] += 1
                elif 1.0 <= score < 1.5:
                    score_dict['1.5'] += 1
                elif 1.5 <= score < 2.0:
                    score_dict['2.0'] += 1
                else:
                    score_dict['>2.0'] += 1
                triple_set.add('|||'.join((line[2], line[3], line[4])))
        # break
    print(score_dict)
    for triple in triple_set:
        print>>fout, triple.encode('utf-8')


def get_triple_nlpcc(out_file_name):
    triple_set = set()
    data_path = get_data_path()
    fin_path = os.path.join(data_path, 'nlpcc_qa/ch.qatriple_all')
    with open(fin_path) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            line = line.decode('utf-8').strip()
            if '|||' in line and len(line.split('|||')) == 3:
                triple = line.split('|||')
                for i in range(len(triple)):
                    triple[i] = triple[i].strip()
                triple_set.add('|||'.join(triple))
    print(len(triple_set))
    fout_path = os.path.join(data_path, out_file_name)
    fout = open(fout_path, 'wb')
    for triple in triple_set:
        print>>fout, triple.encode('utf-8')


def del_brackets(name_str):
    match = bracket_pattern.match(name_str)
    if match:
        return match.group(1)
    return name_str
bracket_pattern = re.compile("(.*)(\(|\（).*(\)|\）)$")


def check_triple(triple_file_name, file_out_name):
    count = 0
    data_path = get_data_path()
    triple_file = os.path.join(data_path, triple_file_name)
    out_file = os.path.join(data_path, file_out_name)
    fout = open(out_file, 'wb')
    with open(triple_file) as fin:
        for line in fin:
            # sub_name, rel, obj_name = line.decode('utf-8').strip().split('\t')
            sub_name, rel, obj_name = line.decode('utf-8').strip().split('|||')
            sub_name = del_brackets(sub_name)

            if '\'' in sub_name:
                sub_name = sub_name.replace('\'', '\\\'')
            rel_dict_list = search_node_neo4j(sub_name)
            if not rel_dict_list:
                continue
            adict = dict()
            adict['reliable'] = []
            adict['possible'] = []
            adict['triple'] = '|||'.join((sub_name, rel, obj_name))
            for rel_dict in rel_dict_list:
                for neo4j_rel, value in rel_dict.iteritems():
                    neo4j_rel = ensure_unicode(neo4j_rel)
                    if neo4j_rel == 'description' or neo4j_rel == 'taglist' or not value:
                        continue
                    value = ensure_unicode(value)
                    if rel == neo4j_rel and obj_name in value:
                        adict['reliable'].append('|||'.join((sub_name, neo4j_rel, value)))
                    elif rel == neo4j_rel:
                        adict['possible'].append('|||'.join((sub_name, neo4j_rel, value)))
                    elif obj_name in value or value in obj_name:
                        adict['possible'].append('|||'.join((sub_name, neo4j_rel, value)))
            if adict['reliable'] or adict['possible']:
                count += 1
            print>>fout, json.dumps(adict, encoding='utf-8', ensure_ascii=False)
    print(count)


def count_rel(file_in):
    count = 0
    rel_set = set()
    with open(file_in) as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            if not line['reliable'] and not line['possible']:
                continue
            if line['reliable']:
                count += 1
                for triple in line['reliable']:
                    r_rel = triple.split('|||')[1]
                    rel_set.add(r_rel)
            if line['possible']:
                for triple in line['possible']:
                    p_rel = triple.split('|||')[1]
                    rel_set.add(p_rel)
    print(len(rel_set))
    print(count)


def read_triple_dict():
    data_path = get_data_path()
    file_triple = os.path.join(data_path, 'check_triple_cqa.all')
    # file_triple = os.path.join(data_path, 'check_triple_nlpcc.all')
    triple_dict = dict()
    with open(file_triple) as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            if not line['reliable'] and not line['possible']:
                continue
            if line['reliable']:
                triple_dict[line['triple']] = line['reliable']
            else:
                triple_dict[line['triple']] = line['possible']
    return triple_dict


def pre_question(text):
    while text[-1] == '?' or text[-1] == '？':
        text = text[:-1]
    return text


def gen_train_cqa(min_score):
    triple_dict = read_triple_dict()
    print('load %d triple dict succeed' % len(triple_dict))

    data_path = get_data_path()
    data_dir_path = os.path.join(data_path, 'gen_qa/cqa_triple_match')
    file_list = os.listdir(data_dir_path)
    file_path_list = []
    for f in file_list:
        file_path_list.append(os.path.join(data_dir_path, f))
    fout_path = os.path.join(data_path, ('qa_train/gen_qa_data_%s_v2' % min_score))
    fout = open(fout_path, 'wb')

    count = 0
    adict = dict()
    q_set = set()
    for file in file_path_list:
        with open(file) as fin:
            for line in fin:
                line = line.decode('utf-8').strip().split('\t')
                score = float(line[-1])
                if score <= min_score:
                    continue
                question = pre_question(line[0].strip())
                if question in q_set:
                    continue
                q_set.add(question)
                count += 1
                adict['question'] = question
                adict['triples'] = []

                triple = '|||'.join((line[2], line[3], line[4]))
                adict['origin_triple'] = triple
                if triple not in triple_dict.keys():
                    continue
                adict['triples'] = triple_dict[triple]
                print>>fout, json.dumps(adict, encoding='utf-8', ensure_ascii=False)
    print(count)
    print(len(q_set))


def gen_qa_nlpcc():
    triple_dict = read_triple_dict()
    print('load %d triple dict succeed' % len(triple_dict))
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'nlpcc_qa/ch.qatriple_all')

    fout_path = os.path.join(data_path, 'qa_train/nlpcc_qa_data')
    fout = open(fout_path, 'wb')

    with open(file_path) as fin:
        count = 1
        while True:
            line = fin.readline()
            if not line:
                break
            line = line.decode('utf-8').strip()
            if line.startswith(str(count)):
                question = line.split('\t')[1].strip()
                triple_list = []
                triple_set = set()
                new_line = fin.readline().decode('utf-8').strip()
                while new_line.strip():
                    triple = new_line.split('|||')
                    for i in range(len(triple)):
                        triple[i] = triple[i].strip()
                    triple[0] = del_brackets(triple[0])
                    triple_set.add('|||'.join(triple))
                    new_line = fin.readline().decode('utf-8').strip()
                for triple in triple_set:
                    # triple = u"高等数学|||出版社|||武汉大学出版社"
                    if triple in triple_dict.keys():
                        print(triple_dict[triple])
                        triple_list.extend(triple_dict[triple])
                if triple_list:
                    adict = dict()
                    adict['question'] = pre_question(question)
                    adict['triple'] = list(set(triple_list))
                    print>> fout, json.dumps(adict, encoding='utf-8', ensure_ascii=False)
                count += 1


def count_rel2(file_in_name, file_out_name):
    data_path = get_data_path()
    file_in = os.path.join(os.path.join(data_path, 'qa_train'), file_in_name)
    file_out = os.path.join(os.path.join(data_path, 'statistics'), file_out_name)
    rel_dict = dict()
    rel_set = set()
    with open(file_in) as fin:
        for line in fin:
            line_dict = json.loads(line.decode('utf-8').strip())
            triple_list = line_dict['triple']
            for triple in triple_list:
                rel = triple.split('|||')[1]
                rel_set.add(rel)
                if rel in rel_dict.keys():
                    rel_dict[rel] += 1
                else:
                    rel_dict[rel] = 1
    rel_dict = sorted(rel_dict.items(), key=lambda d: d[1], reverse=True)
    print(len(rel_set))
    fout = open(file_out, 'wb')
    for rel, count in rel_dict:
        print>>fout, ('%s : %d' % (rel, count)).encode('utf-8')


def merge_rel(rel_dict):
    data_path = get_data_path()
    rel_file = os.path.join(os.path.join(data_path, 'kb'), 'all_pro_map_labeled.json')
    with open(rel_file) as fin:
        rel_map_dict = json.load(fin, encoding='utf-8')
    print('load rel succeed!')
    # reversed_dict = {v: k for k, v in rel_map_dict.items()}
    # map_dict = rel_map_dict.copy()
    # map_dict.update(reversed_dict)
    new_rel_dict = dict()
    for rel, count in rel_dict.iteritems():
        if rel in rel_map_dict.keys():
            if rel_map_dict[rel] in rel_dict.keys():
                new_rel_dict[rel_map_dict[rel]] = rel_dict[rel_map_dict[rel]] + count
            else:
                new_rel_dict[rel_map_dict[rel]] = count
        else:
            new_rel_dict[rel] = count
    return new_rel_dict


if __name__ == '__main__':
    out_file_name_cqa = 'triple_cqa.all'
    out_file_name_nlpcc = 'triple_nlpcc.all'
    # get_triple(out_file_name_cqa)
    # get_triple_nlpcc(out_file_name_nlpcc)
    check_triple(out_file_name_nlpcc, 'check_triple_nlpcc.new')
    # count_rel('../data/check_triple_nlpcc.all')
    # gen_train_cqa(1.0)
    # gen_qa_nlpcc()
    # count_rel2('gen_qa_data_1.0', 'gen_qa.rel_count_1.0')
    # pass
