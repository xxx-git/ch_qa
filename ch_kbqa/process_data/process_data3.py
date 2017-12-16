# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
from global_path import get_data_path
import json
import re


def get_ques_set():
    data_path = get_data_path()
    fin_path = os.path.join(data_path, 'qa_train/test_data')
    question_set = set()
    with open(fin_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            question_set.add(ll['question'])
    return question_set


def del_eval_data():
    data_path = get_data_path()
    file1_in_path = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v3')
    file2_in_path = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v3')
    file1_out_path = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v4')
    fout1 = open(file1_out_path, 'wb')
    file2_out_path = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v4')
    fout2 = open(file2_out_path, 'wb')
    ques_set = get_ques_set()
    with open(file1_in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            if ll['question'] in ques_set:
                continue
            else:
                print>>fout1, json.dumps(ll, ensure_ascii=False, encoding='utf-8')
    with open(file2_in_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            if ll['question'] in ques_set:
                continue
            else:
                print>>fout2, json.dumps(ll, ensure_ascii=False, encoding='utf-8')


if __name__ == '__main__':
    del_eval_data()