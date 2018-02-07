# -*- coding:utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import json
from util import ensure_unicode, normalize_string, delete_source_prefix, get_data_url, parse_sentence
from util import get_top_entity
from ch_er.ner.get_entity_name import crf_segmenter
from predict_rel import decode_ques


def right_answer(test_ans, gold_ans_list):
    if test_ans in gold_ans_list:
        return True
    for gold_ans in gold_ans_list:
        if normalize_string(test_ans) in normalize_string(gold_ans) or normalize_string(gold_ans) in normalize_string(test_ans):
            return True
    return False


def answer_simple_qa(question, simple=True):
    if simple:
        ask_url = 'http://10.1.1.28:8000/api/graph/simple_qa/?q=' + ensure_unicode(question).encode('utf-8')
    else:
        ask_url = 'http://10.1.1.28:8000/api/graph/qa/?q=' + ensure_unicode(question).encode('utf-8')
    data = get_data_url(ask_url)
    if data == '\"No answer !\"':
        return None
    ans_dict = json.loads(data)
    ans_triples = []
    for k, v in ans_dict.iteritems():
        if k == 'triples':
            for triple in v:
                ans_triples.append([delete_source_prefix(triple[0]['name']), triple[1], delete_source_prefix(triple[2]['name'])])
    return ans_triples


def ner_ques(question):
    data = parse_sentence(question, ner=True)
    seg_list = data['seg']
    pos_list = data['pos']
    simple_ner_list = []
    if 'ner' in data.keys():
        simple_ner_list = data['ner']
    feature_list = []
    for i, word in enumerate(seg_list):
        feature_list.append('\t'.join((word, pos_list[i])).encode('utf-8'))
    ner_list = crf_segmenter(feature_list)
    return seg_list, ner_list, simple_ner_list


def get_pattern(ner_list, seg_list):
    tmp_pattern = ''
    entity_name = ''
    if not ner_list:
        return ''.join(seg_list), ''
    for i, tag in enumerate(ner_list):
        if tag == 'O':
            tmp_pattern += seg_list[i]
        elif tag == 'B':
            tmp_pattern += '_'
            entity_name += seg_list[i]
        elif tag == 'I':
            entity_name += seg_list[i]
    ques_pattern = '_'.join(tmp_pattern.split('_'))
    return ques_pattern, entity_name


def answer_seq2seq_qa(question):
    seg_list, ner_list, simple_ner_list = ner_ques(question)
    print('crf: ' + ' '.join(ner_list))
    print('simple: ' + ' '.join(simple_ner_list))
    ques_pattern, entity_name = get_pattern(ner_list, seg_list)
    if ques_pattern == question:
        ques_pattern, entity_name = get_pattern(simple_ner_list, seg_list)
    print('|'.join((ques_pattern, entity_name)))

    sub_entity_dict = get_top_entity(entity_name)
    if not sub_entity_dict:
        return None
    rel_score_list = decode_ques(ques_pattern, 20)
    test_rel = None
    for rel, rel_score in rel_score_list:
        if rel in sub_entity_dict.keys():
            test_rel = ensure_unicode(rel)
            break
    ans_triples = []
    if test_rel:
        ans_triples = [[sub_entity_dict['name'], test_rel, sub_entity_dict[test_rel]]]
    return ans_triples


def eval_qa():
    n = 0
    m1 = 0
    m2 = 0
    with open('test_data') as fin:
        for line in fin:
            line = line.decode('utf-8').strip().replace(' ', '')
            ques_dict = json.loads(line)
            n += 1
            print(n)
            # if n > 50:
            #     break
            question = ques_dict['question']
            triples = ques_dict['triple']
            gold_ans_list = []
            gold_rel_list = []
            for triple in triples:
                gold_ans_list.append(triple.split('|||')[2])
                gold_rel_list.append(triple.split('|||')[1])
            print('question: ' + question)
            print('gold_ans: ' + '|||'.join(gold_ans_list))

            print('simple_qa:')
            ans_triples = answer_simple_qa(question, simple=True)
            test_ans = None

            if ans_triples:
                test_ans = ans_triples[-1][-1]
                print('test_ans: ' + test_ans)
                for item in ans_triples:
                    print(' '.join(item))
            if test_ans:
                if right_answer(test_ans, gold_ans_list):
                    m1 += 1
                    print('simple right!')

            print('seq2seq_qa:')
            ans_triples = answer_seq2seq_qa(question)
            test_ans = None
            test_rel = None
            if ans_triples:
                test_ans = ans_triples[-1][-1]
                test_rel = ans_triples[-1][1]
                print('test_ans: ' + test_ans)
                for item in ans_triples:
                    print(' '.join(item))

            if test_ans:
                if right_answer(test_ans, gold_ans_list) or right_answer(test_rel, gold_rel_list):
                    m2 += 1
                    print('seq2seq right!')

            print('----------------------------------------')
            print(n)
            print(m1)
            print(m2)
        print('----------------------------------------')
        print(n)
        print(m1)
        print(m2)

if __name__ == '__main__':
    # ans = answer_seq2seq_qa(u'李小龙是哪里的人')
    # if ans:
    #     for item in ans:
    #         print(' '.join(item))
    # else:
    #     print('no answer')
    eval_qa()




