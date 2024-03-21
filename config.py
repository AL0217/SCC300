import random
import data
import config

# Settings of simulation
cpu_mode = 'equal'
# the scheduling method
# fifo = First In First Out
# edf = Earliest Deadline First
# optimal = centralized scheduling
scheduling_method = 'optimal'
experimentID = 0

SIMULATION_TIME = 600 * 1000

# Settings of the network
LEVEL_OF_TOPOLOGY = 3

EQUAL_PROCESSORS = 4

HIGH_HIGHER_LEVEL = 6
HIGH_LOWER_LEVEL = 3

LOW_LOWER_LEVEL = 5
LOW_HIGHER_LEVEL = 2

SIZE_OF_QUEUE = 4
SEND_INTERVAL = 1

# Option for enable multiple processes
MULTIPLE_PROCESS = True 

# Rate of request in Request per millisecond
REQUEST_ARRIVAL_RATE = 2
# LAMBDA = 1 / REQUEST_ARRIVAL_RATE

# enable fixed distance between nodes in the network
FIXED_DISTANCE = True

# the distance in m between each node
# propagation speed in ms
PROPAGATION_TIME = 10

# time of processing a packet
PROCESS_TIME = 10
PROCESS_SPEED = 100

# Size of Data pushed to the network but what's the proper size to simulate?  Let's assume its fixed for now
DATA_SIZE = 1000

random.seed(42)

def recordData(env, until_time):
    while env.now <= 600 * 100 :
        if env.now == 0:
            data.processed_rate[config.experimentID].append(0.0)
            data.satisfaction_rate[config.experimentID].append(0.0)
        else:
            data.processed_rate[config.experimentID].append(data.cal_processedRate())
            data.satisfaction_rate[config.experimentID].append(data.cal_satisfaction())
        yield env.timeout(30 * 100)


def random_Senders(env, nodes, until_time):
    while env.now <= until_time:
        send_time = random.expovariate(REQUEST_ARRIVAL_RATE)
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        data.packetCount[experimentID] += 1
        env.process(sender_Node.request())
        yield env.timeout(send_time)

def gen_deadline(envNow):
    return envNow + random.randint(100, 130)

