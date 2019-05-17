class Environment():
    def __init__(self, floors):
        self.floors = floors + 1
        self.elevators = []
        self.users = []

    def addUser(self, user):
        self.users.append(user)
        print(f'U{len(self.users)}| {user.getState()}')
    
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
        print(f'E{len(self.elevators)}| {elevator.getState()}')

    def bestFitElevator(self, user):
        utils = []
        for elevator in self.elevators:
            utils.append(elevator.calcUtil(user))
        print(f'Utils: {utils}')
        maxUtil = max(utils)
        i = utils.index(maxUtil)
        return self.elevators[i]

    def requestElevator(self, user, destinationFloor):
        user.requestElevator(destinationFloor)
        elevator = self.bestFitElevator(user)
        elevator.addStop(user)
        user.setElevator(elevator)
        return elevator

    def takeStairs(self, user):
        elevator = user.elevator
        user.takeStairs()
        elevator.removeFromPath(user)
        return user
    
    def printState(self):
        seperator = '\t'
        elStateList = []
        uStateList = []
        elTableRow = seperator
        for e in self.elevators:
            eIndex = self.elevators.index(e) + 1
            eIndexStr = f'E{eIndex}'
            elTableRow = elTableRow + f'{eIndexStr}{seperator}'
            elState = f'{eIndexStr}| {e.getState()}'
            elStateList.append(elState)
        for u in self.users:
            uIndex = self.users.index(u) + 1
            uIndexStr = f'U{uIndex}'
            uState = f'{uIndexStr}| {u.getState()}'
            uStateList.append(uState)
        print(elTableRow)
        for i in reversed(range(self.floors)):
            toPrint = f'F{i}:{seperator}'
            elevators_on_floor = list(filter(lambda x: x.floor == i, self.elevators))
            utilPrint = [f'[{e.getDirection()}]' if e in elevators_on_floor else '[ ]' for e in self.elevators]
            utilPrint = seperator.join(utilPrint)
            toPrint = toPrint + utilPrint
            print(toPrint)
        print('\n'.join(elStateList))
        print('\n'.join(uStateList))
    
    def run(self):
        for elevator in self.elevators:
            elevator.move()
        for user in self.users:
            user.move()
        self.printState()

    def autoRun(self):
        while any([len(e.destinations) for e in self.elevators]):
            self.run()

    def exit(self):
        turns = 0
        turnsWithNoLight = 0
        turnsSavedByMaxWeight = 0
        turnsSavedByPath = 0
        turnsSavedByUsers = 0
        for elevator in self.elevators:
            [t, tL, tW, tP, tU] = elevator.metrics()
            turns = turns + t
            turnsWithNoLight = turnsWithNoLight + tL
            turnsSavedByMaxWeight = turnsSavedByMaxWeight + tW
            turnsSavedByPath = turnsSavedByPath + tP
            turnsSavedByUsers = turnsSavedByUsers + tU
        print(f'Turns: {turns}')
        print(f'Turns Saved')
        print(f'With no light: {turnsWithNoLight}')
        print(f'By max weight: {turnsSavedByMaxWeight}')
        print(f'By path: {turnsSavedByPath}')
        print(f'By users: {turnsSavedByUsers}')
