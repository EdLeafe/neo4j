from py2neo import Node, Relationship
from utils import connect


# Get the connection to Node4j
g = connect()
g.delete_all()

# Start a transaction
tx = g.begin()

# Create a simple ComputeNode with its own DISK_GB
node = Node("ComputeNode", name="simple_node")
tx.create(node)
gb = Node("DISK_GB", name="local_disk", total=4000, used=0)
tx.create(node)
tx.create(Relationship(node, "PROVIDES", gb))
ram = Node("MEMORY_MB", name="local_ram", total=4096, used=0)
tx.create(ram)
tx.create(Relationship(node, "PROVIDES", ram))

# Create a couple of ComputeNodes that use shared disk
node1 = Node("ComputeNode", name="cn_shared1")
tx.create(node1)
ram1 = Node("MEMORY_MB", name="local_ram1", total=4096, used=0)
tx.create(ram1)
tx.create(Relationship(node1, "PROVIDES", ram1))
node2 = Node("ComputeNode", name="cn_shared2")
tx.create(node2)
ram2 = Node("MEMORY_MB", name="local_ram2", total=4096, used=0)
tx.create(ram2)
tx.create(Relationship(node2, "PROVIDES", ram2))

# Create an aggregate for all the compute nodes that share the disk
agg = Node("Aggregate", name="agg")
tx.create(agg)
# Add the compute nodes to the aggregate
tx.create(Relationship(node1, "MEMBER", agg))
tx.create(Relationship(node2, "MEMBER", agg))

# Create the shared providers and link them to the Aggregate
sd_small = Node("SharedDisk", name="sd_small")
tx.create(sd_small)
tx.create(Relationship(sd_small, "MEMBER", agg))
gb_small = Node("DISK_GB", name="gb_small", total=10000, used=0)
tx.create(gb_small)
tx.create(Relationship(sd_small, "PROVIDES", gb_small))

sd_big = Node("SharedDisk", name="sd_big")
tx.create(sd_big)
tx.create(Relationship(sd_big, "MEMBER", agg))
gb_big = Node("DISK_GB", name="gb_big", total=100000, used=0)
tx.create(gb_big)
tx.create(Relationship(sd_big, "PROVIDES", gb_big))

tx.commit()
