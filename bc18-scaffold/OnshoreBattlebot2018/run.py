import battlecode as bc
import random
import sys
import traceback

from RunEarth import RunEarth

print("Starting Onshore Battlecode 2018 Player")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gameController = bc.GameController()
Planets = bc.Planet
my_team = gameController.team()

runEarth = RunEarth(gameController)
#runMars = RunMars(gameController)

# Main game loop
# Avoid placing additional code here if possible
while True:
    try:
        if gameController.planet() == Planets.Earth:
            print('Running Earth Turn')
            runEarth.Run()
        else:	
            print('Running Mars Turn')
			#runMars.Run()
		
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gameController.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()