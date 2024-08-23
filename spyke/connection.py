
class Node:
    """
    Graph node. The parent of the neuron class.
    implement the connection logic.

    member variables:
    - self.connections: list[Connection], holds the connected outdirected node(end node) of the connection and the connection weight.
    - self.back_refs: list[ConnectionBackRef], holds the connected parent node(start node) of the connection and the connection itself.

    methods:
    - add_connection(self, weight: float, end_node: Node) -> Node, adds a connection to the node and also a backref to the connected node.
    """

    def __init__(self, connections: list['Connection'] = None, back_refs: list['ConnectionBackRef'] = None) -> None:
        self.connections = connections if connections is not None else []
        self.back_refs = back_refs if back_refs is not None else []

    def add_connection(self, connection: 'Connection') -> None:
        """
        Adds a connection to the node with the weight and adds a backref to the newly connected end_node.
        """
        self.connections.append(connection)
        self.connections[-1].end_node.back_refs.append(ConnectionBackRef(self, self.connections[-1]))


class Connection:
    """
    Connection implementation between two node.

    member variables:
    - self.weight: float
    - self.end_node: Node, the node(end_node, child node) that the connection is pointing at(directed connection).
    """
    
    def __init__(self, end_node: Node) -> None:

        if not isinstance(end_node, Node):
            raise ValueError('end_node should be a value of Node!')
        
        self.end_node: Node = end_node


class ConnectionBackRef:
    """
    ConnectionBackRef is a helping class for handling graph operations.
    Contains a reference of the parent node and the connection itself.

    members variables:
    - self.start_node: Node, is the parent(start_node) node of the connection.
    - self.connection: Connection, is the connection reference.
    """

    def __init__(self, start_node: Node, connection: Connection) -> None:

        if not isinstance(start_node, Node) or not isinstance(connection, Connection):
            raise ValueError('start_node should be a value of Node and connection should be a value of Connection!')
            
        self.start_node: Node = start_node
        self.connection: Connection = connection