# -*- coding:utf-8 -*-
from jieba import posseg


def seg_word(sentence):
    seg_list = []
    pos_list = []
    for word, pos in posseg.cut(sentence):
        seg_list.append(word)
        pos_list.append(pos)
    return seg_list, pos_list


def ensure_unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    if isinstance(text, unicode):
        return text
    else:
        print('ensure_unicode error %s' % type(text))


if __name__ == '__main__':
    seg_list, pos_list = seg_word(u'姚明出生于哪里')

    print(' '.join(['/'.join((seg_list[i], pos_list[i]))for i in range(len(seg_list))]))