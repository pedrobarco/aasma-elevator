IN = 1
OUT = -1
WAITING = 0
MIA = -2

def formatState(state):
    if (state == 1):
        return 'IN'
    elif (state == -1):
        return 'OUT'
    elif (state == 0):
        return 'WAITING'
    elif (state == -2):
        return 'MIA'

class User():
    def __init__(self, weight, floor=0):
        self.weight = weight
        self.floor = floor
        self.state = MIA
        self.destinationFloor = None

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
    
    def getState(self):
        seperator = ' '
        state = f'W: {self.weight}'
        state = state + seperator + f'S: {formatState(self.state)}'
        state = state + seperator + f'F: {self.floor}'
        return state