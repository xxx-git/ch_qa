# -*- coding:utf8 -*-
import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append((os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from global_path import get_data_path
from segment import seg_word
import gensim
import numpy as np
# from numpy import linalg


def load_vectors():
    data_path = get_data_path()
    vector_path = os.path.join(data_path, 'vectors/vectors.bin')
    model = gensim.models.KeyedVectors.load_word2vec_format(vector_path, binary=True)
    # print('load vector model succeed! %d words' % len(model))
    return model
model = load_vectors()


def get_similarity(text1, text2):
    text_vector1 = get_vector(text1)
    text_vector2 = get_vector(text2)
    num = text_vector1.dot(text_vector2.T)
    demon = np.linalg.norm(text_vector1) * np.linalg.norm(text_vector2)
    return num / demon


def get_similarity_vector(vector1, vector2):
    num = vector1.dot(vector2.T)
    demon = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    return num / demon


def get_vector(text):
    word_list, _ = seg_word(text)
    text_vector = np.array([0.0] * 200)
    word_len = len(word_list)
    for i in range(word_len):
        try:
            text_vector += model[word_list[i]]
        except KeyError:
            word_len -= 1
            continue
    if word_len == 0:
        return text_vector
    text_vector /= word_len
    return text_vector


def get_vector_by_list(word_list):
    # word_list, _ = seg_word(text)
    text_vector = np.array([0.0] * 200)
    word_len = len(word_list)
    for i in range(word_len):
        try:
            text_vector += model[word_list[i]]
        except KeyError:
            word_len -= 1
            continue
    if word_len == 0:
        return text_vector
    text_vector /= word_len
    return text_vector


def get_max_similarity(seg_list, key_dict):
    ret_word = ''
    ret_value = None
    max_score = 0
    for word in seg_list:
        for key, value in key_dict.iteritems():
            score = get_similarity(key, word)
            if score > max_score:
                ret_word = word
                ret_value = value
                max_score = score
    return ret_word, ret_value, max_score


if __name__ == '__main__':
    # print(get_similarity(u'经营范围', u'经营产业'))
    # print(get_similarity(u'总部地点', u'经营产业'))
    print(get_similarity(u'占用认口', u'发行时间'))
    pass