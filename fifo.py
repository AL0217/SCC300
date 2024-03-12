import node
import data
import config

class fifo(node.Node):
    def __init__(self, id, env, node, num_processor, distance, topology):
        super().__init__(id, env, node, num_processor, distance, topology)

     #function to calculate the completion time for FIFO
    def complete_time(self, queue, packet):
        if len(queue) > config.SIZE_OF_QUEUE:
            return False
        
        cpu_schedule = [self.cpuList[i].next_available_time for i in range(len(self.cpuList))]
        # loop through the queue to simulate the queue time
        for i in range(len(queue)):
            # data.record.write(f"the schedule: {cpu_schedule}\n")
            selected_cpu = cpu_schedule.index(min(cpu_schedule))
            cpu_schedule[selected_cpu] += queue[i].processTime
            # data.record.write(f"deadline: {queue[i].deadline}\n")

        # check if the current time + process time + queue time can meet the deadline    
        if cpu_schedule[selected_cpu] > queue[len(queue) - 1].deadline:
            # data.record.write("failed\n")
            return False
        self.queue.append(packet)
        return True