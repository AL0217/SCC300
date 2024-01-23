from cpu import cpu
from packets import Packets
import config as c
import simpy
import random
import data


class Node:
    def __init__(self, id, env, node, num_processor, distance):
        self.id = id
        self.distance_to_nextNode = distance
        self.queue = []

        self.cpu_num = num_processor
        self.cpuList = [cpu(env), cpu(env), cpu(env), cpu(env)]
        self.cpu_in_use = 0

        self.nextNode = node
        self.env = env

    def request(self):
        #create a packet that need to be send
        packet = Packets(destination=1, processTime=c.PROCESS_TIME, sendTime=self.env.now, deadline=(self.env.now + random.randint(60, 80)), enable_deadline=True)
        # Send the packet
        # simulate the time used to send the packet
        yield self.env.timeout(self.distance_to_nextNode)
        print("Transmitted")

        yield from self.nextNode.receive(packet)

    def handle_queue(self):
        while True:
            # Check if the queue is not empty and a CPU is available
            while self.queue and self.cpu_in_use < self.cpu_num:
                opt_cpu = self.cpuList[0]
                for cpus in self.cpuList:
                    #select the cpu and break the loop
                    if not cpus.checkBusy():
                        opt_cpu = cpus
                        break
                queued_packet = self.queue.pop(0)  # Get the first packet from the queue
                self.cpu_in_use += 1
                yield from opt_cpu.process(queued_packet)  # Assuming you use the first CPU for queue processing
                self.cpu_in_use -= 1
                queued_packet.processed = True

                # the distance here is the DISTANCE to the next node
                yield from self.nextNode.receive(queued_packet)

            # Wait for a short period before checking the queue again
            yield self.env.timeout(1)
    
    def start_queue_handler(self):
        self.env.process(self.handle_queue())


    def receive(self, packet):
        print(f"my id is: {self.id}")
        print("env now: " + str(self.env.now))

        if self.id == "Cloud":
            if packet.processed:
                print("processed packet arrived cloud")
                data.processedCount += 1
                # Do something to record this
            else:
                print("unprocessed packet arrived cloud")
                # Do something to record this
                data.unprocessedCount += 1
            # record a packet arrived cloud
            data.receivedCount += 1
            return

        # Check if the node is busy
        if(self.cpu_in_use >= self.cpu_num):
            for cpus in self.cpuList:
                print(cpus.next_available_time)
            if len(self.queue) > 4:
                self.queue.append(packet)
                return

            print("passed")
            
            # simulate the time used to send the packet
            yield self.env.timeout(self.distance_to_nextNode)

            #call the receive function
            yield from self.nextNode.receive(packet)
            return

        # if the packet processed
        if(packet.processed):
            print("passed processed packet")
            # simulate the time used to send the packet
            yield self.env.timeout(self.distance_to_nextNode)

            #call the receive function
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
        
        # The distance here is the distance from last node
        self.cpu_in_use += 1
        yield from opt_cpu.process(packet)
        self.cpu_in_use -= 1
        packet.processed = True
        # the distance here is the DISTANCE to next node
        yield from self.nextNode.receive(packet)