# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
reload(sys)
sys.setdefaultencoding('utf-8')
from global_path import get_data_path
import json
import random
import string
from utils import seg_sentence


def question_ner(question, sub_name):
    pattern = question.replace(sub_name, '_')
    return pattern.strip()


def is_filter_question(question):
    valid_char = filter(lambda c: c not in char_list, list(question))
    if valid_char:
        return False
    else:
        return True
char_list = list(string.punctuation) + list(u"？》《！。，")


def pre_question(text):
    while text[-1] in end_char_list:
        text = text[:-1]
    return text
end_char_list = list(u"?？，,.。")


def gen_seq2seq_train(file_name_list, dir_name, train=0.8):
    data_path = get_data_path()
    source_train_name = os.path.join(os.path.join(data_path, dir_name), 'question.train')
    target_train_name = os.path.join(os.path.join(data_path, dir_name), 'rel.train')
    source_dev_name = os.path.join(os.path.join(data_path, dir_name), 'question.dev')
    target_dev_name = os.path.join(os.path.join(data_path, dir_name), 'rel.dev')
    source_train_out = open(source_train_name, 'wb')
    target_train_out = open(target_train_name, 'wb')
    source_dev_out = open(source_dev_name, 'wb')
    target_dev_out = open(target_dev_name, 'wb')
    for file_name in file_name_list:
        data_file = os.path.join(os.path.join(data_path, 'qa_train'), file_name)
        with open(data_file) as fin:
            for line in fin:
                ll = json.loads(line.decode('utf-8').strip())
                question = ll['question']
                triple_list = []
                if 'triple' in ll.keys():
                    triple_list = ll['triple']
                elif 'triples' in ll.keys():
                    triple_list = ll['triples']
                else:
                    print(ll)
                # triple_list = ll['triple']
                rel_set = set()
                for triple in triple_list:
                    s, p, o = triple.split('|||')
                    pattern = question_ner(question, s.strip())
                    pattern = pre_question(pattern)
                    if is_filter_question(pattern):
                        continue
                    if p == 'subname' and len(triple_list) > 1:
                        continue
                    if p in rel_set:
                        continue
                    else:
                        rel_set.add(p)
                    num = random.random()
                    if num <= train:
                        print>>source_train_out, pattern.encode('utf-8')
                        print>>target_train_out, p.strip().encode('utf-8')
                    else:
                        print>>source_dev_out, pattern.encode('utf-8')
                        print>>target_dev_out, p.strip().encode('utf-8')


def count_ques_len():
    file_name_list = ['source.train']
    data_path = get_data_path()
    len_count = dict()
    for file_name in file_name_list:
        data_file = os.path.join(os.path.join(data_path, 'seq2seq_v1'), file_name)
        with open(data_file) as fin:
            for line in fin:
                ll = line.decode('utf-8').strip()
                seg_list = seg_sentence(ll)
                seg_len = len(seg_list)
                if seg_len in len_count.keys():
                    len_count[seg_len] += 1
                else:
                    len_count[seg_len] = 1
    print(len_count)


if __name__ == '__main__':
    # gen_seq2seq_train(['nlpcc_qa_data', 'gen_qa_data_1.0'], 'seq2seq_v1')
    # gen_seq2seq_train(['nlpcc_qa_data_v2', 'gen_qa_data_1.0_v2'], 'seq2seq_v2')
    gen_seq2seq_train(['nlpcc_qa_data_v4', 'gen_qa_data_1.0_v4'], 'seq2seq_v4')
    # count_ques_len()
