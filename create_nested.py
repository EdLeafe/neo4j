from py2neo import Relationship
from utils import connect
from utils import create_node

NODE_COUNT = 50

# Get the connection to Node4j
g = connect()
g.delete_all()

# Create NODE_COUNT compute nodes with 2048 DISK_GB, 4096 MEMORY_MB, and 8
# VCPU. Each will also have 2PFs, one public and one private, and each PF will
# provide 8 VFs. We will also make each successive compute node have fewer and
# fewer resources available.
tx = g.begin()

for i in range(NODE_COUNT):
    ratio = i / NODE_COUNT
    c = create_node(tx, "ComputeNode", "cn", i)
    d = create_node(tx, "DISK_GB", "disk", i, total=2048,
            used=int((2048*ratio)))
    tx.create(Relationship(c, "PROVIDES", d))
    r = create_node(tx, "MEMORY_MB", "ram", i, total=4096,
            used=int((4096*ratio)))
    tx.create(Relationship(c, "PROVIDES", r))
    v = create_node(tx, "VCPU", "vcpu", i, total=8, used=int((8*ratio)))
    tx.create(Relationship(c, "PROVIDES", v))
    v = create_node(tx, "VF", "vfpub", i, total=8, used=int((8*ratio)),
            network="public")
    tx.create(Relationship(c, "PROVIDES", v))
    v = create_node(tx, "VF", "vfpriv", i, total=8, used=int((8*ratio)),
            network="private")
    tx.create(Relationship(c, "PROVIDES", v))
tx.commit()

# Create NODE_COUNT compute nodes, each with 2 NUMA nodes. The compute node
# will suppply 2048 DISK_GB; and each NUMA node will supply 2048 MEMORY_MB and
# 4 VCPU. Each NUMA node will also have 2PFs, one public and one private, and
# each PF will provide 8 VFs.
tx = g.begin()
for i in range(NODE_COUNT):
    ratio = i / NODE_COUNT
    c = create_node(tx, "ComputeNode", "cnNuma", i)
    d = create_node(tx, "DISK_GB", "diskNuma", i, total=2048,
            used=int((2048*ratio)))
    tx.create(Relationship(c, "PROVIDES", d))

    # NUMA node A
    for numaPrefix in ("A", "B"):
        n = create_node(tx, "NUMA", "numa%s" % numaPrefix, i)
        tx.create(Relationship(c, "CONTAINS", n))
        r = create_node(tx, "MEMORY_MB", "ramNuma%s" % numaPrefix, i,
                total=4096, used=int((4096*ratio)))
        tx.create(Relationship(n, "PROVIDES", r))
        v = create_node(tx, "VCPU", "vcpuNuma%s" % numaPrefix, i, total=4,
                used=int((4*ratio)))
        tx.create(Relationship(n, "PROVIDES", v))
        v = create_node(tx, "VF", "vfprivNuma%s" % numaPrefix, i, total=8,
                used=int((8*ratio)), network="private")
        tx.create(Relationship(n, "PROVIDES", v))
        v = create_node(tx, "VF", "vfpubNuma%s" % numaPrefix, i, total=8,
                used=int((8*ratio)), network="public")
        tx.create(Relationship(n, "PROVIDES", v))
tx.commit()

#match (v:VF {name: "vfpub0008"}) set v.used=7 return v
#match p=(c:ComputeNode)-[*]-(v:VF network: "public") where v.total - v.used > 4 return p

#match (c:ComputeNode)-[*]->(v:VF) where v.total - v.used > 5
#with c
