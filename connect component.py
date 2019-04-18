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
def graph_read(filename):
    print('loading asqg file......')
    with gzip.open(filename, 'rt') as file:
        string_line = (line.split() for line in file)
        edge_list = ((item[1], item[2]) for item in string_line)

        for edge in edge_list:
            node_dict[edge[0]].append(edge[1])
            node_dict[edge[1]].append(edge[0])
    print('asgq file loaded.')
    return node_dict
def save_result(node_list):
    cwd = os.getcwd()
    textFile = cwd + '/ecoli-200.txt'
    file = open(textFile, 'w+')
    for i in node_list:
        file.write(''.join(i) + "\n")
    file.close()
    return

filename = 'E:/Direction study/E.coil/ed-ecoli-200.gz'
samfile = 'E:/Direction study/E.coil/ecoli2_and_lambda_mappedindex.sam'

time_start = timeit.default_timer()

reads = sam_read(samfile)
node_dict = collections.defaultdict(list)

node_dict = graph_read(filename)

connect_queue = deque()
visited = set()

connect_queue.extend(reads)

for node in reads:
    visited.add(node)

# print(visited)
# print(connect_queue)
# print(connect_queue[1])

# count = 1
while connect_queue:
    # print('iteration: ' + str(count))
    # count += 1
    pop_out = connect_queue.popleft()
    for item in node_dict[pop_out]:
        if item not in visited:
            connect_queue.append(item)
            visited.add(item)

print('finding complete.')
time_end = timeit.default_timer()
save_result(visited)
print('save complete.')
print('total time is: '+ str(time_end - time_start) + 's')