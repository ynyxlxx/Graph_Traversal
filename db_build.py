import sqlite3
import gzip
import argparse

def create_edge_database():
    c.execute('''DROP TABLE IF EXISTS edge_data''')
    c.execute('CREATE TABLE IF NOT EXISTS edge_data(keyword TEXT, neighbor TEXT)')
    c.execute('''PRAGMA synchronous = EXTRA''')
    c.execute('''PRAGMA journal_mode = WAL''')

def insert_edge_data(keyword, neighbor):
    c.executemany("INSERT INTO edge_data(keyword, neighbor) VALUES (?, ?)", [(keyword, neighbor)])

def read_edge_data():
    c.execute('SELECT * FROM edge_data')
    data = c.fetchall()
    for row in data:
        print(row)

parser = argparse.ArgumentParser(description='build a database for the graph.')
parser.add_argument('graph_file', help = 'select the graph file')
parser.add_argument('graph_database', help='select the database of the graph')
args = parser.parse_args()

filename = args.graph_file
database_name = args.graph_database

conn = sqlite3.connect(database_name)
c = conn.cursor()

create_edge_database()

print('building database......')
with gzip.open(filename, 'rt') as file:
    string_line = (line.split() for line in file)
    edge_list = ((item[1], item[2]) for item in string_line)
    count = 1
    for edges in edge_list:
        print('inserted records : %i ' % count)
        insert_edge_data(edges[0], edges[1])
        insert_edge_data(edges[1], edges[0])
        count += 1
    conn.commit()

c.execute("CREATE INDEX keyword_index ON edge_data (keyword)")
print('build complete.')

c.close()
conn.close()