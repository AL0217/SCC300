from cpu import cpu
from packets import Packets
import config as c
import random
import data
import copy

class Node:
    def __init__(self, id, env, node, num_processor, distance):
        self.id = id
        self.distance_to_nextNode = distance
        self.queue = []

        self.cpu_num = num_processor
        self.cpuList = []
        for i in range(num_processor):
            self.cpuList.append(cpu(env, self))

        #probably will have to synchronize this
        self.cpu_in_use = 0

        self.nextNode = node
        self.env = env
        

    def request(self):
        # create a packet that need to be send
        packet = Packets(destination=1, processTime=c.PROCESS_TIME, sendTime=self.env.now, deadline=(self.env.now + random.randint(30, 60)), enable_deadline=True)

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"time now: {self.env.now}\n")
        # Send the packet
    
        yield from self.nextNode.receive(packet)


    def receive(self, packet):
        # simulate the time used to send the packet
        yield self.env.timeout(packet.transmit_time)
        data.record.write("Transmitted\n")

        packet.setDistance(self.distance_to_nextNode)

        data.record.write(f"my id is: {self.id}\n")
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"env now: {self.env.now}\n")

        if self.id == "Cloud":
            if packet.processed:
                data.record.write("processed packet arrived cloud\n")
                data.processedCount += 1
                # Do something to record this
            else:
                data.record.write("unprocessed packet arrived cloud\n")
                data.unprocessedCount += 1
                # Do something to record this
                # simulate the time for process it at cloud
                yield self.env.timeout(packet.processTime)
                packet.processedTime = self.env.now
                data.unprocessedCount += 1

            # record a packet arrived cloud
            if self.env.now <= packet.deadline:
                data.meetDeadline += 1
            data.receivedCount += 1
            data.record.write(f"processed time: {packet.processedTime}\n")
            # print(packet.sendTime)
            # print(packet.packetID)
            data.latencyList[packet.packetID] = packet.processedTime - packet.sendTime
            return
        
        # if the packet processed
        if(packet.processed):
            data.record.write("passed processed packet\n")

            #call the receive function
            packet.setDistance(self.distance_to_nextNode / 2)
            yield from self.nextNode.receive(packet)
            return
        

        # if it is in EDF mode
        # if it is not possible to meet the deadline, do not admit the packet
        if (c.SCHEDULING_METHOD == "EDF") and (self.env.now + packet.processTime > packet.deadline):
            # pass the packet
            data.record.write(f"Not receiving it")
            packet.setDistance(self.distance_to_nextNode)
            yield from self.nextNode.receive(packet)
        
        # For admitted packet
        # Check if the node is busy
        if(self.cpu_in_use >= self.cpu_num):
            # print the states of the cpus
            for cpus in self.cpuList:
                data.record.write(str(cpus.next_available_time) + "\n")

            # scheduling method to use
            match c.SCHEDULING_METHOD:
                case "FIFO":        # First In First Out
                    if len(self.queue) < c.SIZE_OF_QUEUE:
                        self.queue.append(packet)
                        data.record.write("append to queue\n")
                        for packet in self.queue:
                            data.record.write(f"this is queue: {packet.packetID}\n")
                        return
                    
                case "EDF":         # Earliest Deadline First
                    queue = copy.deepcopy(self.queue)
                    queue.append(packet)
                    if self.edf_complete_time(queue):
                        self.queue = queue

                        for packet in self.queue:
                                data.record.write(f"this is queue: {packet.packetID}\n")
                        return
                    else:
                        # if didn't append to the queue
                        pass
            
        
            #call the receive function
            packet.setDistance(self.distance_to_nextNode)
            data.record.write("passing\n")
            yield from self.nextNode.receive(packet)
            return



        data.record.write("not processed\n")

        #init a opt_cpu variable
        opt_cpu = self.cpuList[0]

        #find an available cpu from the cpuList
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if not cpus.checkBusy():
                opt_cpu = cpus
                break

        yield from opt_cpu.process(packet)


    def edf_complete_time(self, queue):
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(c.NUMBER_OF_PROCESSORS)]
        queue.sort(key = lambda p: p.deadline)
        for packet in queue:
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            cpu_schedule[selected_cpu] += packet.processTime
            if cpu_schedule[selected_cpu] > packet.deadline:
                data.record.write("failed\n")
                return False
        return True


