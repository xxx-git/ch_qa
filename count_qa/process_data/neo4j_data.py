# -*- coding:utf-8 -*-
import datetime
import sys
import codecs
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
# reload(sys)
# sys.setdefaultencoding('utf-8')


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


def search_node_neo4j(key_id):
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
    del_rel_query = "match (n:Instance) where n.keyId='%s' return n" % key_id
    results = gdb.query(del_rel_query,  data_contents=True)
    ret_node_dict = {}
    if not results:
        return ret_node_dict
    ret_node_dict = results.graph[0]['nodes'][0]['properties']
    # for nodes in results.graph:
    #     nodes_list = nodes['nodes']
    #     if len(nodes_list) > 1:
    #         print('more than one node')
    #         print(len(nodes_list))
    #         print(nodes_list)
    #     node_dict = nodes_list[0]
    #     if node_dict['properties']:
    #         ret_node_list.append(node_dict['properties'])
    return ret_node_dict

gdb = GraphDatabase("http://10.1.1.28:7474", username="neo4j", password="123456")
if __name__ == '__main__':
    # rel_dict_list = search_triple_neo4j(u"上海中心大厦", '', '')
    # print(len(rel_dict_list))
    # for rel_dict in rel_dict_list:
    #     for rel, val in rel_dict.iteritems():
    #         print("%s: %s" % (rel, val))

    # ret_node_list = search_node_neo4j(u"5333265")
    # print(len(ret_node_list))
    # for node_dict in ret_node_list:
    #     for key, val in node_dict.iteritems():
    #         print('%s: %s' % (key, val))
    #     print('---------------')

    ret_node_dict = search_node_neo4j(u"53342")
    print(ret_node_dict)
    for key, val in ret_node_dict.iteritems():
        print('%s: %s' % (key, val))