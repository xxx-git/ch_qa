# -*- coding:utf8 -*-

import vector_manager
import segment


ques = u'门票最贵的山'
# rel_list = [u'身高', u'体重', u'外文名', u'毕业院校', u'生肖',
#             u'籍贯', u'经纪公司', u'出生地', u'星座', u'民族',
#             u'粉丝', u'血型', u'中文名', u'单曲', u'代表作品',
#             u'主要成就', u'国籍', u'出生日期', u'职业']

rel_list = [u'适宜游玩季节', u'建议游玩时长', u'地理位置', u'开放时间', u'门票价格',
            u'最高海拔', u'英文名称', u'主权归属', u'别称', u'中文名称',
            u'著名景点', u'长度', u'宽度', u'所属山系']

seg_list, pos_list = segment.seg_word(ques)
# seg_list = [u'人口', u'比', u'多', u'多少']
# ques = '人口比多多少'
tag_key = seg_list[0]
rel_key = rel_list[0]
score_tag = 0
score_rel = 0

tag_list = [u'山', u'山峰', u'山脉', u'国家']

for word in seg_list:
    for tag in tag_list:
        score = vector_manager.get_similarity(word, tag)
        print(' '.join((word, tag, str(score))))
        if score > score_tag:
            score_tag = score
            tag_key = tag
print(' '.join((tag_key, str(score_tag))))


for word in seg_list:
    for rel in rel_list:
        score = vector_manager.get_similarity(word, rel)
        print(' '.join((word, rel, str(score))))
        if score > score_rel:
            score_rel = score
            rel_key = rel
print(' '.join((rel_key, str(score_rel))))


# text_vector = vector_manager.get_vector_by_list(seg_list)
#
# for rel in rel_list:
#     rel_vector = vector_manager.get_vector(rel)
#     score = vector_manager.get_similarity_vector(text_vector, rel_vector)
#     print(' '.join((rel, str(score))))
#     if score > score_key:
#         score_key = score
#         rel_key = rel
#
# print(rel_key)
# print(score_key)



