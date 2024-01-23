import simpy
import numpy as np
import networkx as nx
import random
from node import Node
from topology import topology
#Settings of the networl
NUMBER_OF_PROCESSORS = 4
STORAGE_CAPACITY = 100
DISTANCE = 10
#Variables Controlled
PROCESS_TIME = 10
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
nodes = ''
env.process(random_Senders(env, nodes))

env.run(until = 300)

print(f"packets sent: {packetCount}")
print(f"received: {receivedCount}")