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
        elif graph_str == "DEP_TREE":
            self.graph = self.__depthTree()
        elif graph_str == "kArr_TREE":
            self.garph = ""

    # Create a simple graph (you can customize this based on your network topology)
    def __Tree(self):
        tree = nx.Graph()
        tree.add_nodes_from(['Cloud', 
                             'Node1', 'Node2', 
                             'Node3', 'Node4', 'Node5', 'Node6',
                             'User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8'])
        
        tree.add_edges_from([('Cloud', 'Node1'), ('Cloud', 'Node2'),
                            ('Node1', 'Node3'), ('Node1', 'Node4'),
                            ('Node2', 'Node5'), ('Node2', 'Node6'),
                            ('Node3', 'User1'), ('Node3', 'User2'),
                            ('Node4', 'User3'), ('Node4', 'User4'),
                            ('Node5', 'User5'), ('Node5', 'User6'),
                            ('Node6', 'User7'), ('Node6', 'User8'),])
        return tree
    
    def __depthTree(self):
        tree = nx.Graph()
        tree.add_nodes_from(['Cloud', 
                             'Node1', 'Node2', 
                             'Node3', 'Node4', 'Node5', 'Node6',
                             'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Node12', 'Node13', 'Node14'
                             'Node15', 'Node16', "Node17", "Node18", "Node19", "Node20", "Node21", "Node22", "Node23", "Node24", "Node25", "Node26", "Node27", "Node28", "Node29", "Node30"
                             'User1', 'User2', "User3", "User4", "User5", "User6", "User7", "User8", "User9", "User10", "User11", "User12", "User13", "User14", "User15", "User16"])
        
        tree.add_edges_from([('Cloud', 'Node1'), ('Cloud', 'Node2'),
                            ('Node1', 'Node3'), ('Node1', 'Node4'), ('Node2', 'Node5'), ('Node2', 'Node6'),
                            ('Node3', 'Node7'), ('Node3', 'Node8'), ('Node4', 'Node9'), ('Node4', 'Node10'), ('Node5', 'Node11'), ('Node5', 'Node12'), ('Node6', 'Node13'), ('Node6', 'Node14'),
                            ('Node7', 'Node15'), ('Node7', 'Node16'), ('Node8', 'Node17'), ('Node8', 'Node18'), ('Node9', 'Node19'), ('Node9', 'Node20'), ('Node10', 'Node21'), ('Node10', 'Node22'),
                            ('Node11', 'Node23'), ('Node11', 'Node24'), ('Node12', 'Node25'), ('Node12', 'Node26'), ('Node13', 'Node27'), ('Node13', 'Node28'), ('Node14', 'Node29'), ('Node14', 'Node30'),])

        return tree
    
    def kArrTree(self):
        tree = nx.Graph()
        node_set = ['Cloud']
        count = 1
        for i in range(3):
            for j in range(3**(i+1)):
                node_name = "Node" + str(count)
                count += 1
                node_set.append(node_name)

        for i in range(1, 28):
            user = "User"+ str(i)
            node_set.append
        tree.add_nodes_from(node_set)

        conn = [('Cloud', 'Node1'), ('Cloud', 'Node2'), ('Cloud', 'Node3')]
        tree.add_edges_from(conn)

        for i in range(1, 3 ** 3 + 1):
            parent = f"Node{i}"
            children = [f"Node{j+3}" for j in range(i * 3 - 3 + 1, i * 3 + 1) if j <= 3 ** 3 + 3 ** 2]
            tree.add_edges_from([(parent, child) for child in children])

        return tree


    def simulate_network(self, env, cpu_mode):
        scheduler_module = __import__(config.scheduling_method)
        node_class = getattr(scheduler_module, config.scheduling_method)
        match(cpu_mode):
            case "high":
                for node_id in self.graph.nodes:
                    if node_id == "Node1" or node_id == "Node2":
                        self.nodes[node_id] = node_class(node_id, env, None, config.HIGH_HIGHER_LEVEL, 100, self)
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
    
    def simulate_network(self, env, cpu_mode):
        scheduler_module = __import__(config.scheduling_method)
        node_class = getattr(scheduler_module, config.scheduling_method)
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
                    distance = config.PROPAGATION_TIME
                    if node_id == "Node1" or node_id == "Node2":
                        distance = 100
                    self.nodes[node_id] = node_class(node_id, env, None, config.EQUAL_PROCESSORS, distance, self)

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
    
top = topology("TREE")
top.kArrTree()