import battlecode as bc
import random
import sys
import traceback

class IStructure:
	def __init__(self, gameController, unitController, unit,missionController):
		self.gameController = gameController
		self.unitController = unitController
		self.missionController = missionController
		self.unit = unit
		self.mission = None

	def UpdateMission(self):
		if self.unit.structure_is_built() and self.mission == None:
			self.mission = self.missionController.GetMission(self.unit.unit_type)
			self.missionStartRound = self.gameController.round()
			self.targetLocation = None
			print("Structure with id {} obtaining new mission {}".format(self.unit.id,self.mission.action))	