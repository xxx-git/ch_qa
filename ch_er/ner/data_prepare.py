#-*-coding:utf-8-*-
import jieba
import jieba.posseg as pseg
import json


def read_file(file_path):
    ques_list = []
    with open(file_path) as fin:
        for line in fin:
            line = json.loads(line.decode('utf-8').strip())
            ques_list.append(line)
    return ques_list


def gen_train_data(file_in_path, file_out_path):
    ques_list = read_file(file_in_path)
    fout = open(file_out_path, 'wb')
    for ques_dict in ques_list:
        question = ques_dict['question']
        # test_data
        triple = ques_dict['triple'][0]
        en_name = triple.split('|||')[0]

        # gen_qa_data_1.0_v4
        # origin_triple = ques_dict['origin_triple']
        # en_name = origin_triple.split('|||')[0]

        # nlpcc_qa_data_v4
        # origin_triple = ques_dict['origin_triple']
        # if len(origin_triple) == 1:
        #     en_name = origin_triple[0].split('|||')[0]
        # else:
        #     en_name = origin_triple[0].split('|||')[0]
        #     for item in origin_triple:
        #         tmp_name = item.split('|||')[0]
        #         if len(tmp_name) > en_name:
        #             en_name = tmp_name
        seg_list, pos_list, label_list = process_one(question, en_name)
        if seg_list and pos_list and label_list:
            for i, word in enumerate(seg_list):
                print>>fout, ' '.join((word, pos_list[i], label_list[i])).encode('utf-8')
            print>>fout


def process_one(question, en_name):
    seg_list = []
    pos_list = []
    label_list = []
    for word, pos in pseg.cut(question):
        seg_list.append(word)
        pos_list.append(pos)
        label_list.append('O')
    start_idx = -1
    end_idx = -1
    for i in range(len(seg_list)):
        if ''.join(seg_list[i:]).startswith(en_name):
            start_idx = i
            for j in range(i, len(seg_list)):
                if ''.join(seg_list[i:j]) == en_name:
                    end_idx = j
    if start_idx == -1:
        print('-----start = -1-----' + question)
    if end_idx == -1:
        print('-----end = -1-----' + question)
    for i in range(start_idx, end_idx):
        if i == start_idx:
            label_list[i] = 'B'
        else:
            label_list[i] = 'I'
    return seg_list, pos_list, label_list


def seg_sentence(sentence):
    for word, pos in pseg.cut(sentence):
        print('%s %s' % (word, pos))


if __name__ == '__main__':
    # gen_train_data('../data/nlpcc_qa_data_v4', '../data/train_data/train_v1')
    # gen_train_data('../data/gen_qa_data_1.0_v4', '../data/train_data/train_v2')
    # gen_train_data('../data/test_data', '../data/train_data/test_data')
    seg_sentence(u'微软的院长是谁')