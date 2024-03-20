import node
import data

class edf(node.Node):
    def __init__(self, id, env, node, num_processor, distance, topology):
        super().__init__(id, env, node, num_processor, distance, topology)
    

    # function to calculate the completion time for EDF
    def complete_time(self, queue, packet):
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        # sort the queue according to deadline
        queue.sort(key = lambda p: p.deadline)

        # simulate the queue to check if any of the packets will miss the deadline if added the new packet
        for packet in queue:
            data.record.write(f"the queue: {packet.packetID}, deadline: {packet.deadline}\n")
            # get the earliest available cpu
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            # for available_time in cpu_schedule:
            #     selected_cpu = cpu_schedule.index(available_time)
            
            # update the scheduler
            cpu_schedule[selected_cpu] += packet.processTime
            # data.record.write(f"deadline: {packet.deadline}\n")

            # check if the packet fail to meet the deadline
            if cpu_schedule[selected_cpu] > packet.deadline:
                # data.record.write("failed\n")
                return False

        # if all the packet didn't miss, return yes   
        self.queue.append(packet)
        self.queue.sort(key = lambda p: p.deadline)
        return True