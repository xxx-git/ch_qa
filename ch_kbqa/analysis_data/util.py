# -*- coding:utf-8 -*-
import urllib2
import string
import json


def ensure_unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    if isinstance(text, unicode):
        return text
    else:
        print('ensure_unicode error %s' % type(text))


def normalize_string(str):
    str = str.lower()
    str = str.encode('utf-8').translate(None,string.punctuation)
    str = str.replace(' ', '')
    return str


def delete_source_prefix(str):
    if str.startswith('[ZHWIKI]'):
        str = str[len('[ZHWIKI]'):]
    if str.startswith('[HD]'):
        str = str[len('[HD]'):]
    return str


def get_data_url(url):
    try:
        return urllib2.urlopen(url).read()
    except Exception, e:
        print e


def parse_sentence(sentence, seg=True, pos=True, ner=False, el=False):
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


def get_top_entity(entity_name, all=False):
    entity_name = ensure_unicode(entity_name).encode('utf-8')
    if all:
        ask_url = 'http://10.1.1.28:8000/api/graph/entity/?name=%s' % entity_name
    else:
        ask_url = 'http://10.1.1.28:8000/api/graph/entity/?name=%s&autopick=true' % entity_name
    # print(get_data_url(ask_url))
    data = json.loads(get_data_url(ask_url))
    return data

if __name__ == '__main__':
    data = parse_sentence(u'电视剧使命的导演是谁&#39;', ner=True)
    for key, value in data.iteritems():
        print(key)
        print(value)