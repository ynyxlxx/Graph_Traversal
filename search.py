import collections
from collections import deque
import os
import timeit
import gzip
import argparse

def sam_read(sam_file):    #read sequence ID from SAM file.
    print('loading sam file....')
    reads = []
    with open(sam_file) as f:
        for line in f:
            str_list = line.split()
            head = str_list[0]
            if '@' not in head[0]:
                reads.append(str_list[0])
    print('loading complete.')
    return reads

def graph_read(filename, dict):
    print('\n'+'loading asqg file......')
    print('generate edge dictionary......')
    with gzip.open(filename, 'rt') as file:
        string_line = (line.split() for line in file)
        edge_list = ((item[1], item[2]) for item in string_line)

        for edge in edge_list:
            dict[edge[0]].append(edge[1])
            dict[edge[1]].append(edge[0])
    print('generate complete.')
    return dict

def save_result(node_list):
    cwd = os.getcwd()
    textFile = cwd + '/result.txt'
    file = open(textFile, 'w+')
    for i in node_list:
        file.write(''.join(i) + "\n")
    file.close()
    return

def get_connect_component():     #BFS search

    reads = sam_read(samfile)
    node_dict = collections.defaultdict(list)
    node_dict = graph_read(filename, node_dict)
    connect_queue = deque()
    visited = set()

    connect_queue.extend(reads)   #set the start node

    initial_visited = set(reads).intersection(set(node_dict))      #filter out all the nodes that not in the graph

    for node in initial_visited:
        visited.add(node)

    print('start searching....')
    print('\n' + 'total number of start nodes: %i' % len(visited))
    while connect_queue:
        pop_out = connect_queue.popleft()
        for item in node_dict[pop_out]:
            if item not in visited:
                connect_queue.append(item)
                visited.add(item)
                print('number of nodes found now: %i' % len(visited))

    print('\n'+'searching complete.')
    print('result save complete.')
    print('please check the result.txt')
    return


parser = argparse.ArgumentParser(description='find all the connected component of the start node.')
parser.add_argument('graph_file', help = 'select the graph file')
parser.add_argument('sam_file',help = 'select the sam file as start node ')
args = parser.parse_args()

filename = args.graph_file
samfile = args.sam_file
time_start = timeit.default_timer()
get_connect_component()
time_end = timeit.default_timer()
print('duration: '+ str(time_end - time_start) + 's')