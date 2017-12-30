# -*- coding:utf-8 -*-
from pyltp import Parser
import segment


def init_parse_model():
    model_path = 'ltp_model/parser.model'
    parser = Parser()
    parser.load(model_path)
    return parser
parser = init_parse_model()


def parse_question(question):
    seg_list, pos_list = segment.seg_word(question)
    for i in range(len(seg_list)):
        seg_list[i] = segment.ensure_unicode(seg_list[i]).encode('utf-8')
    for i in range(len(pos_list)):
        pos_list[i] = segment.ensure_unicode(pos_list[i]).encode('utf-8')
    print(' '.join(seg_list))
    print(' '.join(pos_list))
    arcs = parser.parse(seg_list, pos_list)
    for i, arc in enumerate(arcs):
        print("%d: %d, %s" % (i, arc.head, arc.relation))


if __name__ == '__main__':
    parse_question(u'中国海拔最高的山是哪一座')

