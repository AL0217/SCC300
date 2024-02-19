import random
import data

# Settings of simulation
END_TIME = 300
SMALLEST_TOTAL_TIME = 30
CPU_MODE = 'equal'
SIMULATION_TIME = 30000

# Settings of the network
LEVEL_OF_TOPOLOGY = 3
TOTAL_NUMBER_OF_PROCESSORS = 24       #should be any reasonable number can be divided by 4
NUMBER_OF_PROCESSORS = 4
# int((TOTAL_NUMBER_OF_PROCESSORS / 2) / 2**(LEVEL_OF_TOPOLOGY-1))
SIZE_OF_QUEUE = 4
SEND_INTERVAL = 1

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

# the scheduling method
# FCFS = First In First Out
# EDF = Earliest Deadline First
SCHEDULING_METHOD = 'FIFO'


random.seed(1)

def random_Senders(env, nodes, until_time):
    while env.now <= until_time:
        sender = random.randint(1, 8)
        senderStr = "User" + str(sender)
        sender_Node = nodes[senderStr]
        env.process(sender_Node.request())
        data.packetCount += 1
        print(f"requested by {senderStr}")
        yield env.timeout(SEND_INTERVAL)

def gen_deadline(envNow):
    return envNow + random.randint(30,60)
