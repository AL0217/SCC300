from packets import Packets
from node import Node
from topology import topology
import config
import simpy
import data

def main():
    env = simpy.Environment()
    top = topology("TREE")
    
    config.scheduling_method = "fifo"
    nodes = top.simulate_network(env, config.cpu_mode)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))
    env.process(config.recordData(env, until_time=config.SIMULATION_TIME))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env.run(until = config.SIMULATION_TIME + 5000)

    for node in nodes:
        for cpu in nodes[node].cpuList:
            data.cpu_idle_time.append([node, cpu.idle_time])
    
    data.record.write(f"cpu idle time: {data.cpu_idle_time}\n")
    data.record.write(f"packet count: {data.packetCount}\n")
    data.record.write(f"received count: {data.receivedCount}\n")
    data.record.write(f"meet deadline count: {data.meetDeadline}\n")
    data.record.write(f"satisfaction rate: {data.cal_satisfaction()}\n")
    data.record.write(f"processed count: {data.processedCount}\n")
    data.record.write(f"processed rate: {data.cal_processedRate()}\n")

    # data.plotLatency()
    # data.plotRemainingTime()

    data.record.write(f"{data.processed_rate}\n")
    data.record.write(f"{data.satisfaction_rate}\n")

    data.record.write(f"{data.failed}")
    # data.plotProcessedRate()
    # data.plotSatisfactionRate()


main()