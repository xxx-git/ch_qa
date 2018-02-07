#!/usr/bin/env python
# -*-coding:utf-8-*-

# CRF Segmenter based character tagging:
# 4-tags for character tagging: B(Begin), E(End), M(Middle), S(Single)

import codecs
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import CRFPP
import global_path


def load_crf_model():
    project_path = global_path.get_project_path()
    crf_model_path = os.path.join(project_path, 'ch_er/data/model/model')
    tagger = CRFPP.Tagger("-m " + crf_model_path)
    return tagger
tagger = load_crf_model()


def crf_segmenter(feature_list):
    tagger.clear()
    for word in feature_list:
        tagger.add(word)
    tagger.parse()
    pred_list = []
    size = tagger.size()
    for i in range(0, size):
        pred_list.append(tagger.y2(i))
    # print(pred_list)
    return pred_list



if __name__ == '__main__':
    # crf_model = sys.argv[1]
    seg_list = [u'微软', u'的', u'院长', u'是', u'谁']
    pos_list = [u'a', u'uj', u'n', u'v', u'r']
    # crf_model = '../data/model/model'
    # seg_list = [u'微软']
    # pos_list = [u'a']
    feature_list = []
    for i, word in enumerate(seg_list):
        feature_list.append('\t'.join((word, pos_list[i])).encode('utf-8'))
    # tagger = CRFPP.Tagger("-m " + crf_model)
    print(crf_segmenter(feature_list))