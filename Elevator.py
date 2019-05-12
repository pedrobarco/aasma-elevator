UP = 1
DOWN = -1
IDLE = 0


def formatDirection(direction):
    if(direction == UP):
        return '↑'
    elif(direction == DOWN):
        return '↓'
    else:
        return '-'


class Elevator():
    def __init__(self, maxWeight, floor=0):
        self.elevators = []
        self.direction = IDLE
        self.floor = floor
        self.weight = 0
        self.maxWeight = maxWeight
        self.maxFloors = None
        self.destinations = []
        self.users = []

        # while elevator destinations are not empty
        # move to floor + direction
    def updateElevators(self, elevators, maxFloors):
        self.maxFloors = maxFloors
        self.elevators = elevators

    def addStop(self, user):
        self.users.append(user)
        self.destinations.append(user.floor)
        self.destinations.append(user.destinationFloor)
        if self.direction == IDLE:
            firstStop = self.destinations[0]
            self.direction = UP if firstStop > self.floor else DOWN
            print(f'Elevator {formatDirection(self.direction)}')

    def move(self):
        if not self.destinations:
            self.direction = IDLE
        nextFloor = self.floor + self.direction
        self.floor = nextFloor
        if nextFloor in self.destinations:
            self.direction = IDLE

    def calcUtil(self, user):
        if (self.weight + user.weight > self.maxWeight):
            return None
        util = 0
        origin = user.floor
        destination = user.destinationFloor
        userDirection = UP if destination - origin > 0 else DOWN
        isInPath = False
        if (self.direction == UP):
            isInPath = self.floor <= origin and userDirection == UP
        elif (self.direction == DOWN):
            isInPath = self.floor > origin and userDirection == DOWN
        elif (self.direction == IDLE):
            idlePenalty = (0.02 * self.maxWeight)
            util -= idlePenalty
            isInPath = True
        distance = 0
        if isInPath:
            distance = abs(origin - self.floor)
        else:
            lastDest = self.destinations[-1]
            distance = abs(lastDest - self.floor) + abs(origin - lastDest)
        if distance:
            floorPenalty = (0.05 * self.maxWeight * distance)
            util -= floorPenalty
        return util

    def getDirection(self):
        return formatDirection(self.direction)

    def getState(self):
        seperator = ' '
        usersInEl = len(list(filter(lambda u: u.state == 1 , self.users)))
        state = f'C: {usersInEl}'
        state = state + seperator + f'W: {self.weight}/{self.maxWeight}'
        return state

        