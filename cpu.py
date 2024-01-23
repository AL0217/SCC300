import simpy

class cpu:
    def __init__(self, env):
        self.next_available_time = 0
        self.env = env

    def checkBusy(self):
        if self.next_available_time > self.env.now:
            return True
        else:
            return False
    
    def process(self, packet):
        # set the cpu to busy
        self.next_available_time = self.env.now + packet.processTime

        # create instance vairiable and update it to check time
        # simulate the time of processing the packet
        yield self.env.timeout(packet.processTime)