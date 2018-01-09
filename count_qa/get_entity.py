# -*- coding:utf-8 -*-
import json
import urllib2
from segment import ensure_unicode


def get_data_url(url):
    try:
        return urllib2.urlopen(url).read()
    except Exception, e:
        print e


def parse_sentence(sentence, seg=True, pos=True, ner=True, el=False):
    sentence = ensure_unicode(sentence).encode('utf-8')
    ask_url = None
    if seg and pos and ner and el:
        ask_url = 'http://10.1.1.28:8000/api/nlp/parse/?content=%s&level=%s' % (sentence, '4')
    elif seg and pos and ner:
        ask_url = 'http://10.1.1.28:8000/api/nlp/parse/?content=%s&level=%s' % (sentence, '3')
    elif seg and pos:
        ask_url = 'http://10.1.1.28:8000/api/nlp/parse/?content=%s&level=%s' % (sentence, '2')
    elif seg:
        ask_url = 'http://10.1.1.28:8000/api/nlp/parse/?content=%s&level=%s' % (sentence, '1')
    else:
        print('seg, pos, ner, el the after depends on the previous one')
    data = json.loads(get_data_url(ask_url))
    # print(data)
    return data


def get_popular_entity(entity_name, all=False):
    entity_name = ensure_unicode(entity_name).encode('utf-8')
    if all:
        ask_url = 'http://10.1.1.28:8000/api/graph/entity/?name=%s' % entity_name
    else:
        ask_url = 'http://10.1.1.28:8000/api/graph/entity/?name=%s&autopick=true' % entity_name
    # print(get_data_url(ask_url))
    data = json.loads(get_data_url(ask_url))
    return data


def get_list_entity_by_tag(entity_tag):
    return [u'喜马拉雅山', u'乔戈里峰']


if __name__ == '__main__':
    data = get_popular_entity(u'珠穆朗玛峰')
    for key, value in data.iteritems():
        print('%s: %s' % (key, value))
    # print('-----------------------------------------------')
    # data = get_popular_entity(u'刘雯', True)
    # for item in data:
    #     for key, value in item.iteritems():
    #         print('%s: %s' % (key, value))
    # print('-----------------------------------------------')
    # data = parse_sentence(u'中国最高的楼')
    # for key, value in data.iteritems():
    #     print('%s: %s' % (key, ' '.join(value)))