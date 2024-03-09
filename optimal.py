import node
import data
import config
import copy
from topology import topology
from packets import Packets

class optimal(node.Node):
    def __init__(self, id, env, node, num_processor, distance, topology):
        super().__init__(id, env, node, num_processor, distance, topology)
        self.simulation_queue = {}
    
    def scheduling(self, packet):
        if packet.packetID in self.simulation_queue:
            data.record.write("collide")
            return
        
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        self.simulation_queue[packet.packetID] = packet
        self.simulation_queue = dict(sorted(self.simulation_queue.items(), key=lambda x: x[1].arrivalTime))

        # for item in self.simulation_queue:
        #     data.record.write(f"stuff in simulation queue: {item}\n")
        for p in self.simulation_queue:
            best_cpu = 0
            delta = 1000
            temp_p = self.simulation_queue.get(p)
            # find the closest 
            if min(cpu_schedule) > temp_p.arrivalTime:
                best_cpu = cpu_schedule.index(min(cpu_schedule))
                cpu_schedule[best_cpu] += temp_p.processTime
                # data.record.write(f"the schedule: {cpu_schedule}\n")
                # data.record.write(f"schedule: {cpu_schedule[best_cpu]}, arrival Time: {temp_p.arrivalTime}, deadline: {temp_p.deadline}\n")
                if cpu_schedule[best_cpu] > temp_p.deadline:
                    data.record.write("Fail\n")
                    self.simulation_queue.pop(packet.packetID)
                    return False
                continue

            for index, available_time in enumerate(cpu_schedule):
                diff = temp_p.arrivalTime - available_time

                # data.record.write(f"available time : {available_time}, p.arrivalTime: {temp_p.arrivalTime}, deadline: {temp_p.deadline}\n")
                # if the arrvial time is closer and is coming after the cpu is available
                if diff < delta and diff >= 0:
                    delta = diff
                    best_cpu = index
            
            cpu_schedule[best_cpu] = temp_p.arrivalTime + temp_p.processTime
            # data.record.write(f"schedule: {cpu_schedule[best_cpu]}\n")

            # if it is causing any miss in deadline
            if cpu_schedule[best_cpu] > temp_p.deadline:
                data.record.write("Fail\n")
                self.simulation_queue.pop(packet.packetID)
                return False
        return True



    def request(self):
        # create a packet that need to be send
        gen_deadline = config.gen_deadline(self.env.now)
        packet = Packets(destination=1, processTime=config.PROCESS_TIME, sendTime=self.env.now, deadline = gen_deadline)

        # loop start from the highest node, if the current time + propogation time + process time can meet the deadline
        # set the node to the destination

        for node in self.node_set[-2:0:-1]:
            distance = self.topology.get_distance(self.id, node)
            packet.arrivalTime = self.env.now + distance * 10
            data.record.write(f"arrival time: {packet.arrivalTime} distance: {distance}\n")
            curr_node = self.topology.get_node(node)
            if curr_node == None:
                data.record.write("No such Node")
                return
            
            if curr_node.scheduling(packet):
                packet.destination = node
                data.record.write(f"destination {packet.destination}\n")
                break

        # add the packet to the list
        data.latencyList[packet.packetID] = 0
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"time now: {self.env.now}\n")
        # Send the packet
        yield from self.nextNode.receive(packet)


    def receive(self, packet):
        # simulate the time used to send the packet
        propagationTime = int(self.distance_to_nextNode / config.PROPAGATION_SPEED)
        yield self.env.timeout(propagationTime)

        # print the info of the packet and the node
        data.record.write("Transmitted\n")
        data.record.write(f"my id is: {self.id}\n")
        data.record.write(f"packet id: {packet.packetID}\n")
        data.record.write(f"propagationTime : {propagationTime}\n")
        # data.record.write(f"transmission time: {transmissionTime}\n")
        data.record.write(f"env now: {self.env.now}\n")

        # if this node is cloud
        if self.id == "Cloud":
            yield from self.cloudReceive(packet)
            return
        
        #######-----IF THIS NODE IS NOT THE CLOUD-----######
        # if this is not the assigned node
        if self.id != packet.destination:
            data.record.write("I am passing it")
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
        # if self.simulation_queue.get(packet.packetID) == None:
        #     data.record.write(f"wrong schedule: {packet.packetID}\n")
        #     return
        

        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            # print the states of the cpus
            data.record.write(f"packet waiting: {packet.packetID}\n")
            data.record.write(f"cpu_in_use: {self.cpu_in_use}\n")
            for cpus in self.cpuList:
                data.record.write(str(cpus.next_available_time) + "\n")

            self.queue.append(packet)
            data.record.write(f"packet added to queue: {packet.packetID}\n")
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
            if not self.cpu_in_use[cpus.id]:
                opt_cpu = cpus
                
                data.record.write(f"node id: {self.id}\n")
                data.record.write(f"cpu id: {opt_cpu.id}\n")
                data.record.write(f"cpu check: {packet.packetID}\n")
                yield from opt_cpu.process(packet)
                break

                
    def complete_time(self, queue):
        pass

        
                

            
        
