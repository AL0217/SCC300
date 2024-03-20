import simpy
import config
import data

class cpu:
    def __init__(self, env, node, id):
        # the id of the cpu
        self.id = id

        # the time this cpu is free
        self.next_available_time = 0

        # the simulation environment
        self.env = env

        # the node that this cpu belongs to
        self.node = node

        self.idle_time = 0
        self.last_use = 0

    
    def process(self, packet):
        # now - last time use
        self.idle_time += self.env.now - self.last_use
        # if this is the optimal one
        if config.scheduling_method == "optimal":
            # for item in self.node.simulation_queue:
                # data.record.write(f"stuff in simulation queue: {item}\n")
            self.node.simulation_queue.pop(packet.packetID)
            if packet.simulate_processed is False:
                self.node.cpu_schedule[self.id] = self.env.now + packet.processTime
        # set the cpu to busy
        self.node.cpu_in_use[self.id] = True
        self.next_available_time = self.env.now + packet.processTime

        # print status of cpu
        # data.record.write(f"cpu id: {self.id}, node: {self.node.id}\n")
        # for cpus in self.node.cpuList:
        #     data.record.write(f" {cpus.id} : {cpus.next_available_time} \n")
        # data.record.write(f"processing: '{packet.packetID}' and deadline: {packet.deadline}\n")
        # data.record.write(f"now: {self.env.now}\n")

        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)

        if config.scheduling_method == "optimal":
            packet.destination = "Cloud"
        # Once processed, reduce the packet size
        packet.dataSize /= 2

        # update the status of the packet
        packet.processedTime = self.env.now
        packet.processed = True

        # data.record.write(f"processed Time: {packet.processedTime}\n")
        # data.record.write(f"releasing cpu id: {self.id}, node: {self.node.id}\n")
        # data.record.write(f"processing: {packet.packetID}\n")
        # data.record.write(f"now: {self.env.now}\n")
        # release the cpu
        self.node.cpu_in_use[self.id] = False
        
        # send it to the next node
        self.env.process(self.node.nextNode.receive(packet))
        # data.record.write(f"finished packet: {packet.packetID}\n")

        # check if there is any packet waiting in the queue
        if len(self.node.queue) > 0:
            nextPacket = self.node.queue.pop(0)
            # data.record.write(f"next packet: {nextPacket.packetID}\n")
            
            # get the first one from the queue
            self.env.process(self.process(nextPacket))
        
        self.last_use = self.env.now

    