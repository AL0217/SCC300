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

# debug = []
packetSet = set()

record = open("record.txt", "w")
# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = processedCount / receivedCount

def plotLatency():
    x_values = range(1, packetCount+1)
    plt.bar(x_values, list(latencyList.values()))

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('Latency')
    plt.title('Latency of packets')
    # plt.grid(True)
    # plt.legend()
    # print(latencyList)

    # Show the plot
    plt.show()

def plotRemainingTime():
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
    # print(meetDeadline)
    # print(packetCount)
    return meetDeadline / packetCount

def cal_processedRate():
    # Processed rate - rate of being processed before cloud
    return processedCount / packetCount

def plotSatisfactionRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.plot(satisfaction_rate[0], label = "optimal", color = "black")
    plt.plot(satisfaction_rate[1], label = "edf", color = "blue")
    plt.plot(satisfaction_rate[2], label = "fifo", color = "red")
    plt.plot(satisfaction_rate[3], label = "prob", color = "green")

    plt.xlabel('simulation time')
    plt.ylabel('satisfaction rate')
    plt.title('Satisfaction rate over 300 seconds time period')

    plt.legend()
    plt.show()

def plotProcessedRate():
    x_values = range(0, config.SIMULATION_TIME, 50 * 1000)
    plt.plot(processed_rate[0], label = "optimal", color = "black")
    plt.plot(processed_rate[1], label = "edf", color = "blue")
    plt.plot(processed_rate[2], label = "fifo", color = "red")
    plt.plot(processed_rate[3], label = "prob", color = "green")
        
    

    plt.xlabel('simulation time')
    plt.ylabel('processed rate')
    plt.title('processed rate over 300 seconds time period')
    plt.legend()
    plt.show()