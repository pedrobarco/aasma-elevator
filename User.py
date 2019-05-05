IN = 1
OUT = -1
WAITING = 0
MIA = -2


class User():
    def __init__(self, weight, floor=0):
        self.weight = weight
        self.floor = floor
        self.destinationFloor = None
        self.state = None

    def requestElevator(self, destinationFloor):
        self.destinationFloor = destinationFloor
        self.state = WAITING

    def enterElevator(self):
        self.state = IN

    def takeStairs(self):
        self.state = MIA

    def exitElevator(self):
        self.state = OUT
        self.destinationFloor = None