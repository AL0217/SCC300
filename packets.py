import config
import data

#statistics of a packet

class Packets:
    def __init__(self, destination, processTime, sendTime, deadline):
        # check if the packet is processed
        self.packetID = data.packetCount[config.experimentID]

        self.processed = False

        # the time it takes to process the packet
        self.dataSize = config.DATA_SIZE

        self.processTime = int(self.dataSize/config.PROCESS_SPEED)
        
        # destination of the packet
        self.destination = destination
        
        # deadline of the packet
        self.deadline = deadline

        # measuring delay
        self.sendTime = sendTime
        self.completionTime = 0
        self.processedTime = 0
        self.reached_cloud = 0

        #optimal variables
        self.arrivalTime = 0
        self.assigned = False
        self.simulate_processed = False