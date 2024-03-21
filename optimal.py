import node
import data
import config
import copy
from topology import topology
from packets import Packets
from collections import OrderedDict

class optimal(node.Node):
    def __init__(self, id, env, node, num_processor, distance, topology):
        super().__init__(id, env, node, num_processor, distance, topology)
        self.simulation_queue = {}
        self.cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        
        # function to calculate the completion time for EDF
    def complete_time(self, queue, packet):
        cpu_schedule = copy.deepcopy(self.cpu_schedule)
        # data.record.write("complete time\n")
        queue.sort(key = lambda p: p.deadline)

        # simulate the queue to check if any of the packets will miss the deadline if added the new packet
        for p in queue:
            p.assigned = True
            if p.simulate_processed:
                data.record.write(f"{p.packetID} sim in complete\n")
                continue
            # data.record.write(f"packet id: '{p.packetID}'\n")
            # data.record.write(f"arrival Time: {p.arrivalTime}\n")

            selected_cpu = cpu_schedule.index(min(cpu_schedule))

            # data.record.write(f"the schedule before: in {self.id} cpu {selected_cpu}, {cpu_schedule}\n")
            # it frees after its arrival
            cpu_schedule[selected_cpu] += p.processTime
            
            # data.record.write(f"deadline: {p.deadline}\n")
            # data.record.write(f"the schedule after: {cpu_schedule}\n")

            # check if the packet fail to meet the deadline
            if cpu_schedule[selected_cpu] > p.deadline:
                # data.record.write("failed\n")
                packet.assigned = False
                return False

        # if all the packet didn't miss, return yes   
        return True

    def arrival_sim(self):
        arrival_queue = []

        # simulate the arrival of packets
        for packet in self.simulation_queue:
            # for arr_p in arrival_queue:
            #     data.record.write(f"arrival_queue: {arr_p.packetID}\n")
            temp_packet = self.simulation_queue.get(packet)
            # data.record.write(f"packet: {packet}\n")
            # data.record.write(f"arrival time: {temp_packet.arrivalTime}\n")
            arrival_queue.append(temp_packet)

            for p in arrival_queue[:]:
                if p.simulate_processed:
                    arrival_queue.remove(p)
                    # data.record.write("simED\n")
                    continue
                # if the packets stays and will be processed before the new packet arrive
                # if they can be processed before arrival
                available_cpu = min(self.cpu_schedule)

                temp_cpu_in_use = {i: False for i in range(len(self.cpuList))}
                    
                # if the cpu is free after the packet arrival, set to true (busy)
                for i in range(len(self.cpu_schedule)):
                    if self.cpu_schedule[i] > p.arrivalTime:
                        temp_cpu_in_use[i] = True
                selected_cpu = 0

                if available_cpu < temp_packet.arrivalTime:
                    # data.record.write(f"processed: {p.simulate_processed}\n")
                    # data.record.write(f"sim process: {p.packetID}\n")
                    # data.record.write(f"arrival time: {p.arrivalTime}\n")
                    # get the earliest available cpu
                    # check the availability of that node at that moment
                    if p.assigned is True:
                        selected_cpu = self.cpu_schedule.index(min(self.cpu_schedule))
                        # data.record.write(f"selected_cpu for {p.packetID} is {selected_cpu}\n")
                        # data.record.write(f"I am in if\n")
                    else:
                        for i in range(len(self.cpu_schedule)):
                            if self.cpu_schedule[i] > p.arrivalTime:
                                temp_cpu_in_use[i] = True
                        # data.record.write(f"I am in else\n")
                        # if not all cpu is False(Free), get the first one that can execute and execute it 
                        if any(cpu is not True for cpu in temp_cpu_in_use):
                            for i in range(len(temp_cpu_in_use)):
                                if temp_cpu_in_use[i] is False:
                                    selected_cpu = i
                                    break

                    # selected_cpu = self.cpu_schedule.index(min(self.cpu_schedule))
                    # data.record.write(f"schedule before: {self.cpu_schedule}\n")
                    # update the simulation time

                    value = self.cpu_schedule[selected_cpu]
                    # if the packet comes early cpu is free
                    #  can be new packet or packet from last iter
                    if self.cpu_schedule[selected_cpu] >= p.arrivalTime:
                        value = p.processTime
                        # update the scheduler
                        self.cpu_schedule[selected_cpu] += value
                    # else if the packets comes after the cpu idle
                    elif self.cpu_schedule[selected_cpu] < p.arrivalTime:
                        value = p.arrivalTime + p.processTime
                        # update the scheduler
                        # data.record.write(f"smaller than\n")
                        self.cpu_schedule[selected_cpu] = p.arrivalTime + p.processTime

                    if self.cpu_schedule[selected_cpu] > p.deadline:
                        # data.record.write("queue before failed\n")
                        # reverse
                        self.cpu_schedule[selected_cpu] = value
                        return False

                    # data.record.write(f"schedule after: {self.cpu_schedule}\n")
            
                    # check if the packet fail to meet the deadline

                    
                    # if it is processed, remove the packet from the arrival queue
                    arrival_queue.remove(p)
                    self.simulation_queue.get(p.packetID).simulate_processed = True
                    
                else:
                    # data.record.write(f"cpu schedule: {self.cpu_schedule}\n")
                    # data.record.write(f"directly here id: {p.packetID}\n")
                    break
            
            # use EDF to check if the remaining queue can meet all their deadlines 
            # if it can't meet, return False
            if arrival_queue is not []:
                flag = self.complete_time(arrival_queue, temp_packet)
            # data.record.write(f"flag: {flag}\n")

            # this mean i try to schedule the packet and it fails it
            if flag is False:
                return False
        return True
    

    def scheduling(self, packet):
        
        # cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        # data.record.write(f"id: {packet.packetID}\n")
        self.simulation_queue[packet.packetID] = packet
        self.simulation_queue = dict(sorted(self.simulation_queue.items(), key=lambda x: (x[1].arrivalTime)))
        # for item in self.simulation_queue:
        #     data.record.write(f"stuff in simulation queue: {item}\n")
        if self.arrival_sim() is False:
            self.simulation_queue.pop(packet.packetID)
            return False
        return True



    def request(self):
        # create a packet that need to be send
        gen_deadline = config.gen_deadline(self.env.now)
        packet = Packets(destination="Cloud", processTime=config.PROCESS_TIME, sendTime=self.env.now, deadline = gen_deadline)

        # loop start from the highest node, if the current time + propogation time + process time can meet the deadline
        # set the node to the destination
        for node in self.node_set[-2:0:-1]:
            distance = self.topology.get_distance(self.id, node)
            packet.arrivalTime = self.env.now + int(distance * 10)
            # data.record.write(f"trying node: {node}\n")
            # data.record.write(f"arrival time: {packet.arrivalTime} distance: {distance}\n")
            curr_node = self.topology.get_node(node)
            if curr_node == None:
                # data.record.write("No such Node")
                return
            
            # data.record.write(f"trying {node}\n")
            if curr_node.scheduling(packet):
                packet.destination = node
                # data.record.write(f"destination {packet.destination}\n")
                break

        # print(f"packet {packet.packetID}")

        # add the packet to the list
        data.latencyList[self.experimentID][packet.packetID] = 0
        if packet.destination != "Cloud":
            data.counter += 1
        # data.record.write(f"destination: {packet.destination}\n")
        # data.record.write(f"packet id: {packet.packetID}\n")
        # data.record.write(f"time now: {self.env.now}\n")
        # Send the packet
        yield from self.nextNode.receive(packet, self.distance_to_nextNode)


    def receive(self, packet, distance_to_next_nde):
        # simulate the time used to send the packet
        yield self.env.timeout(distance_to_next_nde)
        # data.record.write(f"packet: {packet.packetID} yielding for {distance_to_next_nde} in {self.id}\n")

        # print the info of the packet and the node
        # data.record.write("Transmitted\n")
        # data.record.write(f"my id is: {self.id}\n")
        # data.record.write(f"packet id: {packet.packetID}\n")
        # data.record.write(f"propagationTime : {self.distance_to_nextNode}\n")
        # data.record.write(f"env now: {self.env.now}\n")

        # if this node is cloud
        if self.id == "Cloud":
            yield from self.cloudReceive(packet)
            return
        
        #######-----IF THIS NODE IS NOT THE CLOUD-----######
        # if this is not the assigned node
        if self.id != packet.destination:
            # data.record.write("I am passing it")
            self.env.process(self.nextNode.receive(packet, self.distance_to_nextNode))
            return

        # if the packet processed
        if(packet.processed):
            # data.record.write("passed processed packet\n")

            # pass it directly
            #call the receive function of the next node
            self.env.process(self.nextNode.receive(packet, self.distance_to_nextNode))
            return

        # debug
        # if self.simulation_queue.get(packet.packetID) == None:
            # data.record.write(f"wrong schedule: {packet.packetID}\n")
        #     return
        
        # if all cpu is busy
        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            self.queue.append(packet)
            self.queue.sort(key = lambda p: p.deadline)

            return
        
        # if the packet is admitted and the node is free to process it
        # find an available cpu from the cpuList
        # get a cpu that's free and execute the packet
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if self.cpu_in_use[cpus.id] is False:
                yield from cpus.process(packet)
                return