import sys
from Environment import Environment
from User import User
from Elevator import Elevator
UP = 1
DOWN = -1
IDLE = 0

def execute(env, args):
    command = args[0]
    if (command == 'init'):
        env.printState()
        global MOVING
        MOVING = True
    if (command == 'skip'):
        pass
    elif (command == 'exit'):
        exit(0)
    elif (command == 'elevator'):
        maxWeight = int(args[1])
        floor = int(args[2]) if len(args) > 2 else 0
        elevator = Elevator(maxWeight, floor)
        env.addElevator(elevator)
    elif (command == 'user'):
        weight = int(args[1])
        floor = int(args[2]) if len(args) > 2 else 0
        user = User(weight, floor)
        env.addUser(user)
    elif (command == 'request'):
        userId = int(args[1])
        floor = int(args[2])
        user = env.getUserById(userId)
        env.requestElevator(user, floor)
    elif (command == 'stairs'):
        userId = int(args[1])
        user = env.getUserById(userId)
        env.takeStairs(user)

def main():
    args = sys.stdin.readline().strip().split(' ')
    env = Environment(int(args[0]))
    global MOVING
    MOVING = False
    running = True
    while (running):
        args = sys.stdin.readline().strip().split(' ')
        execute(env, args)
        if (MOVING):
            env.run()
            env.printState()

if __name__ == "__main__":
    main()
