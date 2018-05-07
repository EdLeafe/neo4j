from pprint import pprint
from utils import connect


# Get the connection to Node4j
g = connect()

# Query on multiple factors, with a small disk
query = """
MATCH (cnode:ComputeNode)-[*]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 4000
WITH cnode, ram
MATCH (cnode:ComputeNode)-[*]-(disk:DISK_GB)
WHERE disk.total - disk.used > 2000
RETURN cnode, disk, ram
"""
result = g.data(query)
node_disk = [(node["cnode"]["name"], node["disk"]["name"])
        for node in result]
print()
print("Requesting small disk; found %s" % len(result))
pprint(node_disk)

# Query on multiple factors, with a medium disk
query = """
MATCH (cnode:ComputeNode)-[*]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 4000
WITH cnode, ram
MATCH (cnode:ComputeNode)-[*]-(disk:DISK_GB)
WHERE disk.total - disk.used > 8000
RETURN cnode, disk, ram
"""
result = g.data(query)
node_disk = [(node["cnode"]["name"], node["disk"]["name"])
        for node in result]
print()
print("Requesting medium disk; found %s" % len(result))
pprint(node_disk)

# Now run the same query, but with a larger disk
query = """
MATCH (cnode:ComputeNode)-[*]->(ram:MEMORY_MB)
WHERE ram.total - ram.used > 4000
WITH cnode, ram
MATCH (cnode:ComputeNode)-[*]-(disk:DISK_GB)
WHERE disk.total - disk.used > 20000
RETURN cnode, disk, ram
"""
result = g.data(query)
node_disk = [(node["cnode"]["name"], node["disk"]["name"])
        for node in result]
print()
print("Requesting large disk; found %s" % len(result))
pprint(node_disk)
