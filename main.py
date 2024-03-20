from packets import Packets
from node import Node
from topology import topology
import config
import simpy
import data

def main():
    env = simpy.Environment()
    top = topology("TREE")
    
    config.scheduling_method = "edf"
    nodes = top.simulate_network(env, config.cpu_mode)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))
    env.process(config.recordData(env, until_time=config.SIMULATION_TIME))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env.run(until = config.SIMULATION_TIME + 5000)

    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time[config.experimentID].append([(node, cpu.id), cpu.idle_time])

    print(f"cpu idle time: {data.cpu_idle_time}\n")
    print(f"packet count: {data.packetCount}\n")
    print(f"received count: {data.receivedCount}\n")
    print(f"meet deadline count: {data.meetDeadline}\n")
    print(f"satisfaction rate: {data.cal_satisfaction()}\n")
    print(f"processed count: {data.processedCount}\n")
    print(f"processed rate: {data.cal_processedRate()}\n")

    # data.plotLatency()
    # data.plotRemainingTime()

    print(f"processed rate: {data.processed_rate}\n")
    print(f"satisfaction rate: {data.satisfaction_rate}\n")

    # data.record.write(f"{data.failed}")
    needed = []
    for key, value in data.failed[0].items():
        if round(value[1], 5) - round(value[0], 5) < 40.00005:
            needed.append((key, value))  # Append both the key and value
    data.record.write(f"Packets I need: {needed}")
    print(len(needed))
    # data.plotProcessedRate()
    print(data.counter)
    # data.plotSatisfactionRate()


main()