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
vcpu = Node("VCPU", name="vcpu", total=8)
tx.create(vcpu)
tx.create(Relationship(node, "PROVIDES", vcpu))
gb = Node("DISK_GB", name="disk", total=4000)
tx.create(node)
tx.create(Relationship(node, "PROVIDES", gb))
ram = Node("MEMORY_MB", name="ram", total=4096)
tx.create(ram)
tx.create(Relationship(node, "PROVIDES", ram))

consumer = Node("Consumer", name="Jay", pk=1)
tx.create(consumer)
tx.create(Relationship(consumer, "CONSUMES", vcpu, amount=2))
tx.create(Relationship(consumer, "CONSUMES", ram, amount=1024))
tx.create(Relationship(consumer, "CONSUMES", gb, amount=500))

consumer = Node("Consumer", name="Ed", pk=2)
tx.create(consumer)
tx.create(Relationship(consumer, "CONSUMES", vcpu, amount=1))
tx.create(Relationship(consumer, "CONSUMES", ram, amount=512))
tx.create(Relationship(consumer, "CONSUMES", gb, amount=250))

tx.commit()
