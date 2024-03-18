import random
import data

# Settings of simulation
cpu_mode = 'equal'
# the scheduling method
# fifo = First In First Out
# edf = Earliest Deadline First
# optimal = centralized scheduling
scheduling_method = 'optimal'


SIMULATION_TIME = 3000

# Settings of the network
LEVEL_OF_TOPOLOGY = 3
TOTAL_NUMBER_OF_PROCESSORS = 24       #should be any reasonable number can be divided by 4
EQUAL_PROCESSORS = 4
HIGH_HIGHER_LEVEL = 80
HIGH_LOWER_LEVEL = 40

LOW_LOWER_LEVEL = 80
LOW_HIGHER_LEVEL = 40

SIZE_OF_QUEUE = 4
SEND_INTERVAL = 1

# Option for enable multiple processes
MULTIPLE_PROCESS = True 

# Rate of request in Request per millisecond
REQUEST_ARRIVAL_RATE = 3
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
DATA_SIZE_MAX = 1000
DATA_SIZE_MIN = 1000



random.seed(1)

def recordData(env, until_time):
    while env.now <= until_time + 500:
        if env.now == 0:
            data.processed_rate.append(0.0)
            data.satisfaction_rate.append(0.0)
        else:
            data.processed_rate.append(data.cal_processedRate())
            data.satisfaction_rate.append(data.cal_satisfaction())
        yield env.timeout(500)


def random_Senders(env, nodes, until_time):
    while env.now <= until_time:
        send_time = random.expovariate(REQUEST_ARRIVAL_RATE)
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        env.process(sender_Node.request())
        data.packetCount += 1
        # print(f"requested by {senderStr}")
        yield env.timeout(send_time)

def gen_deadline(envNow):
    return envNow + random.randint(30,60)

def gen_size():
    return random.randint(DATA_SIZE_MIN, DATA_SIZE_MAX)

def gen_target(nodes, weights):
    return random.choices(nodes, weights, k = 1)[0]
