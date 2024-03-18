from node import Node
import data
import config
from packets import Packets
import random

class probability (Node):
    def __init__(self, id, env, nextNode, num_processor, distance, topology):
        super().__init__(id, env, nextNode, num_processor, distance, topology)

    def scheduling(self):
        weights = []
        nodes = self.node_set[-2:0:-1]
    
        for node in nodes:
            weights.append(self.topology.get_node(node).cpu_num)

        # print(nodes)
        # print(weights)
        assignment = config.gen_target(nodes, weights)
        # print(assignment)
        return assignment




    def request(self):
        # create a packet that need to be send
        gen_deadline = config.gen_deadline(self.env.now)
        packet = Packets(destination=1, processTime=config.PROCESS_TIME, sendTime=self.env.now, deadline = gen_deadline)

        # loop start from the highest node, if the current time + propogation time + process time can meet the deadline
        # set the node to the destination
        # for item in self.node_set[-2::-1]:
        #     print(item)
        packet.destination = self.scheduling()

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        # data.record.write(f"packet id: {packet.packetID}\n")
        # data.record.write(f"time now: {self.env.now}\n")
        # Send the packet
        yield from self.nextNode.receive(packet)


    def receive(self, packet):
        # simulate the time used to send the packet
        yield self.env.timeout(self.distance_to_nextNode)

        # print the info of the packet and the node
        # data.record.write("Transmitted\n")
        # data.record.write(f"my id is: {self.id}\n")
        # data.record.write(f"packet id: {packet.packetID}\n")
        # data.record.write(f"propagationTime : {propagationTime}\n")
        # data.record.write(f"transmission time: {transmissionTime}\n")
        # data.record.write(f"env now: {self.env.now}\n")

        # if this node is cloud
        if self.id == "Cloud":
            yield from self.cloudReceive(packet)
            return
        
        #######-----IF THIS NODE IS NOT THE CLOUD-----######
        # if this is not the assigned node
        if self.id != packet.destination:
            # data.record.write("I am passing it")
            self.env.process(self.nextNode.receive(packet))
            return

        # if the packet processed
        if(packet.processed):
            # data.record.write("passed processed packet\n")

            # pass it directly
            #call the receive function of the next node
            self.env.process(self.nextNode.receive(packet))
            return
        

        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            # print the states of the cpus
            # data.record.write(f"packet waiting: {packet.packetID}\n")
            # data.record.write(f"cpu_in_use: {self.cpu_in_use}\n")
            # for cpus in self.cpuList:
            #     data.record.write(str(cpus.next_available_time) + "\n")

            self.queue.append(packet)
            # data.record.write(f"packet added to queue: {packet.packetID}\n")
            # for packet in self.queue:
                # data.record.write(f"this is queue: {packet}\n")
            self.queue.sort(key = lambda p: p.deadline)
            return
        
        # if the packet is admitted and the node is free to process it
        # data.record.write("not processed\n")
        opt_cpu = self.cpuList[0]

        #find an available cpu from the cpuList
        # data.record.write(f"packet waiting: {packet.packetID}\n")
        
        # get a cpu that's free and execute the packet
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if not self.cpu_in_use[cpus.id]:
                opt_cpu = cpus
                
                # data.record.write(f"node id: {self.id}\n")
                # data.record.write(f"cpu id: {opt_cpu.id}\n")
                # data.record.write(f"cpu check: {packet.packetID}\n")
                yield from opt_cpu.process(packet)
                break