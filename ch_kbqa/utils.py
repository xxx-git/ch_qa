import jieba


def ensure_unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    elif isinstance(text, unicode):
        return text
    else:
        print('ensure unicode error: %s' % type(text))


def seg_sentence(sentence):
    seg_list = []
    for word in jieba.cut(sentence):
        seg_list.append(word)
    return seg_list
