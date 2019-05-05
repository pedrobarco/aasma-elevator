class Environment():
    def __init__(self, floors):
        self.floors = floors
        self.elevators = []
        self.users = []

    def addUser(self, user):
        self.users.append(user)

    def addElevator(self, elevator, floors=None):
        if floors:
            self.floors = floors
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
