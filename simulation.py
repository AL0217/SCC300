from concurrent.futures import process
from importlib import resources
from struct import pack
from urllib import response
import simpy
import numpy as np

#Settings of the networl
NUM_OF_ENTITY_1 = 8     #1 user connect to each edge node
NUM_OF_ENTITY_2 = 16    #2 users connect to each edge node
HEIGHT_OF_TREE = 5
NUMBER_OF_PROCESSORS = 4
STORAGE_CAPACITY = 100
DISTANCE = 10
#Variables Controlled
MEAN_SERVICE_TIME = 90
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
        self.nextDistance = DISTANCE
        self.env = env

    def receive(self, packet, distance):            #how do I perform multi processes
        # Check if the node is busy
        print("env now: " + str(env.now))
        print("self.next_available_time: " + str(self.next_available_time))
        if(self.next_available_time >= env.now):
            self.nextNode.receive(packet, self.nextDistance)

        # If Not
        # set the node to busy
        print(self.id)
        self.next_available_time = self.env.now + packet.processTime

        # Send the packet
        # simulate the time used to send the packet
        yield self.env.timeout(distance)
        print("received the packet")

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)
        print("processed the packet")


#statistics of a packet
class Packets:
    def __init__(self, destination):
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
        print(env.now)
        yield from self.closestNode.receive(packet, self.distance)


def node(env):
    while True:
        print("push data")
        duration = 10
        yield env.timeout(duration)

        print("response")
        response_duration = 5
        yield env.timeout(response_duration)

env = simpy.Environment()

node1 = Node(1, env, None)
node2 = Node(2, env, None)

node1.nextNode = node2

user = Users(node1, env)

env.process(user.request())
env.process(user.request())

env.run(until = 200)