from edge import Edge


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = []

    def add_edge(self, edge):
        self.edges[edge.source.id].append(edge)
        self.edges[edge.target.id].append(Edge(edge.target, edge.source, edge.weight, edge.tags))

    def get_neighbors(self, node_id):
        return self.edges[node_id]
