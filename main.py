from packets import Packets
from node import Node
from topology import topology
import config
import simpy
import data

def main():
    env = simpy.Environment()
    top = topology()
    
    nodes = top.simulate_network(env, "TREE", config.CPU_MODE)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env.run(until = config.SIMULATION_TIME + 1000)

    print(f"packet count: {data.packetCount}")
    print(f"received count: {data.receivedCount}")
    print(f"meet deadline count: {data.meetDeadline}")
    print(f"processed count: {data.processedCount}")
    # print(config.NUMBER_OF_PROCESSORS)
    print("")
    zeros = []
    for key, value in data.latencyList.items():
        if value == 0:
            zeros.append(key)

    print(zeros)

    # print(data.latencyList)
    print(data.failed)
    # top.drawing()
    # data.plotLatency()
    print(len(data.packetSet))

main()