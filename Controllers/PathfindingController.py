import random
import sys
import traceback

# Given a robot and destination, determines the best route to take
# Returns an array of directions to the calling robot
# Robot will follow the given directions until it determines that it needs to recalculate its path
# This is far more efficient than running Pathfinding every turn and more adaptive than running it once only
# May implement multiple pathfinding methods and determine which to use based upon what's needed or the distance
class PathfindingController:
    """This is the Pathfinding Controller"""
    def __init__(self, gameController, mapController):
        self.game_controller = gameController
        self.map_controller = mapController

    def find_path_to(self, current_location, destination):
        """This finds the path to"""
        #print("starting pathfinding")
        path = []
        while current_location != destination:
            direction = current_location.direction_to(destination)
            #print("next direction is {}".format(direction))
            path.append(direction)
            #print("direction count is {}".format(len(path)))
            current_location = current_location.add(direction)
        #print("returning path")
        return path
