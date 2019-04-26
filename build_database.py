import sqlite3
import gzip

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


filename = 'E:/Direction study/HIV/ed-phage-200.gz'

conn = sqlite3.connect('edge-phage-200.db')
c = conn.cursor()

create_edge_database()

print('building database......')
with gzip.open(filename, 'rt') as file:
    string_line = (line.split() for line in file)
    edge_list = ((item[1], item[2]) for item in string_line)
    for edges in edge_list:
        insert_edge_data(edges[0], edges[1])
        insert_edge_data(edges[1], edges[0])
    conn.commit()

c.execute("CREATE INDEX keyword_index ON edge_data (keyword)")
print('build complete.')

# read_edge_data()

c.close()
conn.close()