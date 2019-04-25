from pprint import pprint
from utils import connect


# Get the connection to Node4j
g = connect()

#import pudb
#pudb.set_trace()

# Simple query
query = """
MATCH (cn:ComputeNode)-[:PROVIDES*0..1]->(nm)-[:PROVIDES]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 2000
RETURN cn, nm, ram
"""
result = g.run(query).data()
pprint(result)

# Query on multiple factors
query = """
MATCH p=(cnode:ComputeNode)-[*]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 4000
WITH p, cnode, ram
MATCH (cnode:ComputeNode)-[*]->(disk:DISK_GB)
WHERE disk.total - disk.used > 2000
RETURN p, cnode, disk, ram
"""
result = g.run(query)
pprint(result.data())
