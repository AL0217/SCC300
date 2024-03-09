import matplotlib.pyplot as plt

packetCount = 0
receivedCount = 0

processedCount = 0

meetDeadline = 0

packetList = {}
latencyList = {}
failed = {}
closeToDeadline = {}
packetSet = set()
cpu_set = []

record = open("record.txt", "w")


# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = unprocessedCount / receivedCount


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