import matplotlib.pyplot as plt
import config
import numpy as np

packetCount = [0, 0, 0]
receivedCount = [0, 0, 0]

missed_at_node = [{}, {} ,{}]

processedCount = [0, 0, 0]

meetDeadline = [0, 0, 0]

packetList = [{}, {}, {}]

experiment_set = ["fifo", "edf", "optimal"]
# Metrics

# Latency of packet being processed
latencyList = [{}, {}, {}]

# The remaining deadline
closeToDeadline = [{}, {}, {}]
# CPU idle time
cpu_idle_time = [[], [], []]
cpu_id = [[], [], []]

# Satisfaction rate
satisfaction_rate = [[], [], []]

# processed rate
processed_rate = [[], [], []]

failed = [{}, {}, {}]

# debug = []
packetSet = [set(), set(), set()]

counter = 0

record = open("record.txt", "w")
# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = processedCount / receivedCount

def plotLatency():
    plt.figure(figsize=(8,6))
    x_values = experiment_set
    y_values = []

    for i in range(len(latencyList)):
        y_values.append(sum(latencyList[i].values())/packetCount[i])

    plt.bar(x_values, y_values)

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('Average Latency')
    plt.title('Average latency of packets')

    # Show the plot
    # plt.show()
    plt.savefig("experiment1/2/Latency_of_packets.png")

def plotRemainingTime():
    plt.figure(figsize=(8,6))
    x_values = experiment_set

    y_values = []

    for i in range(len(closeToDeadline)):
        y_values.append(sum(closeToDeadline[i].values())/(packetCount[i]))

    plt.bar(x_values, y_values)

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('average remaining deadlines')
    plt.title('Average remaining deadlines')

    # Show the plot
    # plt.show()
    plt.savefig("experiment1/2/Remaining_deadlines.png")

def cal_satisfaction():
    # Satisfaction rate (rate of meeting the deadline)
    return meetDeadline[config.experimentID] / packetCount[config.experimentID]

def cal_processedRate():
    # Processed rate - rate of being processed before cloud
    return processedCount[config.experimentID] / packetCount[config.experimentID]

def plotCPUidleTime():
    plt.figure(figsize=(10,6))
    for sublist in cpu_idle_time:
        # Iterate over each element in the sublist
        for i in range(len(sublist)):
            # Divide each element by the divider
            sublist[i] = sublist[i] * 100 / config.SIMULATION_TIME
    y_values = cpu_idle_time
    x = range(len(cpu_id[0]))
    width = 0.2

    plt.bar(cpu_id[0], y_values[0], width=width, label = "fifo")
    plt.bar([i + width for i in x], y_values[1], width=width, label = "edf")
    plt.bar([i + 2 * width for i in x], y_values[2], width=width, label = "optimal")
    # plt.bar([i + 3 * width for i in x], y_values[3], width=width, label = "prob")

    # Add labels and title
    plt.xlabel('cpu (Node - Cpu id)')
    plt.ylabel('Percentage cpu idle time')
    plt.title('CPU idle time')
    plt.legend()

    # Show the plot
    # plt.show()
    plt.savefig("experiment1/2/cpu_idle_time.png")

def plotSatisfactionRate():
    plt.figure(figsize=(8,6))
    x_values = np.arange(0, 601, 30)
    plt.plot(x_values, satisfaction_rate[2], label = "optimal", color = "black")
    plt.plot(x_values, satisfaction_rate[1], label = "edf", color = "blue")
    plt.plot(x_values, satisfaction_rate[0], label = "fifo", color = "red")
    # plt.plot(satisfaction_rate[3], label = "prob", color = "green")

    plt.xlabel('simulation time')
    plt.ylabel('satisfaction rate')
    plt.title('Satisfaction rate over 600 seconds time period')

    plt.legend()
    # plt.show()
    plt.savefig("experiment1/2/Satisfaction_rate" + experiment_set[config.experimentID] + ".png")

def plotProcessedRate():
    plt.figure(figsize=(8,6))
    x_values = np.arange(0, 601, 30)
    plt.plot(x_values, processed_rate[2], label = "optimal", color = "black")
    plt.plot(x_values, processed_rate[1], label = "edf", color = "blue")
    plt.plot(x_values, processed_rate[0], label = "fifo", color = "red")
    # plt.plot(processed_rate[3], label = "prob", color = "green")
        
    plt.xlabel('simulation time')
    plt.ylabel('processed rate')
    plt.title('processed rate over 600 seconds time period')
    plt.legend()
    # plt.show()
    plt.savefig("experiment1/2/ProcessRate" + experiment_set[config.experimentID] + ".png")