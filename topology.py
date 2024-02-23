import networkx as nx
import matplotlib.pyplot as plt
from node import Node
import random
import config as c


class topology:
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

    def simulate_network(self, env, graph_str, cpu_mode):
        nodes = {}
        if graph_str == "TREE":
            graph = self.__Tree()
            # Create nodes based on their names
            match(cpu_mode):
                case "high":
                    for node_id in graph.nodes:
                        if node_id == "Node1" or node_id == "Node2":
                            nodes[node_id] = Node(node_id, env, None, int(c.TOTAL_NUMBER_OF_PROCESSORS / 4), c.DISTANCE)
                            continue
                        nodes[node_id] = Node(node_id, env, None, int(c.HIGH_LOW_PROCESSORS), c.DISTANCE)
                case "low":
                    for node_id in graph.nodes:
                        if not (node_id == "Node1" or node_id == "Node2"):
                                nodes[node_id] = Node(node_id, env, None, 6, c.DISTANCE)
                                continue
                        nodes[node_id] = Node(node_id, env, None, 2, c.DISTANCE)
                case 'equal':
                    for node_id in graph.nodes:
                        nodes[node_id] = Node(node_id, env, None, int(c.EQUAL_PROCESSORS), c.DISTANCE)
                
            # Establish relationships based on edges
            for edge in graph.edges:
                parent, child = edge
                parent_node = nodes[parent]
                child_node = nodes[child]

                child_node.nextNode = parent_node

            return nodes
        return False

    def drawing(self):    
        # Visualize the network topology
        nx.draw(self.__Tree(), with_labels=True, font_weight='bold')
        plt.show()