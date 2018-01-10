import random
import sys
import traceback

# Uses all known information from various controllers to determine the current strategy
# Returns an array of values, each detailing a different part of the strategy
# Example (using fake situations and values):  {"Zerg","Knights","Separate"}
#	Zerg = Ignore rockets research and building.  Focusing on building lots of using and killing the enemy quickly
#	Knights = Focus on building primarily or only knights, due to either terrain or opponent's unit choices
#	Separate = Knights move towards the enemy with space between them.  Possibly because the opponent has lots of AOE mages 
# Start by simply returning {"Default"} until we get the basics finished.
class StrategyController:
	def __init__(self, gameController, mapController):
		self.gameController = gameController
		self.mapController = mapController