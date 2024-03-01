from abc import abstractmethod
import node
import data
import config
import copy
from packets import Packets

class optimal(node.Node):
    def __init__(self, id, env, node, num_processor, distance):
        super().__init__(self, id, env, node, num_processor, distance)
        self.node_set = []
        self.simulation_queue = []

    def busy(self, packet):
        # IF it is impossible to meet the deadline
        if packet.processTime > packet.deadline:
            return False
    
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        temp_queue = copy.deepcopy(self.simulation_queue)
        temp_queue.append(packet)
        temp_queue.sort(key = lambda p: p.deadline)

        # simulate the queue according to deadline
        for packet in temp_queue:
            # get the earliest available cpu
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            
            # update the scheduler
            cpu_schedule[selected_cpu] += packet.processTime

            if cpu_schedule[selected_cpu] > packet.deadline:
                data.record.write("failed\n")
                return False

        # if the packet added will not lead to fail in any packets in the queue
        # reserve place for the packet,  
        return True



    def request(self):
        # create a packet that need to be send
        gen_deadline = config.gen_deadline(self.env.now)
        packet = Packets(destination=1, processTime=config.PROCESS_TIME, sendTime=self.env.now, deadline = gen_deadline)

        # loop start from the highest node, if the current time + propogation time + process time can meet the deadline
        # set the node to the destination
        for i in range(len(self.node_set) - 1, -1, -1):
            distance = int(i * config.DISTANCE / config.PROPAGATION_SPEED)

            if self.node_set[i].busy():
                packet.destination = self.node_set[i].id
                break

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"time now: {self.env.now}\n")
        # Send the packet


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
            # if packet.packetID not in data.packetSet:
            #     data.packetSet.add(packet.packetID)
            # else:
            #     data.record.write("collide")
            
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
        # if this is not the assigned node
        if self.id != packet.destination:
            self.env.process(self.nextNode.receive(packet))
            return

        # if the packet processed
        if(packet.processed):
            data.record.write("passed processed packet\n")

            # pass it directly
            #call the receive function of the next node
            self.env.process(self.nextNode.receive(packet))
            return

        # debug
        if packet.id not in self.simulation_queue:
            print(f"wrong schedule: {packet.id}")
            return
        

        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            # print the states of the cpus
            data.record.write(f"packet waiting: {packet.packetID}\n")
            data.record.write(f"cpu_in_use: {self.cpu_in_use}\n")
            for cpus in self.cpuList:
                data.record.write(str(cpus.next_available_time) + "\n")

            self.queue.append(packet)
            self.queue.sort(key = lambda p: p.deadline)
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

                
    def complete_time(self, queue):
        pass

        
                

            
        
