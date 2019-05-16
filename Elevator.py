UP = 1
DOWN = -1
IDLE = 0

import math

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

    def addWeight(self, user):
        weight = user.weight
        self.weight = self.weight + weight

    def removeWeight(self, user):
        weight = user.weight
        self.weight = self.weight - weight
        self.users.remove(user)

    def removeFromPath(self, user):
        uIndex = self.users.index(user)
        print(uIndex)
        if(self.destinations[uIndex * 2] ==  user.destinationFloor):
            self.destinations.pop(uIndex * 2)
        elif(self.destinations[uIndex * 2] ==  user.floor):
            self.destinations.pop(uIndex * 2)
            self.destinations.pop(uIndex * 2)
        self.users.pop(uIndex)

    def calcUtil(self, user):
        weight = sum([u.weight for u in self.users]) if self.users else self.weight
        if (weight + user.weight > self.maxWeight):
            return -math.inf
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
        state = state + seperator + f'Dest: {self.destinations}'
        return state

    def move(self):
        if not self.destinations:
            self.direction = IDLE
        else:
            nextStop = self.destinations[0]
            if self.direction == IDLE:
                self.direction = UP if nextStop > self.floor else DOWN
            nextFloor = self.floor + self.direction
            self.floor = nextFloor
            if nextFloor == self.destinations[0]:
                self.direction = IDLE
                self.destinations.pop(0)