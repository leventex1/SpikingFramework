from connection import Node, Connection, ConnectionBackRef


n1 = Node()
n2 = Node()

assert len(n1.connections) == 0
assert len(n1.back_refs) == 0

n1.add_connection(Connection(n2))

assert len(n1.connections) == 1
assert len(n1.back_refs) == 0

assert len(n2.connections) == 0
assert len(n2.back_refs) == 1

assert n1.connections[0].end_node == n2
assert n2.back_refs[0].start_node == n1
assert n2.back_refs[0].connection == n1.connections[0]
