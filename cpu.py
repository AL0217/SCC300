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

    # function to check if this cpu is busy
    def busy(self):
        if self.next_available_time > self.env.now:
            return True
        else:
            return False
    
    def process(self, packet):
        # set the cpu to busy
        self.node.cpu_in_use[self.id] = True
        self.next_available_time = self.env.now + packet.processTime

        # print status of cpu
        data.record.write(f"cpu id: {self.id}\n")
        data.record.write(f"processing: {packet.packetID} and deadline: {packet.deadline}\n")
        data.record.write(f"now: {self.env.now}\n")

        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)

        # Once processed, reduce the packet size
        packet.dataSize /= 2

        # update the status of the packet
        packet.processedTime = self.env.now
        packet.processed = True
        data.record.write(f"processed Time: {packet.processedTime}\n")

        # release the cpu
        self.node.cpu_in_use[self.id] = False
        
        # send it to the next node
        self.env.process(self.node.nextNode.receive(packet))
        data.record.write(f"finished packet: {packet.packetID}\n")

        # check if there is any packet waiting in the queue
        if len(self.node.queue) > 0:
            nextPacket = self.node.queue.pop(0)
            data.record.write(f"next packet: {nextPacket}\n")
            
            # get the first one from the queue
            self.env.process(self.process(nextPacket))

    