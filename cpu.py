import simpy

class cpu:
    def __init__(self, env, node):
        self.next_available_time = 0
        self.env = env
        self.node = node

    def checkBusy(self):
        if self.next_available_time > self.env.now:
            return True
        else:
            return False
    
    def process(self, packet):
        self.node.cpu_in_use += 1
        # set the cpu to busy
        self.next_available_time = self.env.now + packet.processTime

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)
        
        # update the status of the packet
        packet.processed = True
        
        # send it to the next node
        self.node.nextNode.receive(packet)

        if len(self.node.queue) != 0:
            nextPacket = self.node.queue.pop(0)
            self.process(nextPacket)
        
        self.node.cpu_in_use -= 1
