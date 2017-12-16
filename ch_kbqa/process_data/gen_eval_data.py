# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
from global_path import get_data_path


def read_train_data(file1=None, file2=None):
    data_path = get_data_path()
    file1 = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v2')
    file2 = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v2')
    rel_ques_dict = {}
    ques_triple_dict = {}
    for f in [file1, file2]:
        with open(f) as fin:
            for line in fin:
                ll = json.loads(line.decode('utf-8').strip())
                triple_list = []
                ques = ll['question']
                if 'triple' in ll.keys():
                    triple_list = ll['triple']
                elif 'triples' in ll.keys():
                    triple_list = ll['triples']
                # if ques in ques_triple_dict.keys():
                #     print(ques)
                ques_triple_dict[ques] = triple_list
    #             for triple in triple_list:
    #                 rel = triple.split('|||')[1]
    #                 if rel in rel_ques_dict.keys():
    #                     rel_ques_dict[rel].add(ques)
    #                 else:
    #                     rel_ques_dict[rel] = set()
    #                     rel_ques_dict[rel].add(ques)
    # return rel_ques_dict
    print('load succeed')
    return ques_triple_dict


def read_count_dict():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'statistics/train_data.rel_dict')
    count_dict = {}
    idx = 1
    with open(file_path) as fin:
        for line in fin:
            rel, count = line.decode('utf-8').strip().split('\t')
            count = int(count)
            for i in range(count):
                count_dict[idx] = rel
                idx += 1
    return count_dict


def gen_eval_data():
    num = 1000
    data_path = get_data_path()
    file1 = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v2')
    file2 = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v2')
    file_out_path = os.path.join(data_path, 'qa_train/test_data_tmp')
    fout = open(file_out_path, 'wb')
    rel_ques_dict = read_train_data(file1, file2)
    count_dict = read_count_dict()
    for i in range(num):
        idx = random.randint(1, 6594)
        rel = count_dict[idx]
        ques_list = list(rel_ques_dict[rel])
        ques_id = random.randint(0, len(ques_list)-1)
        ques = ques_list[ques_id]
        print>>fout, json.dumps({'question': ques, 'relation': rel}, encoding='utf-8', ensure_ascii=False)


def get_eval_data():
    data_path = get_data_path()
    file_in_path = os.path.join(data_path, 'qa_train/test_data_tmp')
    file_out_path = os.path.join(data_path, 'qa_train/test_data')
    fout = open(file_out_path, 'wb')
    ques_triple_dict = read_train_data()
    with open(file_in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            rel = ll['relation']
            ques = ll['question']
            if ques not in ques_triple_dict.keys():
                print(ques)
                continue
            triple_list = ques_triple_dict[ques]
            print>> fout, json.dumps({'question': ques, 'triple': triple_list},ensure_ascii=False, encoding='utf-8')


def rewrite_data():
    data_path = get_data_path()
    file_in_path = os.path.join(data_path, 'qa_train/test_data')
    fout1_path = os.path.join(data_path, 'seq2seq_v4/test_ques')
    fout2_path = os.path.join(data_path, 'seq2seq_v4/test_rel')
    fout1 = open(fout1_path, 'wb')
    fout2 = open(fout2_path, 'wb')
    with open(file_in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            triple_list = ll['triple']
            ques = ll['question']
            triple = triple_list[0]
            sub, rel, _ = triple.split('|||')
            ques_pattern = ques.replace(sub, '_')
            print>> fout1, ques_pattern.encode('utf-8')
            print>> fout2, rel.encode('utf-8')


def del_overlap():
    data_path = get_data_path()
    file_in_path = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v2')
    fout_path = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v3')
    fout = open(fout_path, 'wb')
    with open(file_in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            triple_list = ll['triples']
            name_list = set()
            for triple in triple_list:
                name, _, _ = triple.split('|||')
                name_list.add(name)
            name_list = list(name_list)
            if len(name_list) < 2:
                print>>fout, json.dumps(ll, encoding='utf-8', ensure_ascii=False)
            else:
                name_max = ''
                for name in name_list:
                    if len(name) > len(name_max):
                        if name_max in name:
                            name_max = name
                        else:
                            name_max = name
                            print(ll['question'])
                            print(ll['triples'])
                new_triple_list = []
                for triple in triple_list:
                    name, _, _ = triple.split('|||')
                    if name == name_max:
                        new_triple_list.append(triple)
                print>> fout, json.dumps({'origin_triple': ll['origin_triple'], 'question': ll['question'], 'triples': new_triple_list}, encoding='utf-8', ensure_ascii=False)


def count_rel():
    data_path = get_data_path()
    fin_path = os.path.join(data_path, 'qa_train/test_data')
    fout_path = os.path.join(data_path, 'statistics/test_rel')
    fout = open(fout_path, 'wb')
    # question_set = set()
    rel_dict = {}
    with open(fin_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            # question_set.add(ll['question'])
            triple_list = ll['triple']
            for triple in triple_list:
                _, rel, _ = triple.split('|||')
                rel_dict[rel] = rel_dict.get(rel, 0) + 1
    rel_dict = sorted(rel_dict.iteritems(), key=lambda x: x[1], reverse=True)
    for rel, count in rel_dict:
        print>>fout, '%s: %d' % (rel, count)


if __name__ == '__main__':
    rewrite_data()
