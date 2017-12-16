# -*- coding:utf8 -*-

import vector_manager
import segment


# ques = u'比鹿晗高多少'
rel_list = [u'身高', u'体重', u'外文名', u'毕业院校', u'生肖',
            u'籍贯', u'经纪公司', u'出生地', u'星座', u'民族',
            u'粉丝', u'血型', u'中文名', u'单曲', u'代表作品',
            u'主要成就', u'国籍', u'出生日期', u'职业']

# seg_list, pos_list = segment.seg_word(ques)
seg_list = [u'人口', u'比', u'多', u'多少']
# ques = '人口比多多少'
word_key = seg_list[0]
rel_key = rel_list[0]
score_key = 0

text_vector = vector_manager.get_vector_by_list(seg_list)

for rel in rel_list:
    rel_vector = vector_manager.get_vector(rel)
    score = vector_manager.get_similarity_vector(text_vector, rel_vector)
    print(' '.join((rel, str(score))))
    if score > score_key:
        score_key = score
        rel_key = rel

print(rel_key)
print(score_key)



