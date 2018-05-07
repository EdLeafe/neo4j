from py2neo import Node, Relationship
from utils import connect
from utils import create_node

NODE_COUNT = 50

# Get the connection to Node4j
g = connect()
g.delete_all()

# Create the aggregates and shared disk providers.
tx = g.begin()
agg = Node("Aggregate", name="agg")
tx.create(agg)

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

# Create NODE_COUNT compute nodes with 2048 DISK_GB, 4096 MEMORY_MB, and 8
# VCPU. Each will also have 2PFs, one public and one private, and each PF will
# provide 8 VFs. We will also make each successive compute node have fewer and
# fewer resources available.
tx = g.begin()

for i in range(NODE_COUNT):
    ratio = i / NODE_COUNT
    cnode = create_node(tx, "ComputeNode", "cn", i)
    # Add the first node to the shared disk aggregate
    if i == 0:
        tx.create(Relationship(cnode, "MEMBER", agg))
    disk = create_node(tx, "DISK_GB", "disk", i, total=2048,
            used=int((2048*ratio)))
    tx.create(Relationship(cnode, "PROVIDES", disk))
    r = create_node(tx, "MEMORY_MB", "ram", i, total=4096,
            used=int((4096*ratio)))
    tx.create(Relationship(cnode, "PROVIDES", r))
    vcpu = create_node(tx, "VCPU", "vcpu", i, total=8, used=int((8*ratio)))
    tx.create(Relationship(cnode, "PROVIDES", vcpu))
    vf = create_node(tx, "VF", "vfpub", i, total=8, used=int((8*ratio)),
            network="public")
    tx.create(Relationship(cnode, "PROVIDES", vf))
    vf = create_node(tx, "VF", "vfpriv", i, total=8, used=int((8*ratio)),
            network="private")
    tx.create(Relationship(cnode, "PROVIDES", vf))
tx.commit()

# Create NODE_COUNT compute nodes, each with 2 NUMA nodes. The compute node
# will suppply 2048 DISK_GB; and each NUMA node will supply 2048 MEMORY_MB and
# 4 VCPU. Each NUMA node will also have 2PFs, one public and one private, and
# each PF will provide 8 VFs.
tx = g.begin()
for i in range(NODE_COUNT):
    ratio = i / NODE_COUNT
    cnode = create_node(tx, "ComputeNode", "cnNuma", i)
    # Add the first node to the shared disk aggregate
    if i == 0:
        tx.create(Relationship(cnode, "MEMBER", agg))
    disk = create_node(tx, "DISK_GB", "diskNuma", i, total=2048,
            used=int((2048*ratio)))
    tx.create(Relationship(cnode, "PROVIDES", disk))

    # NUMA node A
    for numaPrefix in ("A", "B"):
        numanode = create_node(tx, "NUMA", "numa%s" % numaPrefix, i)
        tx.create(Relationship(cnode, "CONTAINS", numanode))
        r = create_node(tx, "MEMORY_MB", "ramNuma%s" % numaPrefix, i,
                total=4096, used=int((4096*ratio)))
        tx.create(Relationship(numanode, "PROVIDES", r))
        vcpu = create_node(tx, "VCPU", "vcpuNuma%s" % numaPrefix, i, total=4,
                used=int((4*ratio)))
        tx.create(Relationship(numanode, "PROVIDES", vcpu))
        vf = create_node(tx, "VF", "vfprivNuma%s" % numaPrefix, i, total=8,
                used=int((8*ratio)), network="private")
        tx.create(Relationship(numanode, "PROVIDES", vf))
        vf = create_node(tx, "VF", "vfpubNuma%s" % numaPrefix, i, total=8,
                used=int((8*ratio)), network="public")
        tx.create(Relationship(numanode, "PROVIDES", vf))
tx.commit()
