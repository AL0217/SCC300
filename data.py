import matplotlib.pyplot as plt
import config

experimentID = 0

packetCount = [0,0,0,0]
receivedCount = [0,0,0,0]

processedCount = [0,0,0,0]

meetDeadline = [0,0,0,0]

packetList = [{}, {}, {}, {}]


# Metrics

# Latency of packet being processed
latencyList = [{}, {}, {}, {}]

# The remaining deadline
closeToDeadline = [{}, {}, {}, {}]

# CPU idle time
cpu_idle_time = [[], [], [], []]

# Satisfaction rate
satisfaction_rate = [[], [], [], []]

# processed rate
processed_rate = [[], [], [], []]

# failed = {}

# debug = []
packetSet = [set(), set(), set(), set()]

record = open("record.txt", "w")
# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = processedCount / receivedCount

def plotLatency():
    x_values = range(1, packetCount[experimentID]+1)
    plt.bar(x_values, list(latencyList[experimentID].values()))

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('Latency')
    plt.title('Latency of packets')
    # plt.grid(True)
    # plt.legend()
    # print(latencyList)

    # Show the plot
    plt.show()

def plotIdleTime():
    x_values = range(1, packetCount[experimentID] + 1)
    plt.bar(x_values, list(closeToDeadline[experimentID].values()))

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('deadline diff')
    plt.title('Remaining deadlines')
    # print(latencyList)

    # Show the plot
    plt.show()

def cal_satisfaction():
    # Satisfaction rate (rate of meeting the deadline)
    return meetDeadline[experimentID] / packetCount[experimentID]

def cal_processedRate():
    # Processed rate - rate of being processed before cloud
    return processedCount[experimentID] / packetCount[experimentID]

def plotSatisfactionRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.plot(satisfaction_rate[experimentID])

    plt.xlabel('simulation time')
    plt.ylabel('satisfaction rate')
    plt.title('Satisfaction rate over 300 seconds time period')

    plt.show()

def plotProcessedRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.plot(processed_rate[experimentID])

    plt.xlabel('simulation time')
    plt.ylabel('processed rate')
    plt.title('processed rate over 300 seconds time period')

    plt.show()