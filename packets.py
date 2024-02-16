import config

packetCounter = 1
#statistics of a packet
class Packets:
    def __init__(self, destination, processTime, sendTime, deadline, enable_deadline):
        global packetCounter
        # check if the packet is processed
        self.packetID = packetCounter
        packetCounter += 1

        self.processed = False

        # the time it takes to process the packet
        self.processTime = processTime
        
        # destination of the packet
        self.destination = destination
        self.transmit_time = 10
        
        # deadline of the packet
        self.enable_deadline = enable_deadline
        self.deadline = deadline

        # measuring delay
        self.sendTime = sendTime
        self.completionTime = 0
        self.processedTime = 0
        self.reached_cloud = 0
    
    def setDistance(self, distance_to_nextNode):
        self.transmit_time = distance_to_nextNode
