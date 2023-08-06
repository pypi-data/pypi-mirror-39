from graphviz import Digraph

def plot_computational_graph(node):
    graph = ADDigraph()
    graph.add_node_subgraph_to_plot_graph(node)
    graph.render()

class ADDigraph(Digraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.added_nodes = set()
        self.added_edges = set()
        self.graph_attr.update(rankdir="BT")

    @staticmethod
    def id_str(node):
        return str(node.id)

    @staticmethod
    def represent(node):
        if node.type == "Variable":
            return str(node.name)
        if node.type == "Constant":
            return str(node.value())
        return str(node.type)

    def add_node(self, node):
        super().node(ADDigraph.id_str(node),
                     label=ADDigraph.represent(node),
                     color=ADDigraph.get_color(node),
                     shape=ADDigraph.get_shape(node))
        self.added_nodes.add(ADDigraph.id_str(node))

    def add_edge(self, child, parent):
        self.edge(ADDigraph.id_str(child),
                  ADDigraph.id_str(parent),
                  **{"style": "filled"})
        self.added_edges.add((ADDigraph.id_str(child),
                  ADDigraph.id_str(parent)))

    @staticmethod
    def get_color(node):
        if node.type == "Variable" or node.type == "Constant":
            # better way to figure out the coloring?

            return "indianred1"
        else:
            return "lightblue"

    @staticmethod
    def get_shape(node):
        if node.type == "Variable" or node.type == "Constant":
            return "box"
        else:
            return "oval"

    def add_node_subgraph_to_plot_graph(self, top_node):
        if ADDigraph.id_str(top_node) not in self.added_nodes:
            self.add_node(top_node)

            # Add connections to children
            for child in top_node.children:
                self.add_edge(child, top_node)

            # Make each of the children do the same, but skip duplicates
            for child in set(top_node.children):
                self.add_node_subgraph_to_plot_graph(child)