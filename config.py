import random
import data

# Settings of simulation
CPU_MODE = 'high'
SIMULATION_TIME = 30000

# Settings of the network
LEVEL_OF_TOPOLOGY = 3
TOTAL_NUMBER_OF_PROCESSORS = 24       #should be any reasonable number can be divided by 4
EQUAL_PROCESSORS = 4
HIGH_LOW_PROCESSORS = int((TOTAL_NUMBER_OF_PROCESSORS / 2) / 2**(LEVEL_OF_TOPOLOGY-1))
SIZE_OF_QUEUE = 4
SEND_INTERVAL = 1

# Option for enable multiple processes
MULTIPLE_PROCESS = True 

# Rate of request in Request per millisecond
REQUEST_ARRIVAL_RATE = 2
LAMBDA = 1 / REQUEST_ARRIVAL_RATE

# enable fixed distance between nodes in the network
FIXED_DISTANCE = True

# the distance in m between each node
# distance in km
# propagation speed in km/s
DISTANCE = 10
PROPAGATION_SPEED = 1
# transmission speed in Mbps
TRANSMISSION_SPEED = 1000

# time of processing a packet
PROCESS_TIME = 10
PROCESS_SPEED = 100

# Size of Data pushed to the network but what's the proper size to simulate?  Let's assume its fixed for now
DATA_SIZE_MAX = 1000
DATA_SIZE_MIN = 1000

# the scheduling method
# fifo = First In First Out
# edf = Earliest Deadline First
# optimal = centralized scheduling
SCHEDULING_METHOD = 'optimal'

random.seed(1)

def random_Senders(env, nodes, until_time):
    while env.now <= until_time:
        arrival_rate = random.expovariate(REQUEST_ARRIVAL_RATE)
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        env.process(sender_Node.request())
        data.packetCount += 1
        print(f"requested by {senderStr}")
        yield env.timeout(arrival_rate)

def gen_deadline(envNow):
    return envNow + random.randint(30,60)

def gen_size():
    return random.randint(DATA_SIZE_MIN, DATA_SIZE_MAX)

def gen_target(nodes, weights):
    return random.choices(nodes, weights, k = 1)[0]
