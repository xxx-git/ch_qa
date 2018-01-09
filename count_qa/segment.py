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


def format_large_number(number):
    number_str = str(number)
    if '.' in number_str:
        int_str, dec_str = number_str.split('.')
        dec_str = '.' + dec_str
    else:
        int_str = number_str
        dec_str = ''
    resversed_int_list = int_str[::-1]
    resversed_int_ret = ''
    for i in range(0, len(resversed_int_list), 3):
        resversed_int_ret += resversed_int_list[i:i+3] + ','
    if resversed_int_ret[-1] == ',':
        resversed_int_ret = resversed_int_ret[:-1]
    int_ret = ''.join(resversed_int_ret[::-1])
    return int_ret+dec_str


if __name__ == '__main__':
    # seg_list, pos_list = seg_word(u'姚明出生于哪里')
    # print(' '.join(['/'.join((seg_list[i], pos_list[i]))for i in range(len(seg_list))]))
    print(format_large_number(123456789.3422))