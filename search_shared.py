from pprint import pprint
import uuid
from py2neo import Graph, Node, Relationship

from utils import connect
from utils import create_node


# Get the connection to Node4j
g = connect()

# With a small enough request, all compute nodes should be returned
query = """
    match (cnode:ComputeNode)-[*]-(gb:DISK_GB)
    where gb.total - gb.used > 2000
    return cnode, gb
"""
results = g.data(query)
print("With a small disk amount requested")
pprint([(result["cnode"], result["gb"]) for result in results])
print()

# Now request a bigger disk
query = """
    match (cnode:ComputeNode)-[*]-(gb:DISK_GB)
    where gb.total - gb.used > 8000
    return cnode, gb
"""
results = g.data(query)
print("With a medium-sized disk amount requested")
pprint([(result["cnode"], result["gb"]) for result in results])
print()

# This should only return the big shared disk
query = """
    match (cnode:ComputeNode)-[*]-(gb:DISK_GB)
    where gb.total - gb.used > 50000
    return cnode, gb
"""
results = g.data(query)
print("With a large disk amount requested")
pprint([(result["cnode"], result["gb"]) for result in results])
