# -*- coding:utf-8 -*-
import datetime
import sys
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
# reload(sys)
# sys.setdefaultencoding('utf-8')
import time
import json


def load_mini_kb():
    file_path = 'process_data/kb_mini'
    with open(file_path) as fin:
        kb_mini = json.load(fin, encoding='utf-8')
    print('load kb_mini succeed!')
    return kb_mini
kb_mini = load_mini_kb()


def load_tag_dict():
    # tag_dict = {}
    file_path = 'process_data/tag_rel_dict'
    with open(file_path) as fin:
        tag_dict = json.load(fin, encoding='utf-8')
    return tag_dict
tag_dict = load_tag_dict()


def tag_dict_format():
    ret_tag_dict = {}
    for tag_str, rel_dict in tag_dict.iteritems():
        tag_list = tag_str.split()
        for tag in tag_list:
            ret_tag_dict[tag] = tag_str
    return ret_tag_dict


def key_dict_format(key_dict):
    ret_key_dict = {}
    for key_str, _ in key_dict.iteritems():
        key_list = key_str.split()
        for key in key_list:
            ret_key_dict[key] = key_str
    return ret_key_dict


def rel_dict_format(tag_key):
    ret_rel_dict = {}
    rel_dict = tag_dict[tag_key]
    for rel_str, pred_list in rel_dict.iteritems():
        rel_list = rel_str.split()
        for rel in rel_list:
            ret_rel_dict[rel] = pred_list
    return ret_rel_dict


def search_triple_neo4j(sub, rel=None, obj=None):
    '''
    for every_edge in results:
        start_node_id = str(every_edge[0]['start'])
        pos = start_node_id.rindex('/')
        start_node = start_node_id[pos+1:]
        n1 = gdb.nodes.get(int(start_node))    ##start node
        rel_type = every_edge[0]['type']    ## edge
        n2 = gdb.nodes.get(be_replaced_node)  ###end node
        n1.relationships.create(rel_type, n2)
    '''
    del_rel_query = "match (a:Instance)-[r]->(b) where a.name='%s' return r" % sub
    # del_rel_query = "match (a:Instance) where a.name='%s' return a" % sub
    results = gdb.query(del_rel_query,  data_contents=True)
    ret_dict_list = []
    node_id_set = set()
    if not results:
        return ret_dict_list
    for edge in results.graph:
        start_node_id = edge['relationships'][0]['startNode']
        if start_node_id in node_id_set:
            continue
        node_id_set.add(start_node_id)
        for node in edge['nodes']:
            if node['id'] == start_node_id:
                search_node = node
                if search_node['properties']:
                    ret_dict_list.append(search_node['properties'])
    return ret_dict_list


def search_node_neo4j(sub):
    '''
    for every_edge in results:
        start_node_id = str(every_edge[0]['start'])
        pos = start_node_id.rindex('/')
        start_node = start_node_id[pos+1:]
        n1 = gdb.nodes.get(int(start_node))    ##start node
        rel_type = every_edge[0]['type']    ## edge
        n2 = gdb.nodes.get(be_replaced_node)  ###end node
        n1.relationships.create(rel_type, n2)
    '''
    del_rel_query = "match (a:Instance) where a.name='%s' return a" % sub
    results = gdb.query(del_rel_query,  data_contents=True)
    ret_node_list = []
    if not results:
        return ret_node_list
    for nodes in results.graph:
        nodes_list = nodes['nodes']
        if len(nodes_list) > 1:
            print('more than one node')
            print(len(nodes_list))
            print(nodes_list)
        node_dict = nodes_list[0]
        if node_dict['properties']:
            ret_node_list.append(node_dict['properties'])
    return ret_node_list


def search_node_keyid(entity_id):
    del_rel_query = "match (a:Instance) where a.keyId='%s' return a" % entity_id
    results = gdb.query(del_rel_query, data_contents=True)
    ret_node_list = []
    if not results:
        return ret_node_list
    for nodes in results.graph:
        nodes_list = nodes['nodes']
        if len(nodes_list) > 1:
            print('more than one node')
            print(len(nodes_list))
            print(nodes_list)
        node_dict = nodes_list[0]
        if node_dict['properties']:
            ret_node_list.append(node_dict['properties'])
    return ret_node_list


gdb = GraphDatabase("http://10.1.1.28:7474", username="neo4j", password="123456")
if __name__ == '__main__':
    # rel_dict_list = search_triple_neo4j(u"上海中心大厦", '', '')
    # print(len(rel_dict_list))
    # for rel_dict in rel_dict_list:
    #     for rel, val in rel_dict.iteritems():
    #         print("%s: %s" % (rel, val))

    # ret_node_list = search_node_neo4j(u"杨洋")
    # print(len(ret_node_list))
    # for node_dict in ret_node_list:
    #     for key, val in node_dict.iteritems():
    #         print('%s: %s' % (key, val))
    #     print('---------------')

    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    for i in range(10):
        ret_node_list = search_node_keyid(u"2322/5098092")
        localtime = time.asctime(time.localtime(time.time()))
        print(localtime)
    # print(len(ret_node_list))
    # for node_dict in ret_node_list:
    #     for key, val in node_dict.iteritems():
    #         print('%s: %s' % (key, val))
    #     print('---------------')