import random
import sys
import traceback

from Controllers import *
from Entities import *

class RunEarth:

	# Initialize controllers
	# Initialize all class variables
	# Only include code that should be initialized once at the beginning of the match
	def __init__(self, gameController):
		self.gameController = gameController
		self.mapController = MapController(gameController)
		self.enemyTrackingController = EnemyTrackingController(gameController)
		self.strategyController = StrategyController(gameController, self.mapController, self.enemyTrackingController)
		self.researchTreeController = ResearchTreeController(gameController, self.strategyController)
		self.buildController = BuildController(gameController, self.mapController, self.strategyController)
		self.pathfindingController = PathfindingController(gameController, self.mapController)
		self.missionController = MissionController(gameController,self.strategyController)
		self.unitController = UnitController(gameController, self.strategyController, self.pathfindingController, self.missionController)
		self.targettingController = TargettingController(gameController, self.mapController, self.strategyController)
	  
	 
	# Runs once per turn for this planet only
	def Run(self):
		self.round = self.gameController.round()
		if self.round == 1:
			print("First round on Earth.  Initializing map")
			self.mapController.InitializeEarthMap()

			print("Selecting default strategy")
			self.strategyController.SetDefaultStrategy()
		else:
			print("Round {}".format(self.round))
			print("Setting strategy for the turn")
			self.strategyController.UpdateStrategy()
		
		print("Update research queue")
		self.researchTreeController.UpdateQueue()
		
		print("Updating units.  Synching between game units and player entities.")
		self.unitController.UpdateUnits()
 
		print("Running all units")
		self.unitController.RunUnits()
