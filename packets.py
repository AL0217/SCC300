
#statistics of a packet
class Packets:
    def __init__(self, destination, processTime):
        self.processed = False
        self.processTime = processTime
        self.destination = destination
