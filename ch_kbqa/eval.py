# -*- coding:utf-8 -*-


def eval_dev():
    target_rel_list = []
    file_target = '../data/seq2seq_v4/test_rel'
    with open(file_target) as fin:
        for line in fin:
            rel = line.decode('utf-8').strip()
            target_rel_list.append(rel)

    question_list = []
    res_rel_list = []
    file_res = '../data/seq2seq_v4/test_res'
    with open(file_res) as fin:
        for line in fin:
            question, rel, _ = line.decode('utf-8').strip().split('|||')
            res_rel_list.append(rel.strip())
            question_list.append(question.strip())

    if len(target_rel_list) != len(res_rel_list) or len(target_rel_list) != len(question_list):
        raise ValueError("1Lists must have the same length.")
    fout = open(file_res, 'wb')
    for i in range(len(question_list)):
        print>>fout, '|||'.join((question_list[i], res_rel_list[i], target_rel_list[i])).encode('utf-8')

    if len(target_rel_list) != len(res_rel_list):
        raise ValueError("2Lists must have the same length.")
    right = sum(x == y for x, y in zip(target_rel_list, res_rel_list))
    return right * 1.0 / len(target_rel_list)


def analysis_res():
    file_res = '../data/seq2seq_v4/test_res'
    right_rel_dict = dict()
    with open(file_res) as fin:
        for line in fin:
            question, res_rel, target_rel = line.decode('utf-8').strip().split('|||')
            if res_rel == target_rel:
                if target_rel in right_rel_dict.keys():
                    right_rel_dict[target_rel][0] += 1
                else:
                    right_rel_dict[target_rel] = [1, 0, []]
            else:
                if target_rel in right_rel_dict.keys():
                    right_rel_dict[target_rel][1] += 1
                    right_rel_dict[target_rel][2].append(res_rel)
                else:
                    right_rel_dict[target_rel] = [0, 1, [res_rel]]
    rel_dict = sorted(right_rel_dict.iteritems(), key=lambda x: x[1][0], reverse=True)
    file_out = '../data/seq2seq_v4/analysis_res'
    fout = open(file_out, 'wb')
    for rel, val in rel_dict:
        print>>fout, ('%s: (%d,%d) (%s)' % (rel, val[0], val[1], ','.join(list(set(val[2]))))).encode('utf-8')

if __name__ == '__main__':
    print('accuracy on test_ques: %f' % eval_dev())
    # analysis_res()
