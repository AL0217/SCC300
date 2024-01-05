from concurrent.futures import process
from importlib import resources
from struct import pack
from urllib import response
import simpy
import numpy as np
import networkx as nx
import random

#Settings of the networl
NUM_OF_ENTITY_1 = 8     #1 user connect to each edge node
NUM_OF_ENTITY_2 = 16    #2 users connect to each edge node
HEIGHT_OF_TREE = 5
NUMBER_OF_PROCESSORS = 4
STORAGE_CAPACITY = 100
DISTANCE = 10
#Variables Controlled
MEAN_SERVICE_TIME = 50
MEAN_TIME_BETWEEN_ARRIVALS = 10
#Size of Data pushed to the network but what's the proper size to simulate?  Let's assume its fixed for now
DATA_SIZE_MAX = 110
DATA_SIZE_MIN = 10

#minimise the data im sending
#add a deadline and meet the deadline
#deadline parameters
#inferring how many packet passed

#i can assume i know the distance to the cloud

#each node is advertising 

class Node:
    def __init__(self, id, env, node):
        self.id = id
        self.next_available_time = 0
        self.cpu = NUMBER_OF_PROCESSORS
        self.storage = STORAGE_CAPACITY
        self.nextNode = node
        self.env = env

    def request(self):
        #create a packet that need to be send
        packet = Packets(destination=1)
        yield from self.nextNode.receive(packet, DISTANCE)

    def receive(self, packet, distance):            #how do I perform multi processes
        print(f"my id is: {self.id}")
        # Check if the node is busy
        print("env now: " + str(env.now))
        print("self.next_available_time: " + str(self.next_available_time))

        if(self.next_available_time > env.now):
            if(self.nextNode.id != "Cloud"):
                print("passed")
                yield from self.nextNode.receive(packet, DISTANCE)
            else:
                print("reached cloud")
            return

        if(packet.processed == True):
            if(self.nextNode.id != "Cloud"):
                print("passed processed packet")
                yield from self.nextNode.receive(packet, DISTANCE)
            else:
                print("processed packet reached cloud")
            return

        # If Not
        # set the node to busy
        self.next_available_time = env.now + packet.processTime

        # Send the packet
        # simulate the time used to send the packet
        yield self.env.timeout(distance)
        print(f"received the packet by node{self.id}")

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)
        print(f"processed the packet by node{self.id}")
        packet.processed = True




#statistics of a packet
class Packets:
    def __init__(self, destination):
        self.processed = False
        self.processTime = MEAN_SERVICE_TIME
        self.destination = destination


class Users:
    def __init__(self, node, env):
        self.closestNode = node
        self.distance = 10
        self.env = env

    def request(self):
        #create a packet that need to be send
        packet = Packets(destination=1)
        yield from self.closestNode.receive(packet, self.distance)


def node(env):
    while True:
        print("push data")
        duration = 10
        yield env.timeout(duration)

        print("response")
        response_duration = 5
        yield env.timeout(response_duration)

def graph():
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
    return G


def simulate_network(env, graph):
    nodes = {}

    # Create nodes based on their names
    for node_id in graph.nodes:
        nodes[node_id] = Node(node_id, env, None)

    # Establish relationships based on edges
    for edge in graph.edges:
        parent, child = edge
        parent_node = nodes[parent]
        child_node = nodes[child]

        child_node.nextNode = parent_node

    return nodes


def random_Senders(env, nodes):
    while True:
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        env.process(sender_Node.request())
        print(f"requested by {senderStr}")
        yield env.timeout(10)


env = simpy.Environment()
nodes = simulate_network(env, graph())
random_Senders(env, nodes)
env.run(until = 200)