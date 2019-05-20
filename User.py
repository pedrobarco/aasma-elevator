IN = 1
OUT = -1
WAITING = 0
MIA = -2

UP = 1
DOWN = -1
IDLE = 0

ON = 1
OFF = 0

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
        self.originalFloor = floor
        self.state = MIA
        self.destinationFloor = None
        self.elevator = None

    def requestElevator(self, destinationFloor):
        self.destinationFloor = destinationFloor
        self.state = WAITING

    def setElevator(self, elevator):
        self.elevator = elevator

    def enterElevator(self):
        self.state = IN
        elevator = self.elevator
        elevator.addWeight(self)

    def takeStairs(self):
        self.elevator = None
        self.destinationFloor = None
        self.state = MIA

    def exitElevator(self):
        self.state = OUT
        self.destinationFloor = None
        elevator = self.elevator
        elevator.removeWeight(self)
        self.elevator = None
    
    def getState(self):
        seperator = ' '
        state = f'W: {self.weight}'
        state = state + seperator + f'S: {formatState(self.state)}'
        state = state + seperator + f'CurrF: {self.floor}'
        state = state + seperator + f'DestF: {self.destinationFloor}'
        return state

    def move(self):
        if self.elevator:
            elevator = self.elevator
            if self.state == IN:
                self.floor = elevator.floor
                if self.floor == self.destinationFloor:
                    self.exitElevator()
            elif self.floor == elevator.floor and elevator.direction == IDLE:
                self.enterElevator()
            