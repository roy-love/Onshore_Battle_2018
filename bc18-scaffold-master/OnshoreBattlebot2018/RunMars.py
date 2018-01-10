import battlecode as bc
import random
import sys
import traceback

from Controllers import *
from Entities import *

class RunMars:

	# Initialize controllers
	# Initialize all class variables
	# Only include code that should be initialized once at the beginning of the match
	def __init__(self, gameController):
      self.gameController = gameController
	  self.mapController = Controllers.MapController.MapController()
	  self.strategyController = Controllers.StrategyController.StrategyController(mapController)
	  self.researchTreeController = Controllers.ResearchTreeController.ResearchTreeController(strategyController)
	  self.buildController = Controllers.BuildController.BuildController(mapController, strategyController)
	  self.unitController = Controllers.UnitController.UnitController(strategyController)
	  self.targettingController = Controllers.TargettingController.TargettingController(mapController, strategyController)
	  self.pathfindingController = Controllers.PathfindingController.PathfindingController(mapController)
	  self.enemyTrackingController = Controllers.EnemyTrackingController.EnemyTrackingController()
	  
	  self.round = gameController.round()
	 
	# Runs once per turn for this planet only
	def Run(self):
		#Do Mars turn things here