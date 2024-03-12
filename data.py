import matplotlib.pyplot as plt
import config

packetCount = 0
receivedCount = 0

processedCount = 0

meetDeadline = 0

packetList = {}


# Metrics

# Latency of packet being processed
latencyList = {}

# The remaining deadline
closeToDeadline = {}

# CPU idle time
cpu_idle_time = []

# Satisfaction rate
satisfaction_rate = []

# processed rate
processed_rate = []

failed = {}

debug = []
packetSet = set()

record = open("record.txt", "w")
# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = processedCount / receivedCount

def plotLatency():
    x_values = range(1, packetCount + 1)
    plt.bar(x_values, list(latencyList.values()))

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('Latency')
    plt.title('Latency of packets')
    # print(latencyList)

    # Show the plot
    plt.show()

def plotIdleTime():
    x_values = range(1, packetCount + 1)
    plt.bar(x_values, list(closeToDeadline.values()))

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('deadline diff')
    plt.title('Remaining deadlines')
    # print(latencyList)

    # Show the plot
    plt.show()

def cal_satisfaction():
    # Satisfaction rate (rate of meeting the deadline)
    return meetDeadline / packetCount

def cal_processedRate():
    # Processed rate - rate of being processed before cloud
    return processedCount / packetCount

def plotSatisfactionRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.bar(x_values, satisfaction_rate)

    plt.xlabel('simulation time')
    plt.ylabel('satisfaction rate')
    plt.title('Satisfaction rate over 300 seconds time period')

    plt.show()

def plotProcessedRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.bar(x_values, processed_rate)

    plt.xlabel('simulation time')
    plt.ylabel('processed rate')
    plt.title('processed rate over 300 seconds time period')

    plt.show()