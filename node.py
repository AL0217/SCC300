from cpu import cpu
from packets import Packets
import config
import random
import data
import simpy
import copy

class Node:
    def __init__(self, id, env, node, num_processor, distance):
        self.id = id
        self.distance_to_nextNode = distance
        self.queue = []

        self.cpu_num = num_processor
        self.cpuList = [cpu(env, self, i) for i in range(num_processor)]
        self.cpu_in_use = {i: False for i in range(num_processor)}
        self.nextNode = node
        self.env = env
        

    def request(self):
        # create a packet that need to be send
        # random.seed(1)
        packet = Packets(destination=1, processTime=config.PROCESS_TIME, sendTime=self.env.now, deadline=(config.gen_deadline(self.env.now)), enable_deadline=True)

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"time now: {self.env.now}\n")
        # Send the packet
    
        yield from self.nextNode.receive(packet)


    def receive(self, packet):
        # simulate the time used to send the packet
        propagationTime = int(self.distance_to_nextNode / config.PROPAGATION_SPEED)
        transmissionTime = (packet.dataSize / config.TRANSMISSION_SPEED)
        yield self.env.timeout(propagationTime + transmissionTime)

        # print the info of the packet and the node
        data.record.write("Transmitted\n")
        data.record.write(f"my id is: {self.id}\n")
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"propagationTime : {propagationTime}\n")
        data.record.write(f"transmission time: {transmissionTime}\n")
        data.record.write(f"env now: {self.env.now}\n")

        # if this node is cloud
        if self.id == "Cloud":
            
            if packet.packetID not in data.packetSet:
                data.packetSet.add(packet.packetID)
            else:
                data.record.write("collide")
            
            data.receivedCount += 1
            data.record.write(f"receive packet: {packet.packetID}")
            data.record.write(f"received Count: {data.receivedCount}")
            # Check if the packet is processed
            if packet.processed:
                data.record.write("processed packet arrived cloud\n")
                data.processedCount += 1
                data.record.write(f"processed Count: {data.processedCount}")
            else:
                # if the packet is unprocessed, processed it at cloud immediately
                data.record.write("unprocessed packet arrived cloud\n")

                # simulate the time for process it at cloud
                yield self.env.timeout(packet.processTime)
                packet.processedTime = self.env.now

            # get the data of the packet arrived cloud
            # need to add the deadline graph and other metrics

            # Check if the packet meet the deadline    
            if packet.processedTime <= packet.deadline:
                data.meetDeadline += 1
            else:
                data.failed[packet.packetID] = [packet.sendTime, packet.processedTime, packet.deadline]
            
            data.record.write(f"processed time: {packet.processedTime}\n")
            data.latencyList[packet.packetID] = packet.processedTime - packet.sendTime
            return
        
        #######-----IF THIS NODE IS NOT THE CLOUD-----######

        # if the packet processed
        if(packet.processed):
            data.record.write("passed processed packet\n")

            # pass it directly
            #call the receive function of the next node
            self.env.process(self.nextNode.receive(packet))
            return
        

        # if it is impossible to meet the deadline, do not admit the packet
        if (self.env.now + packet.processTime > packet.deadline):
            # pass the packet
            data.record.write(f"Not receiving it")
            self.env.process(self.nextNode.receive(packet))
        
        # For admitted packet
        # Check if the node is busy
        # Only allow one packet to look at this
        
        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            # print the states of the cpus
            data.record.write(f"packet waiting: {packet.packetID}\n")
            data.record.write(f"cpu_in_use: {self.cpu_in_use}\n")
            for cpus in self.cpuList:
                data.record.write(str(cpus.next_available_time) + "\n")

            queue = copy.deepcopy(self.queue)
            queue.append(packet)
            # scheduling method to use
            match config.SCHEDULING_METHOD:
                case "FIFO":        # First In First Out
                    # if the p
                    if self.fifo_complete_time(queue) and len(self.queue) < config.SIZE_OF_QUEUE:
                        self.queue.append(packet)
                        data.record.write("append to queue\n")
                        for packet in self.queue:
                            data.record.write(f"this is queue: {packet.packetID}\n")
                        return
                    
                case "EDF":         # Earliest Deadline Firs
                    if self.edf_complete_time(queue):
                        self.queue = queue

                        for packet in self.queue:
                                data.record.write(f"this is queue: {packet.packetID}\n")
                        return
        
            # if fail to admit the packet, pass it
            data.record.write("passing\n")
            self.env.process(self.nextNode.receive(packet))
            return
        
        # if the packet is admitted and the node is free to process it
        data.record.write("not processed\n")
        opt_cpu = self.cpuList[0]

        #find an available cpu from the cpuList

        data.record.write(f"packet waiting: {packet.packetID}\n")
        
        # get a cpu that's free and execute the packet
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if not cpus.busy():
                opt_cpu = cpus
                
                data.record.write(f"node id: {self.id}\n")
                data.record.write(f"cpu id: {opt_cpu.id}\n")
                data.record.write(f"cpu check: {packet.packetID}\n")
                yield from opt_cpu.process(packet)
                break




    # function to calculate the completion time for EDF
    def edf_complete_time(self, queue):
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        queue.sort(key = lambda p: p.deadline)
        for packet in queue:
            data.record.write(f"the schedule: {cpu_schedule}\n")
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            cpu_schedule[selected_cpu] += packet.processTime
            data.record.write(f"deadline: {packet.deadline}\n")
            if cpu_schedule[selected_cpu] > packet.deadline:
                data.record.write("failed\n")
                return False
        return True
    
    #function to calculate the completion time for FIFO
    def fifo_complete_time(self, queue):
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        # loop through the queue to simulate the queue time
        for i in range(len(queue)):
            data.record.write(f"the schedule: {cpu_schedule}\n")
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            cpu_schedule[selected_cpu] += queue[i].processTime
            data.record.write(f"deadline: {queue[i].deadline}\n")

        # check if the current time + process time + queue time can meet the deadline    
        if cpu_schedule[selected_cpu] > queue[len(queue) - 1].deadline:
            data.record.write("failed\n")
            return False


