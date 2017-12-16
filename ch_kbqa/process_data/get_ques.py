# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import random
from global_path import get_data_path


def read_train_data():
    data_path = get_data_path()
    file1 = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v2')
    file2 = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v2')
    rel_ques_dict = {}
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
                for triple in triple_list:
                    rel = triple.split('|||')[1]
                    if rel in rel_ques_dict.keys():
                        rel_ques_dict[rel].add(ques)
                    else:
                        rel_ques_dict[rel] = set()
                        rel_ques_dict[rel].add(ques)
    return rel_ques_dict


def get_ques():
    rel_ques_dict = read_train_data()
    while True:
        sys.stdout.write("> ")
        sys.stdout.flush()
        rel = sys.stdin.readline()
        rel = rel.decode('utf-8').strip()
        try:
            ques_list = list(rel_ques_dict[rel])
            ques_id = random.randint(0, len(ques_list) - 1)
            ques = ques_list[ques_id]
            print(ques)
        except KeyError:
            continue


if __name__ == '__main__':
    get_ques()