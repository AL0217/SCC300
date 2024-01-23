import random
import data

# Settings of the network
NUMBER_OF_PROCESSORS = 4

# Option for enable multiple processes
MULTIPLE_PROCESS = True 

# enable fixed distance between nodes in the network
FIXED_DISTANCE = True
# the distance between each node
DISTANCE = 10

# time of processing a packet
PROCESS_TIME = 10

# Size of Data pushed to the network but what's the proper size to simulate?  Let's assume its fixed for now
DATA_SIZE_MAX = 100
DATA_SIZE_MIN = 10

# metrics of the simulations
DATA_COLLECTORS = [
    "PROCESSED_RATIO",  # Measure the ratio of processed packets
    "LATENCY",  # Measure request and response latency
    "LINK_LOAD",  # Measure link loads
    "PATH_STRETCH",  # Measure path stretch
]

# the scheduling method
# FCFS = First come first serve
SCHEDULING_METHOD = 'FCFS'


def random_Senders(env, nodes):
    while True:
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        env.process(sender_Node.request())
        data.packetCount += 1
        print(f"requested by {senderStr}")
        yield env.timeout(5)
