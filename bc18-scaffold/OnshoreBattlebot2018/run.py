import battlecode as bc
import random
import sys
import traceback

from RunEarth import RunEarth
from RunMars import RunMars

print("Starting Onshore Battlecode 2018 Player")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
GAMECONTROLLER = bc.GameController()
PLANETS = bc.Planet
MY_TEAM = GAMECONTROLLER.team()

RUNEARTH = RunEarth(GAMECONTROLLER)
RUNMARS = RunMars(GAMECONTROLLER)

# Main game loop
# Avoid placing additional code here if possible
while True:
    try:
        if GAMECONTROLLER.planet() == PLANETS.Earth:
            print('Running Earth Turn')
            RUNEARTH.Run()
        else:
            print('Running Mars Turn')
            RUNMARS.Run()

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    GAMECONTROLLER.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
