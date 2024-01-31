import matplotlib.pyplot as plt

packetCount = 0
receivedCount = 0

processedCount = 0
unprocessedCount = 0

meetDeadline = 0

latencyList = []
# packetLossRate = (receivedCount / packetCount) * 100
# processedRate = unprocessedCount / receivedCount


def plotLatency():
    x_values = range(1, len(latencyList) + 1)
    plt.bar(x_values, latencyList)

    # Add labels and title
    plt.xlabel('Packets id')
    plt.ylabel('Latency')
    plt.title('Latency of packets')

    # Show the plot
    plt.show()