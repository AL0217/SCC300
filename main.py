from packets import Packets
from node import Node
from topology import topology
import config as c
import simpy
import data

def main():
    env = simpy.Environment()
    top = topology()
    
    nodes = top.simulate_network(env, "TREE")

    for node in nodes:
        env.process(nodes[node].handle_queue())

    # There will be 6 packets per process (in a settings of 5s send) not delivered to cloud because simulation end
    env.process(c.random_Senders(env, nodes))
    env.process(c.random_Senders(env, nodes))
    env.process(c.random_Senders(env, nodes))
    env.process(c.random_Senders(env, nodes))
    # env.process(c.random_Senders(env, nodes))
    # env.process(c.random_Senders(env, nodes))

    env.run(until = 300)

    print(f"packet count: {data.packetCount}")
    print(f"received count: {data.receivedCount}")
    print(f"meet deadline count: {data.meetDeadline}")
    print(f"processed count: {data.processedCount}")
    data.plotLatency()

main()