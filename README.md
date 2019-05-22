# AASMA Elevators

AASMA Elevators is a Python project for simulating an intelligent environment with autonomous elevators.

## Installation

This project requires no installation. Use [git](https://git-scm.com/) command line tool to clone this repo or download it directly as a .zip [here](https://github.com/pedrobarco/aasma-elevator/archive/master.zip).

```bash
git clone https://github.com/pedrobarco/aasma-elevator
```

## Usage

```bash
python3 main.py # runs interactiely
python3 main.py [< in.txt] # uses in.txt instructions set as input 
python3 main.py [< in.txt] [> out.txt] # saves run to out.txt
```

This world has three objects/classes:
- Elevators: accept users floor requests
- Users: make elevator requests
- Environments: buildings with elevators and users

Our environment is managed by a turn-based intruction set, where the first step is creating an environment with users and elevators. Elevators and users are uniquely identified by their id. This identifier is generated at creation time, sequentially.
When the command `init` is used, the world starts and every instruction will be consumed as a new turn. In each turn the environment changes and so do the elevators and users.

```bash
10 # 10 floor building (must be the first instruction/line)
elevator 400 5
elevator 250 
user 70 1 # (userId = 1)
user 80 # (userId = 2)
init 
```

## Instruction Set

- NFLOORS
    - NFLOORS: building's number of floors **(first instruction/line)**
- elevator maxWeight [floor] 
   - maxWeight: elevator weight limit
   - floor: floor where elevator is created (defaults to 0)
- user weight [floor]
   - weight: user's weight 
   - floor: floor where user is created (defaults to 0)
- request userId floor
   - userId: user requesting a lift 
   - floor: user's destination floor
- stairs userId
   - userId: user taking the stairs
- init
    - initates turn-based environment moves
- skip 
    - skips a turn (same as no action)
- auto
    - skips turns until all elevator have no destinations
- exit
    - exits program, presenting collected metrics

## Metrics

Our project implements metrics that calculate how many turns has an elevator saved when compared to *normal* elevator system. These turns saved are divided into categories: 
- **ligth**: turns with elevators' ligths turn off
- **weight**: turns saved by rejecting a request that exceeded the weigth limit
- **path**: turns saved by repathing when users take stairs
- **users**: turns saved by users when the elevator idles in the mean floor (based on destination history)

## Samples

Samples are in the [samples/](https://github.com/pedrobarco/aasma-elevator/samples) directory. The samples present different scenarios where metrics and turns saved vary accordingly.