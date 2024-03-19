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
        queue.append(packet)
        queue.sort(key = lambda p: p.deadline)

        # for p in queue:
        #     data.record.write(f"in node queue: {p.packetID}, deadline: {p.deadline}\n")
        # sort the queue according to deadline
        

        # simulate the queue to check if any of the packets will miss the deadline if added the new packet
        for p in queue:
            if p.simulate_processed:
                # data.record.write(f"{p.packetID} sim in complete\n")
                continue
            # data.record.write(f"packet id: {p.packetID}\n")
            # data.record.write(f"arrival Time: {p.arrivalTime}\n")

            
            # get the earliest available cpu
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            # data.record.write(f"the schedule before: in {self.id} cpu {selected_cpu}, {cpu_schedule}\n")
            # it frees after its arrival
            if cpu_schedule[selected_cpu] > p.arrivalTime:
                # data.record.write(f"larger than\n")
                cpu_schedule[selected_cpu] += p.processTime
                # update the scheduler
                
            elif cpu_schedule[selected_cpu] <= p.arrivalTime and len(queue[queue.index(p) + 1:]) == 0:
                # data.record.write(f"smaller than\n")
                cpu_schedule[selected_cpu] = p.arrivalTime + p.processTime
            
            else:
                # data.record.write(f"exception\n")
                # for p in queue:
                #     data.record.write(f"in node queue: {p.packetID}, arrivalTime: {p.arrivalTime}\n")
                continue
            
            # data.record.write(f"deadline: {p.deadline}\n")
            # data.record.write(f"the schedule after: {cpu_schedule}\n")



            # check if the packet fail to meet the deadline
            if cpu_schedule[selected_cpu] > p.deadline:
                # data.record.write("failed\n")
                return False

        # if all the packet didn't miss, return yes   
        return True

    def arrival_sim(self):
        arrival_queue = []

        # simulate the arrival of packets
        for packet in self.simulation_queue:  
            # data.record.write(f"arrival_queue: {arrival_queue}\n")
            temp_packet = self.simulation_queue.get(packet)
            # data.record.write(f"packet: {packet}\n")
            # data.record.write(f"arrival time: {temp_packet.arrivalTime}\n")

            for p in arrival_queue[:]:
                if p.simulate_processed:
                    arrival_queue.remove(p)
                    # data.record.write("simED\n")
                    continue
                # if the packets stays and will be processed before the new packet arrive
                # if they can be processed before arrival
                available_cpu = min(self.cpu_schedule)
                if available_cpu < temp_packet.arrivalTime:
                    # data.record.write(f"processed: {p.simulate_processed}\n")
                    # data.record.write(f"sim process: {p.packetID}\n")
                    # get the earliest available cpu
                    selected_cpu = self.cpu_schedule.index(available_cpu)
                    
                    # data.record.write(f"schedule before: {self.cpu_schedule}\n")
                    # update the simulation time
                    
                    if self.cpu_schedule[selected_cpu] >= p.arrivalTime:
                        # update the scheduler
                        self.cpu_schedule[selected_cpu] += p.processTime

                    elif self.cpu_schedule[selected_cpu] < p.arrivalTime:
                        # update the scheduler
                        self.cpu_schedule[selected_cpu] = p.arrivalTime + p.processTime

                    # data.record.write(f"schedule: {self.cpu_schedule}\n")
            
                    # check if the packet fail to meet the deadline
                    if self.cpu_schedule[selected_cpu] > p.deadline:
                        # data.record.write("queue before failed\n")
                        return False
                    
                    # if it is processed, remove the packet from the arrival queue
                    arrival_queue.remove(p)
                    self.simulation_queue.get(p.packetID).simulate_processed = True
                    
                else:
                    # data.record.write(f"cpu schedule: {self.cpu_schedule}\n")
                    # data.record.write(f"directly here id: {p.packetID}\n")
                    break
            
            # use EDF to check if the remaining queue can meet all their deadlines 
            # if it can't meet, return False
            flag = self.complete_time(arrival_queue, temp_packet)
            # data.record.write(f"flag: {flag}\n")

            # this mean i try to schedule the packet and it fails it
            if flag is False:
                return False
        return True
    

    def scheduling(self, packet):
        if packet.packetID in self.simulation_queue:
            # data.record.write("collide")
            return
        
        # cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        # data.record.write(f"id: {packet.packetID}\n")
        self.simulation_queue[packet.packetID] = packet
        self.simulation_queue = dict(sorted(self.simulation_queue.items(), key=lambda x: (x[1].arrivalTime)))
        # for item in self.simulation_queue:
        #     data.record.write(f"stuff in simulation queue: {item}\n")
        if not self.arrival_sim():
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
            packet.arrivalTime = self.env.now + int(distance * 10)
            # data.record.write(f"trying node: {node}\n")
            # data.record.write(f"arrival time: {packet.arrivalTime} distance: {distance}\n")
            curr_node = self.topology.get_node(node)
            if curr_node == None:
                # data.record.write("No such Node")
                return
            
            if curr_node.scheduling(packet):
                packet.destination = node
                # data.record.write(f"destination {packet.destination}\n")
                break

        # print(f"packet {packet.packetID}")

        # add the packet to the list
        data.latencyList[self.experimentID][packet.packetID] = 0
        # data.record.write(f"destination: {packet.destination}\n")
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
            self.env.process(self.nextNode.receive(packet))
            return

        # if the packet processed
        if(packet.processed):
            # data.record.write("passed processed packet\n")

            # pass it directly
            #call the receive function of the next node
            self.env.process(self.nextNode.receive(packet))
            return

        # debug
        # if self.simulation_queue.get(packet.packetID) == None:
            # data.record.write(f"wrong schedule: {packet.packetID}\n")
        #     return
        
        # if all cpu is busy
        if not any(cpu is False for cpu in self.cpu_in_use.values()):
            # print the states of the cpus
            # data.record.write(f"packet waiting: {packet.packetID}\n")
            # data.record.write(f"cpu_in_use: {self.cpu_in_use}\n")
            # for cpus in self.cpuList:
            #     data.record.write(str(cpus.next_available_time) + "\n")

            self.queue.append(packet)
            # data.record.write(f"packet added to queue: {packet.packetID}\n")
            self.queue.sort(key = lambda p: p.deadline)

            # for pac in self.queue:
            #     data.record.write(f"packet in node queue: {pac.packetID}, deadline = {pac.deadline}\n")
            return
        
        # if the packet is admitted and the node is free to process it
        # data.record.write("not processed\n")

        #find an available cpu from the cpuList
        # data.record.write(f"packet waiting: {packet.packetID}\n")
        
        # get a cpu that's free and execute the packet
        for cpus in self.cpuList:
            #select the cpu and break the loop
            if self.cpu_in_use[cpus.id] is False:
                yield from cpus.process(packet)
                return