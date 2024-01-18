from concurrent.futures import process
from importlib import resources
from multiprocessing import cpu_count
from struct import pack
from urllib import response
import simpy
import numpy as np
import networkx as nx
import random

#Settings of the networl
NUMBER_OF_PROCESSORS = 4
STORAGE_CAPACITY = 100
DISTANCE = 10
#Variables Controlled
PROCESS_TIME = 15
TIME_BETWEEN_ARRIVALS = 10
#Size of Data pushed to the network but what's the proper size to simulate?  Let's assume its fixed for now
DATA_SIZE_MAX = 110
DATA_SIZE_MIN = 10

packetCount = 0
receivedCount = 0

#minimise the data im sending
#add a deadline and meet the deadline
#deadline parameters
#inferring how many packet passed

#i can assume i know the distance to the cloud

#each node is advertising 

class cpu:
    def __init__(self, env):
        self.next_available_time = 0
        self.env = env

    def checkBusy(self):
        if self.next_available_time > env.now:
            return True
        else:
            return False
    
    def process(self, packet):
        # set the cpu to busy
        self.next_available_time = env.now + packet.processTime

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)
        

class Node:
    def __init__(self, id, env, node):
        self.id = id

        self.cpu_num = NUMBER_OF_PROCESSORS
        self.cpuList= [cpu(env), cpu(env), cpu(env), cpu(env)]
        self.cpu_in_use = 0

        self.nextNode = node
        self.env = env

    def request(self):
        #create a packet that need to be send
        packet = Packets(destination=1)
        # Send the packet
        # simulate the time used to send the packet
        yield self.env.timeout(DISTANCE)
        print("Transmitted")

        yield from self.nextNode.receive(packet)

    def receive(self, packet):
        print(f"my id is: {self.id}")
        print("env now: " + str(env.now))

        # Check if the node is busy
        if(self.cpu_in_use >= self.cpu_num):
            for cpus in self.cpuList:
                print(cpus.next_available_time)
            if(self.id != "Cloud"):
                print("passed")
                
                # simulate the time used to send the packet
                yield self.env.timeout(DISTANCE)

                #call the receive function
                yield from self.nextNode.receive(packet)
            else:
                print("reached cloud")
            return

        # if the packet is not processed
        if(packet.processed):
            if(self.id != "Cloud"):
                print("passed processed packet")
                # simulate the time used to send the packet
                yield self.env.timeout(DISTANCE)

                #call the receive function
                yield from self.nextNode.receive(packet)
            else:
                print("processed packet reached cloud")
                global receivedCount
                receivedCount += 1
            return

        print("not processed")

        #init a opt_cpu variable
        opt_cpu = self.cpuList[0]

        #find an available cpu from the cpuList
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if not cpus.checkBusy():
                opt_cpu = cpus
                break
        
        # The distance here is the distance from last node
        self.cpu_in_use += 1
        yield from opt_cpu.process(packet)
        self.cpu_in_use -= 1
        packet.processed = True
        # the distance here is the DISTANCE to next node
        yield from self.nextNode.receive(packet)
        
        



#statistics of a packet
class Packets:
    def __init__(self, destination):
        self.processed = False
        self.processTime = PROCESS_TIME
        self.destination = destination


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
        global packetCount
        packetCount += 1
        print(f"requested by {senderStr}")
        yield env.timeout(5)



env = simpy.Environment()
nodes = simulate_network(env, graph())

env.process(random_Senders(env, nodes))


env.run(until = 300)

print(f"packets sent: {packetCount}")
print(f"received: {receivedCount}")