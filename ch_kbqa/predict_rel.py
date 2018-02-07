#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Predict Method for Testing
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

import numpy as np
from six.moves import xrange
import tensorflow as tf

import data_utils
from headline import LargeConfig
from utils import ensure_unicode

config = LargeConfig()  # new Large Config,
FLAGS = tf.app.flags.FLAGS  # Reuse the tf.app.flags from headline module

from headline import create_model
from headline import buckets

buckets = buckets


def initial_model(sess):
    model = create_model(sess, True)
    model.batch_size = FLAGS.batch_size
    src_vocab_path = os.path.join(FLAGS.data_dir, "question-vocab")
    dest_vocab_path = os.path.join(FLAGS.data_dir, "rel-vocab")
    src_vocab, _ = data_utils.initialize_vocabulary(src_vocab_path)
    _, dest_rev_vocab = data_utils.initialize_vocabulary(dest_vocab_path)
    return model, src_vocab, dest_rev_vocab


sess = tf.Session()
model, src_vocab, dest_rev_vocab = initial_model(sess)


def decode_ques(sentence, top_k=10):
    sentence = sentence.strip()
    if len(sentence) == 0:
        raise "invalid sentence"
    if len(sentence) > 31:
        sentence = sentence[:31]
        print('too long question!')
    token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), src_vocab,
                                                 tokenizer=data_utils.jieba_tokenizer)
    bucket_id = min([b for b in xrange(len(buckets)) if buckets[b][0] > len(token_ids)])
    encoder_inputs, decoder_inputs, target_weights = model.get_batch(
        {bucket_id: [(token_ids, [])]}, bucket_id)
    _, _, output_logits_batch = model.step(sess, encoder_inputs, decoder_inputs,
                                           target_weights, bucket_id, True)
    output_logits = []
    for item in output_logits_batch:
        output_logits.append(item[0])

    rel_score_list = []
    logit = output_logits[0]
    logit_length = len(logit)

    index_sort_list = list(reversed(np.argsort(logit)[(logit_length - top_k):logit_length]))
    for index in index_sort_list:
        rel = tf.compat.as_str(dest_rev_vocab[index])
        score = logit[index]
        rel_score_list.append((rel, score))
    # for rel, rel_score in rel_score_list:
    #     print("%s : %f" % (rel, rel_score))
    return rel_score_list


# def main(_):
#     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     for i in range(10):
#         sentence = u'_多大了'
#         decode_ques(sentence)
#         print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == "__main__":
    # tf.app.run()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for i in range(10):
        sentence = u'_多大了'
        decode_ques(sentence)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
