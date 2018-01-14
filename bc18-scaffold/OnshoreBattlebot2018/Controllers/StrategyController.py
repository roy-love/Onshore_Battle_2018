from enum import Enum


# Uses all known information from various controllers to determine the current strategy
# Stores the values from enums, for easy access
# Start by simply returning {"Default"} until we get the basics finished.
class StrategyController:
	def __init__(self, gameController, mapController, enemyTrackingController):
		self.gameController = gameController
		self.mapController = mapController
		self.enemyTrackingController = enemyTrackingController

		self.macroStrategy = MacroStrategies.Default
		self.unitStrategy = UnitStrategies.Default

	#TODO set default strategy based upon the current map
	def SetDefaultStrategy(self):
		self.macroStrategy = MacroStrategies.Default
		self.unitStrategy = UnitStrategies.Default

	#TODO update strategy based upon changes to the map, enemies seen, or any other criteria
	def UpdateStrategy(self):
		
		pass

#Add more strategy types as needed
class MacroStrategies(Enum):
	Default = 0
	ZergRush = 1
	Turtle = 2
	MarsRush = 3

class UnitStrategies(Enum):
	Default = 0
	WorkerRush = 1
	KnightRush = 2
	MageRush = 3
	RangerRush = 4
	HealerRush = 5