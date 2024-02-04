from cpu import cpu
from packets import Packets
import config as c
import random
import data

class Node:
    def __init__(self, id, env, node, num_processor, distance):
        self.id = id
        self.distance_to_nextNode = distance
        self.queue = []

        self.cpu_num = num_processor
        self.cpuList = [cpu(env, self), cpu(env, self), cpu(env, self), cpu(env, self)]
        self.cpu_in_use = 0

        self.nextNode = node
        self.env = env
        

    def request(self):
        # create a packet that need to be send
        packet = Packets(destination=1, processTime=c.PROCESS_TIME, sendTime=self.env.now, deadline=(self.env.now + random.randint(20, 80)), enable_deadline=True)

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        print(f"packet id: {packet.packetID}")
        print(f"time now: {self.env.now}")
        # Send the packet
    
        yield from self.nextNode.receive(packet)


    def receive(self, packet):
        # simulate the time used to send the packet
        yield self.env.timeout(packet.transmit_time)
        print("Transmitted")

        packet.setDistance(self.distance_to_nextNode)

        print(f"my id is: {self.id}")
        print(f"packet id: {packet.packetID}")
        print(f"env now: {self.env.now}")

        if self.id == "Cloud":
            if packet.processed:
                print("processed packet arrived cloud")
                data.processedCount += 1
                # Do something to record this
            else:
                print("unprocessed packet arrived cloud")
                # Do something to record this
                # simulate the time for process it at cloud
                yield self.env.timeout(packet.processTime)
                packet.processedTime = self.env.now
                data.unprocessedCount += 1

            # record a packet arrived cloud
            if self.env.now <= packet.deadline:
                data.meetDeadline += 1
            data.receivedCount += 1
            print(f"processed time: {packet.processedTime}")
            # print(packet.sendTime)
            # print(packet.packetID)
            data.latencyList[packet.packetID] = packet.processedTime - packet.sendTime
            return
        
        # if the packet processed
        if(packet.processed):
            print("passed processed packet")

            #call the receive function
            packet.setDistance(self.distance_to_nextNode / 2)
            yield from self.nextNode.receive(packet)
            return

        # Check if the node is busy
        if(self.cpu_in_use >= self.cpu_num):
            for cpus in self.cpuList:
                print(cpus.next_available_time)
            if len(self.queue) < c.SIZE_OF_QUEUE:
                self.queue.append(packet)
                print("append to queue")
                for packet in self.queue:
                    print(packet)
                return

            print("passed")

            #call the receive function
            packet.setDistance(self.distance_to_nextNode)
            yield from self.nextNode.receive(packet)
            return



        print("not processed")

        #init a opt_cpu variable
        opt_cpu = self.cpuList[0]

        #find an available cpu from the cpuList
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if not cpus.checkBusy():
                opt_cpu = cpus
                break

        yield from opt_cpu.process(packet)
