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
        packet.processedTime = self.env.now
        packet.transmit_time = packet.transmit_time / 2
        packet.processed = True
        
        # send it to the next node
        # maybe we need "yield from" here
        yield from self.node.nextNode.receive(packet)

        # print(f"process id: {packet.packetID}")
        # print(f"node id {self.node.id}")
        for packet in self.node.queue:
                print(packet)
        if len(self.node.queue) > 0:
            nextPacket = self.node.queue.pop(0)
            print(f"next packet: {nextPacket}")
            
            # should i do this?
            self.env.process(self.process(nextPacket))
        self.node.cpu_in_use -= 1
