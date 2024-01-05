import networkx as nx
import matplotlib.pyplot as plt

# Create a simple graph (you can customize this based on your network topology)
G = nx.Graph()
G.add_nodes_from(['Cloud', 'Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6','User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8'])
G.add_edges_from([('Cloud', 'Node1'), ('Cloud', 'Node2'),
                  ('Node1', 'Node3'), ('Node1', 'Node4'),
                  ('Node2', 'Node5'), ('Node2', 'Node6'),
                  ('Node3', 'User1'), ('Node3', 'User2'),
                  ('Node4', 'User3'), ('Node4', 'User4'),
                  ('Node5', 'User5'), ('Node5', 'User6'),
                  ('Node6', 'User7'), ('Node6', 'User8'),])


# Visualize the network topology
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()