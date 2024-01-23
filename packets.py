import config

#statistics of a packet
class Packets:
    def __init__(self, destination, processTime, sendTime, deadline, enable_deadline):
        # check if the packet is processed
        self.processed = False

        # the time it takes to process the packet
        self.processTime = processTime
        
        # destination of the packet
        self.destination = destination
        
        # deadline of the packet
        self.enable_deadline = enable_deadline
        self.deadline = deadline

        # measuring delay
        self.sendTime = sendTime
        self.processedTime = 0
        self.reached_cloud = 0
