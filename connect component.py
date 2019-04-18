import collections
from collections import deque
import os
import timeit
import gzip

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
    print('loading asqg file......')
    print('generate dictionary......')
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
    textFile = cwd + '/' + str(filename) + '-node.txt'
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
    for node in reads:
        visited.add(node)

    while connect_queue:
        pop_out = connect_queue.popleft()
        for item in node_dict[pop_out]:
            if item not in visited:
                connect_queue.append(item)
                visited.add(item)

    print('finding complete.')
    save_result(visited)
    print('save complete.')
    return


filename = 'test_new.gz'
samfile = 'test_new.sam'
time_start = timeit.default_timer()
get_connect_component();
time_end = timeit.default_timer()
print('total time is: '+ str(time_end - time_start) + 's')