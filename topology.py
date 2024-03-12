import networkx as nx
import matplotlib.pyplot as plt
from node import Node
import random
import edf
import config


class topology:
    def __init__(self, graph_str):
        self.nodes = {}
        if graph_str == "TREE":
            self.graph = self.__Tree()

    # Create a simple graph (you can customize this based on your network topology)
    def __Tree(self):
        tree = nx.Graph()
        tree.add_nodes_from(['Cloud', 'Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6','User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8'])
        tree.add_edges_from([('Cloud', 'Node1'), ('Cloud', 'Node2'),
                        ('Node1', 'Node3'), ('Node1', 'Node4'),
                        ('Node2', 'Node5'), ('Node2', 'Node6'),
                        ('Node3', 'User1'), ('Node3', 'User2'),
                        ('Node4', 'User3'), ('Node4', 'User4'),
                        ('Node5', 'User5'), ('Node5', 'User6'),
                        ('Node6', 'User7'), ('Node6', 'User8'),])
        return tree
    


    def simulate_network(self, env, cpu_mode):
        scheduler_module = __import__(config.SCHEDULING_METHOD)
        node_class = getattr(scheduler_module, config.SCHEDULING_METHOD)
        match(cpu_mode):
            case "high":
                for node_id in self.graph.nodes:
                    if node_id == "Node1" or node_id == "Node2":
                        self.nodes[node_id] = node_class(node_id, env, None, config.HIGH_HIGHER_LEVEL, config.PROPAGATION_TIME, self)
                        continue
                    self.nodes[node_id] = node_class(node_id, env, None, config.HIGH_LOWER_LEVEL, config.PROPAGATION_TIME, self)
            case "low":
                for node_id in self.graph.nodes:
                    if not (node_id == "Node1" or node_id == "Node2"):
                        self.nodes[node_id] = node_class(node_id, env, None, config.LOW_LOWER_LEVEL, config.PROPAGATION_TIME, self)
                        continue
                    self.nodes[node_id] = node_class(node_id, env, None, config.LOW_HIGHER_LEVEL, config.PROPAGATION_TIME, self)
            case 'equal':
                for node_id in self.graph.nodes:
                    self.nodes[node_id] = node_class(node_id, env, None, config.EQUAL_PROCESSORS, config.PROPAGATION_TIME, self)

                # Establish relationships based on edges
        for edge in self.graph.edges:
            parent, child = edge
            parent_node = self.nodes[parent]
            child_node = self.nodes[child]
            child_node.node_set = nx.shortest_path(self.graph, source=child, target="Cloud", weight='weight')
            child_node.nextNode = parent_node
        return self.nodes

    def drawing(self):    
        # Visualize the network topology
        nx.draw(self.__Tree(), with_labels=True, font_weight='bold')
        plt.show()

    def get_node(self, id):
        return self.nodes[id]
    
    def get_distance(self, src, dst):
        return nx.shortest_path_length(self.graph, src, dst)