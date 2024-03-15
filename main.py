from packets import Packets
from node import Node
from topology import topology
import config
import simpy
import data

def main():
    env = simpy.Environment()
    top = topology("TREE")
    
    experimentID = 0
    config.scheduling_method = "optimal"
    nodes = top.simulate_network(env, config.cpu_mode, experimentID)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME, experimentID=experimentID))
    env.process(config.recordData(env, until_time=config.SIMULATION_TIME, experimentID=experimentID))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env.run(until = config.SIMULATION_TIME + 5000)

    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time[experimentID].append([node, cpu.idle_time])
    
    print(f"cpu idle time: {data.cpu_idle_time[experimentID]}")
    print(f"packet count: {data.packetCount[experimentID]}")
    print(f"received count: {data.receivedCount[experimentID]}")
    print(f"meet deadline count: {data.meetDeadline[experimentID]}")
    print(f"satisfaction rate: {data.cal_satisfaction()}")
    print(f"processed count: {data.processedCount[experimentID]}")
    print(f"processed rate: {data.cal_processedRate()}")


    env2 = simpy.Environment()
    experimentID = 1
    config.scheduling_method = "edf"
    nodes = top.simulate_network(env2, config.cpu_mode, 1)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env2.process(config.random_Senders(env2, nodes, config.SIMULATION_TIME, experimentID=1))
    env2.process(config.recordData(env2, until_time=config.SIMULATION_TIME, experimentID=1))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env2.run(until = config.SIMULATION_TIME + 5000)

    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time[1].append([node, cpu.idle_time])

    print(f"cpu idle time: {data.cpu_idle_time[experimentID]}")
    print(f"packet count: {data.packetCount[experimentID]}")
    print(f"received count: {data.receivedCount[experimentID]}")
    print(f"meet deadline count: {data.meetDeadline[experimentID]}")
    print(f"satisfaction rate: {data.cal_satisfaction()}")
    print(f"processed count: {data.processedCount[experimentID]}")
    print(f"processed rate: {data.cal_processedRate()}")


    env3 = simpy.Environment()
    experimentID = 2
    config.scheduling_method = "fifo"
    nodes = top.simulate_network(env3, config.cpu_mode, 2)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env3.process(config.random_Senders(env3, nodes, config.SIMULATION_TIME, experimentID=2))
    env3.process(config.recordData(env3, until_time=config.SIMULATION_TIME, experimentID=2))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env3.run(until = config.SIMULATION_TIME + 5000)
    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time[2].append([node, cpu.idle_time])

    print(f"cpu idle time: {data.cpu_idle_time[experimentID]}")
    print(f"packet count: {data.packetCount[experimentID]}")
    print(f"received count: {data.receivedCount[experimentID]}")
    print(f"meet deadline count: {data.meetDeadline[experimentID]}")
    print(f"satisfaction rate: {data.cal_satisfaction()}")
    print(f"processed count: {data.processedCount[experimentID]}")
    print(f"processed rate: {data.cal_processedRate()}")

    env4 = simpy.Environment()
    experimentID = 3
    config.scheduling_method = "probability"
    nodes = top.simulate_network(env4, config.cpu_mode, 3)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env4.process(config.random_Senders(env4, nodes, config.SIMULATION_TIME, experimentID=3))
    env4.process(config.recordData(env4, until_time=config.SIMULATION_TIME, experimentID=3))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env4.run(until = config.SIMULATION_TIME + 5000)
    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time[3].append([node, cpu.idle_time])

    print(f"cpu idle time: {data.cpu_idle_time[experimentID]}")
    print(f"packet count: {data.packetCount[experimentID]}")
    print(f"received count: {data.receivedCount[experimentID]}")
    print(f"meet deadline count: {data.meetDeadline[experimentID]}")
    print(f"satisfaction rate: {data.cal_satisfaction()}")
    print(f"processed count: {data.processedCount[experimentID]}")
    print(f"processed rate: {data.cal_processedRate()}")
    # print(config.NUMBER_OF_PROCESSORS)
    # print("")
    # zeros = []
    # for key, value in data.latencyList.items():
    #     if value == 0:
    #         zeros.append(key)

    # print(data.debug)
    # print(zeros)

    # print(data.latencyList)
    # print(data.failed)
    # top.drawing()
    #
    # print(len(data.packetSet))


    # data.plotLatency()
    # data.plotIdleTime()
    # data.plotProcessedRate()
    # data.plotSatisfactionRate()
main()