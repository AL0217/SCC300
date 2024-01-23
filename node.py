from cpu import cpu
from packets import Packets
import simpy


class Node:
    def __init__(self, id, env, node, distance, number_of_processors):
        self.id = id
        self.distance_to_nextNode = distance
        self.queue = []

        self.cpu_num = number_of_processors
        self.cpuList = [cpu(env), cpu(env), cpu(env), cpu(env)]
        self.cpu_in_use = 0

        self.nextNode = node
        self.env = env

    def request(self):
        #create a packet that need to be send
        packet = Packets(destination=1)
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

        # Check if the node is busy
        if(self.cpu_in_use >= self.cpu_num):
            for cpus in self.cpuList:
                print(cpus.next_available_time)
            if(self.id != "Cloud"):
                if len(self.queue) > 4:
                    self.queue.append(packet)
                    return

                print("passed")
                
                # simulate the time used to send the packet
                yield self.env.timeout(self.distance_to_nextNode)

                #call the receive function
                yield from self.nextNode.receive(packet)
            else:
                print("reached cloud")
            return

        # if the packet processed
        if(packet.processed):
            if(self.id != "Cloud"):
                print("passed processed packet")
                # simulate the time used to send the packet
                yield self.env.timeout(self.distance_to_nextNode)

                #call the receive function
                yield from self.nextNode.receive(packet)
            else:
                print("processed packet reached cloud")
                global receivedCount
                receivedCount += 1
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