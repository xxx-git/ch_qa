#!/usr/bin/python
# -*- coding:utf-8 -*-


len_dict = {}
file_path = '../data/seq2seq_v4/question.dev'
with open(file_path, 'rb') as fin:
    for line in fin:
        ll = line.decode('utf-8').strip()
        len_dict[len(ll)] = len_dict.get(len(ll), 0) + 1
    ret = sorted(len_dict.items(), key=lambda x: x[0], reverse=True)
    print(ret)