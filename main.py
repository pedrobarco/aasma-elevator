import sys
from Environment import Environment
from User import User
from Elevator import Elevator
UP = 1
DOWN = -1
IDLE = 0



def decide(env, args):
    command = args[0]
    if (command == 'exit'):
        exit(0)
    elif (command == 'elevator'):
        maxWeight = int(args[1])
        floor = int(args[2]) if len(args) > 2 else 0
        elevator = Elevator(maxWeight, floor)
        env.addElevator(elevator)
        print(f'U{len(env.elevators)}| {elevator.getState()}')
    elif (command == 'user'):
        weight = int(args[1])
        floor = int(args[2]) if len(args) > 2 else 0
        user = User(weight, floor)
        env.addUser(user)
        print(f'U{len(env.users)}| {user.getState()}')
    elif (command == 'state'):
        env.printState()
    
def main():
    args = sys.stdin.readline().strip().split(' ')
    env = Environment(int(args[0]))
    running = True
    while (running):
        args = sys.stdin.readline().strip().split(' ')
        decide(env, args)

if __name__ == "__main__":
    main()
