import battlecode as bc
import random
import sys
import traceback

# Keeps track of friendly units and structures
# Utilize the Map and Strategy controllers for data
# Set build priorities and locations
# Store in a build queue (thingToBuild, whereToBuild)
# Workers access this class to determine what to build next
class BuildController:
	def __init__(self, gameController, mapController, strategyController):
      self.gameController = gameController
	  self.mapController = mapController
	  self.strategyController = strategyController