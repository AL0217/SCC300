import simpy
import config
import data

class cpu:
    def __init__(self, env, node, id):
        self.id = id
        self.next_available_time = 0
        # self.available = simpy.Resource(env, capacity = 1)
        self.env = env
        self.node = node

    def busy(self):
        if self.next_available_time > self.env.now:
            return True
        else:
            return False
    
    def process(self, packet):
        self.node.cpu_in_use[self.id] = True
        data.record.write(f"cpu id: {self.id}\n")
        data.record.write(f"processing: {packet.packetID} and deadline: {packet.deadline}\n")
        data.record.write(f"now: {self.env.now}\n")
        # data.record.write(f"{self.node.id} resource now: {resource.count}\n")
        # set the cpu to busy
        self.next_available_time = self.env.now + packet.processTime

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)
        self.node.cpu_in_use[self.id] = False
        # update the status of the packet
        packet.processedTime = self.env.now
        data.record.write(f"processed Time: {packet.processedTime}\n")
        packet.transmit_time /= 2
        packet.processed = True
        
        # send it to the next node
        # maybe we need "yield from" here
        self.env.process(self.node.nextNode.receive(packet))

        data.record.write(f"finish packet: {packet.packetID}\n")
        # print(f"process id: {packet.packetID}")
        # print(f"node id {self.node.id}")

        # release the resources

        if len(self.node.queue) > 0:
            nextPacket = self.node.queue.pop(0)
            data.record.write(f"next packet: {nextPacket}\n")
            
            # get the first one from the queue
            self.env.process(self.process(nextPacket))

    