import os
import uuid

from py2neo import Graph, Node


def connect():
    """Connects to the Node4j server, using the environment variables if
    present, or 'localhost' if not.
    """
    host = os.getenv("NEO4J_HOST") or "localhost"
    password = os.getenv("NEO4J_PASSWORD") or "secret"
    return Graph(host=host, password=password)


def create_node(tx, typ, name_base, num=None, **kwargs):
    """Convenience method for creating a series of nodes with incrementing
    names and UUIDs.
    """
    if num is None:
        nm = name_base
    else:
        nm = "%s%s" % (name_base, ("%s" % num).zfill(4))
    u = "%s" % uuid.uuid4()
    new_node = Node(typ, name=nm, uuid=u, **kwargs)
    tx.create(new_node)
    return new_node
