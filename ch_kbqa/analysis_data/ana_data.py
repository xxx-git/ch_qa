# -*- coding:utf8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from global_path import get_data_path


def find_diff():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'seq2seq_v1/res.dev')
    question_dict = {}
    with open(file_path) as fin:
        for line in fin:
            ll = line.decode('utf-8').strip().split('|||')
            question = ll[0].strip()
            target_rel = ll[-1].strip()
            # if question in question_dict.keys():
            #     question_dict[question].add(target_rel)
            # else:
            #     question_dict[question] = set()
            #     question_dict[question].add(target_rel)
            temp_set = question_dict.get(question, set())
            temp_set.add(target_rel)
            question_dict[question] = temp_set
    file_out_path = os.path.join(data_path, 'statistics/same_question_rel')
    fout = open(file_out_path, 'wb')
    for ques, rel_set in question_dict.iteritems():
        print>>fout, json.dumps({'question': ques, 'rel_set': list(rel_set)}, encoding='utf-8', ensure_ascii=False)


def question_ner(question, sub_name):
    pattern = question.replace(sub_name, '_')
    return pattern.strip()


def read_ques():
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'statistics/diff_subject')
    question_dict = {}
    with open(file_path) as fin:
        for line in fin:
            ll = json.loads(line.decode('utf-8').strip())
            if ll['question'] in question_dict.keys():
                print(ll)
            else:
                question_dict[ll['question']] = ll['sub_name']
    return question_dict


def gen_train_data():
    file_list = ['gen_qa_data_1.0', 'nlpcc_qa_data']
    data_path = get_data_path()
    file_path = os.path.join(data_path, 'qa_train')

    file_out_path = os.path.join(file_path, 'all_qa_data')
    fout = open(file_out_path, 'wb')

    question_dict = read_ques()

    for f in file_list:
        file = os.path.join(file_path, f)
        with open(file) as fin:
            for line in fin:
                ll = json.loads(line.decode('utf-8').strip())
                question = ll['question'].strip()
                if question in question_dict.keys():
                    sub_name = question_dict[question]
                    triple_list = []
                    for triple in ll['triple']:
                        entity_name = triple.split('|||')[0].strip()
                        if entity_name == sub_name:
                            triple_list.append(triple)
                    if triple_list:
                        print>>fout, json.dumps({'question': question, 'triples': triple_list}, encoding='utf-8', ensure_ascii=False)
                else:
                    print>>fout, json.dumps({'question': question, 'triples': ll['triple']}, encoding='utf-8', ensure_ascii=False)


def find_diff_rel():
    data_path = get_data_path()
    file1 = os.path.join(data_path, 'qa_train/nlpcc_qa_data_v2')
    file2 = os.path.join(data_path, 'qa_train/gen_qa_data_1.0_v2')

    file_out_path = os.path.join(data_path, 'statistics/train_data.rel_dict')
    fout = open(file_out_path, 'wb')
    rel_dict = dict()
    for f in [file1, file2]:
        with open(f) as fin:
            for line in fin:
                print(line)
                ll = json.loads(line.decode('utf-8').strip())
                if 'triples' in ll.keys():
                    triple_list = ll['triples']
                elif 'triple' in ll.keys():
                    triple_list = ll['triple']
                if len(triple_list) <= 1:
                    continue
                rel_set = set()
                for triple in triple_list:
                    rel = triple.split('|||')[1]
                    rel_set.add(rel)
                for r in rel_set:
                    rel_dict[r] = rel_dict.get(r, 0) + 1
    rel_dict = sorted(rel_dict.items(), key=lambda x: x[1], reverse=True)
    all_count = 0
    for rel, count in rel_dict:
        all_count += count
        print>>fout, '\t'.join((rel, str(count))).encode('utf-8')
    print(all_count)



if __name__ == '__main__':
    find_diff_rel()
    pass
