from packets import Packets
from node import Node
from topology import topology
import config
import simpy
import data
import random


experiment_set = ["fifo", "edf", "optimal"]
# FIFO data
for experiment in experiment_set:
    env = simpy.Environment()
    top = topology("TREE")  
    config.scheduling_method = experiment
    config.experimentID = experiment_set.index(experiment)
    random.seed(42)
    nodes = top.simulate_network(env, config.cpu_mode)

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))
    env.process(config.recordData(env, config.SIMULATION_TIME))
    # env.process(config.random_Senders(env, nodes, config.SIMULATION_TIME))

    env.run(until = config.SIMULATION_TIME + 20000)

    for node in nodes:
        if node[:4] == "User" or node == "Cloud":
            continue
        for cpu in nodes[node].cpuList:
            id = node[4] + "-" + str(cpu.id)
            data.cpu_idle_time[config.experimentID].append(cpu.idle_time)
            data.cpu_id[config.experimentID].append(id)

    print(f"cpu idle time: {data.cpu_idle_time[config.experimentID]}\n")
    print(f"packet count: {data.packetCount[config.experimentID]}\n")
    print(f"received count: {data.receivedCount[config.experimentID]}\n")
    print(f"meet deadline count: {data.meetDeadline[config.experimentID]}\n")
    print(f"satisfaction rate: {data.cal_satisfaction()}\n")
    print(f"processed count: {data.processedCount[config.experimentID]}\n")
    print(f"processed rate: {data.cal_processedRate()}\n")
    

for fail in data.failed:
    data.record.write(f"failed: {fail}\n")
print(data.missed_at_node)
data.plotCPUidleTime()
data.plotLatency()
data.plotProcessedRate()
data.plotRemainingTime()
data.plotSatisfactionRate()
