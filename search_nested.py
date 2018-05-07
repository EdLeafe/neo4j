from pprint import pprint
from utils import connect


# Get the connection to Node4j
g = connect()

# Simple query
query = """
MATCH (cn:ComputeNode)-[]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 2000
RETURN cn, ram
"""
result = g.data(query)
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
result = g.data(query)
pprint(result)
