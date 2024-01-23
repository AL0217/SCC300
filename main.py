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
    env.process(c.random_Senders(env, nodes))
    
    env.run(until = 300)
    print(data.packetCount)
    print(data.receivedCount)

main()