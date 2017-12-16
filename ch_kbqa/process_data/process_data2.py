# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
from global_path import get_data_path
# from vector_manager import get_similarity
import json
import re


def gen_check_rel():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'check_triple_nlpcc.new')
    file_out_path = os.path.join(data_path, 'check_triple_nlpcc.tmp')
    fout = open(file_out_path, 'wb')
    with open(file_path, 'rb') as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            triple = ll['triple']
            sub_name, rel, _ = triple.split('|||')
            reli_list = list(set(ll['reliable']))
            possi_list = list(set(ll['possible']))
            possi_rel_list = []
            if len(reli_list) > 0:
                reliable_rel = rel
                print>>fout, json.dumps({'triple': triple, 'rel': reliable_rel,
                                         'possi_rel_list': possi_rel_list},
                                        encoding='utf-8', ensure_ascii=False)
            elif len(possi_list) > 0:
                for item in possi_list:
                    item_rel = item.split('|||')[1]
                    possi_rel_list.append(item_rel)
                possi_rel_list = list(set(possi_rel_list))
                tmp_rel = ''
                if rel in possi_rel_list:
                    tmp_rel = rel
                print>>fout, json.dumps({'triple': triple, 'rel': tmp_rel,
                                         'possi_rel_list': possi_rel_list},
                                        encoding='utf-8', ensure_ascii=False)


def get_select_rel():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'check_triple_nlpcc.tmp')
    file_out_path = os.path.join(data_path, 'check_triple_nlpcc.tmp2')
    fout = open(file_out_path, 'wb')
    with open(file_path) as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            origin_rel = line['triple'].split('|||')[1]
            rel = line['rel']
            possi_rel_list = line['possi_rel_list']
            select_rel = ''
            if rel != '':
                select_rel = rel
            elif len(possi_rel_list) == 1:
                select_rel = possi_rel_list[0]
            elif len(possi_rel_list) > 1:
                print(line['triple'])
                max_sim = 0
                for possi_rel in possi_rel_list:
                    if possi_rel == 'subname':
                        continue
                    sim = get_similarity(possi_rel, origin_rel)
                    if sim > max_sim:
                        max_sim = sim
                        select_rel = possi_rel
            print>>fout, json.dumps({'triple': line['triple'], 'rel': rel, 'possi_rel_list': possi_rel_list,
                                     'select_rel': select_rel}, encoding='utf-8', ensure_ascii=False)


def gen_check_triple():
    data_path = get_data_path()
    triple_dict = read_rel_dict()
    file_path = os.path.join(data_path, 'check_triple_nlpcc.new')
    file_out_path = os.path.join(data_path, 'check_triple_nlpcc.select')
    fout = open(file_out_path, 'wb')
    with open(file_path, 'rb') as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            triple = ll['triple']
            sub_name, rel, _ = triple.split('|||')
            reli_list = list(set(ll['reliable']))
            if len(reli_list) > 0:
                print>>fout, json.dumps({'triple': triple, 'select_triple': reli_list},
                                        encoding='utf-8', ensure_ascii=False)
            else:
                possi_list = list(set(ll['possible']))
                possi_triple_list = []
                if triple not in triple_dict.keys():
                    print(triple)
                    continue
                select_rel = triple_dict[triple]
                for possi in possi_list:
                    _, rel, _ = possi.split('|||')
                    if rel == select_rel:
                        possi_triple_list.append(possi)
                print>>fout, json.dumps({'triple': triple, 'select_triple': possi_triple_list},
                                        encoding='utf-8', ensure_ascii=False)


def read_rel_dict():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'check_triple_nlpcc.tmp2')
    triple_dict = {}
    with open(file_path, 'rb') as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            select_rel = line['select_rel']
            if select_rel:
                triple_dict[line['triple']] = select_rel
    return triple_dict


def read_triple_dict():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'check_triple_nlpcc.select')
    triple_dict = {}
    with open(file_path, 'rb') as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            select_triple_list = line['select_triple']
            triple_dict[line['triple']] = select_triple_list
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


def del_brackets(name_str):
    match = bracket_pattern.match(name_str)
    if match:
        return match.group(1)
    return name_str
bracket_pattern = re.compile("(.*)(\(|\（).*(\)|\）)$")


def gen_qa_nlpcc():
    triple_dict = read_triple_dict()
    print('load %d triple dict succeed' % len(triple_dict))
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'nlpcc_qa/ch.qatriple_all')

    fout_path = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v2')
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
                    adict['origin_triple'] = list(triple_set)
                    print>> fout, json.dumps(adict, encoding='utf-8', ensure_ascii=False)
                count += 1


if __name__ == '__main__':
    # gen_check_rel()
    # get_select_rel()
    # gen_check_triple()
    # gen_train_cqa(1.0)
    gen_qa_nlpcc()

