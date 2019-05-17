class Environment():
    def __init__(self, floors):
        self.floors = floors + 1
        self.turns = 0
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
        elevator.removeFromPath(user)
        user.takeStairs()
        return user
    
    def printState(self):
        seperator = '\t'
        elStateList = []
        uStateList = []
        elTableRow = seperator + seperator
        print(f'== TURN {self.turns} ==')
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
            toPrintSeperator = seperator + seperator if i < 10 else seperator
            toPrint = f'F{i}:{toPrintSeperator}'
            elevators_on_floor = list(filter(lambda x: x.floor == i, self.elevators))
            utilPrint = [f'[{e.getDirection()}]' if e in elevators_on_floor else '[ ]' for e in self.elevators]
            utilPrint = seperator.join(utilPrint)
            toPrint = toPrint + utilPrint
            print(toPrint)
        print('\n'.join(elStateList))
        print('\n'.join(uStateList))
    
    def run(self):
        self.turns = self.turns + 1
        for elevator in self.elevators:
            elevator.move()
        for user in self.users:
            user.move()
        self.printState()

    def autoRun(self):
        while any([len(e.destinations) for e in self.elevators]):
            self.run()

    def exit(self):
        print(f'== METRICS ==')
        print(f'Turns: {self.turns}')
        for elevator in self.elevators:
            [tL, tW, tP, tU] = elevator.metrics()
            eIndex = self.elevators.index(elevator)
            print(f'E{eIndex}')
            print(f'With no light: {tL}')
            print(f'By max weight: {tW}')
            print(f'By path: {tP}')
            print(f'By users: {tU}')
