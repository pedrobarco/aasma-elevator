IN = 1
OUT = -1
WAITING = 0
MIA = -2

UP = 1
DOWN = -1
IDLE = 0

ON = 1
OFF = 0

import math
import bisect

def formatDirection(direction):
    if(direction == UP):
        return '↑'
    elif(direction == DOWN):
        return '↓'
    else:
        return '-'

def formatLights(lights):
    if(lights == ON):
        return 'ON'
    elif(lights == OFF):
        return 'OFF'

def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

class Elevator():
    def __init__(self, maxWeight, floor=0):
        self.elevators = []
        self.direction = IDLE
        self.floor = floor
        self.weight = 0
        self.maxWeight = maxWeight
        self.maxFloors = None
        self.destinations = []
        self.destinationHistory = []
        self.inRepositioning = False
        self.turnsSavedByMaxWeight = 0
        self.turnsSavedByPath = 0
        self.turnsSavedByUsers = 0
        self.turnsWithNoLight = 0
        self.users = []
        self.lights = OFF

        # while elevator destinations are not empty
        # move to floor + direction
    def updateElevators(self, elevators, maxFloors):
        self.maxFloors = maxFloors
        self.elevators = elevators
    
    def updateDestinations(self):
        unsortedDestinations = []
        for user in self.users:
            if user.floor == user.originalFloor:
                unsortedDestinations.append(user.originalFloor)
            unsortedDestinations.append(user.destinationFloor)
        inPath, notInPath = partition(lambda d: d > self.floor if self.direction == UP else d <= self.floor, unsortedDestinations)
        inPath = sorted(list(dict.fromkeys(inPath)))
        notInPath = sorted(list(dict.fromkeys(notInPath)))
        destinations = inPath + notInPath
        return destinations

    def addStop(self, user):
        if self.inRepositioning == ON:
            if self.destinations:
               self.destinations.pop(0)
            self.inRepositioning = OFF
            self.turnsSavedByUsers = self.turnsSavedByUsers + abs(self.destinationHistory[-1] - self.floor)
        self.users.append(user)
        self.destinations.append(user.floor)
        self.destinations.append(user.destinationFloor)
        self.destinationHistory.append(user.floor)
        self.destinationHistory.append(user.destinationFloor)
        self.destinations = self.updateDestinations()
    
    def updateLights(self):
        self.lights = ON if self.weight > 0 else OFF

    def addWeight(self, user):
        weight = user.weight
        self.weight = self.weight + weight
        self.updateLights()

    def removeWeight(self, user):
        weight = user.weight
        self.weight = self.weight - weight
        self.users.remove(user)
        self.updateLights()

    def removeFromPath(self, user):
        nearestToUserFloor = bisect.bisect_left(self.destinations, user.floor)
        nearestToUserDestination = bisect.bisect_left(self.destinations, user.destinationFloor)
        self.turnsSavedByPath = self.turnsSavedByPath + abs(nearestToUserFloor - user.floor)
        self.turnsSavedByPath = self.turnsSavedByPath + abs(nearestToUserDestination - user.destinationFloor)
        self.users.remove(user)
        self.destinations = self.updateDestinations()

    def calcUtil(self, user):
        weight = sum([u.weight for u in self.users]) if self.users else self.weight
        if (weight + user.weight > self.maxWeight):
            self.turnsSavedByMaxWeight = self.turnsSavedByMaxWeight + abs(self.floor - user.floor)
            return -math.inf
        util = 0
        origin = user.floor
        destination = user.destinationFloor
        userDirection = UP if destination - origin > 0 else DOWN
        isInPath = False
        if (self.inRepositioning):
            isInPath = True
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
        state = state + seperator + f'L: {formatLights(self.lights)}'
        return state

    def move(self):
        if self.lights == OFF:
            self.turnsWithNoLight = self.turnsWithNoLight + 1
        if not self.destinations:
            if len(self.destinationHistory) > 2:
                roundedAverageFloor = round(sum(self.destinationHistory) / len(self.destinationHistory))
                if roundedAverageFloor != self.floor:
                    self.inRepositioning = ON
                    self.destinations.append(roundedAverageFloor)
                    self.move()
                else:
                    self.direction = IDLE
            else:
                self.direction = IDLE
        else:
            nextStop = self.destinations[0]
            if self.direction == IDLE and nextStop != self.floor:
                self.direction = UP if nextStop > self.floor else DOWN
            nextFloor = self.floor + self.direction
            self.floor = nextFloor
            if nextFloor == self.destinations[0]:
                self.direction = IDLE
                self.destinations.pop(0)
    
    def metrics(self):
        return[self.turnsWithNoLight, self.turnsSavedByMaxWeight, self.turnsSavedByPath, self.turnsSavedByUsers]