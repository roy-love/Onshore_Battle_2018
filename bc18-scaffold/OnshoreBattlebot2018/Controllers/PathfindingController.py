import random
import sys
import traceback

# Given a robot and destination, determines the best route to take
# Returns an array of directions to the calling robot
# Robot will follow the given directions until it determines that it needs to recalculate its path
# This is far more efficient than running Pathfinding every turn and more adaptive than running it once only
# May implement multiple pathfinding methods and determine which to use based upon what's needed or the distance
class PathfindingController:
	def __init__(self, gameController, mapController):
		self.gameController = gameController
		self.mapController = mapController