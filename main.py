from Environment import Environment
from User import User
from Elevator import Elevator
UP = 1
DOWN = -1
IDLE = 0


def main():
    env = Environment(5)
    e1 = Elevator(200, 5)
    e2 = Elevator(100)
    env.addElevator(e1)
    env.addElevator(e2)
    u1 = User(50)
    env.addUser(u1)
    env.requestElevator(u1, 5)


if __name__ == "__main__":
    main()
