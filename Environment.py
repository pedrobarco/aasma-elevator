class Environment():
    def __init__(self, floors):
        self.floors = floors + 1
        self.elevators = []
        self.users = []

    def addUser(self, user):
        self.users.append(user)
    
    def getUserById(self, i):
        return self.users[i - 1]

    def getElevatorById(self, i):
        return self.elevators[i - 1]

    def addElevator(self, elevator):
        self.elevators.append(elevator)
        for elevator in self.elevators:
            updatedElevators = self.elevators[:]
            updatedElevators.remove(elevator)
            elevator.updateElevators(updatedElevators, self.floors)

    def bestFitElevator(self, user):
        utils = []
        for elevator in self.elevators:
            utils.append(elevator.calcUtil(user))
        print(f'Utils: {utils}')
        maxUtil = max(utils)
        return utils.index(maxUtil)

    def requestElevator(self, user, destinationFloor):
        user.requestElevator(destinationFloor)
        bestFit = self.bestFitElevator(user)
        bestElevator = self.elevators[bestFit]
        print(f'== Elevator {bestFit + 1} ==')
        bestElevator.addStop(user)
        return bestElevator
    
    def printState(self):
        seperator = '\t'
        elStateList = []
        elTableRow = seperator
        for e in self.elevators:
            eIndex = self.elevators.index(e) + 1
            eIndexStr = f'E{eIndex}'
            elTableRow = elTableRow + f'{eIndexStr}{seperator}'
            elState = f'{eIndexStr}| {e.getState()}'
            elStateList.append(elState)
        print(elTableRow)
        for i in reversed(range(self.floors)):
            toPrint = f'F{i}:{seperator}'
            elevators_on_floor = list(filter(lambda x: x.floor == i, self.elevators))
            utilPrint = [f'[{e.getDirection()}]' if e in elevators_on_floor else '[ ]' for e in self.elevators]
            utilPrint = seperator.join(utilPrint)
            toPrint = toPrint + utilPrint
            print(toPrint)
        print('\n'.join(elStateList))