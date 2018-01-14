import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IStructure import IStructure

class Factory(IStructure):
	def __init__(self, gameController, unitController, unit, missionController):
		super(Factory, self).__init__(gameController, unitController, unit, missionController)

		self.roundStartProduction = 0
		self.IsWorking = False
		self.directions = list(bc.Direction)

	def run(self):
		
		self.UpdateMission()

		if not self.mission is None:

			if self.mission.action == Missions.TrainBot:
				print ("Factory [{}] TRAIN_BOT {} {}".format(self.unit.id, self.IsWorking,self.unit.is_factory_producing()))
				if self.IsWorking and not self.unit.is_factory_producing():
					if self.tryUnloadUnits():
						print("Factory [{}] successfully unloaded a unit.".format(self.unit.id))
						self.mission = None
						self.IsWorking = False
				elif not self.IsWorking and self.tryProduceRobot(self.mission.info):
					self.IsWorking = True
				else:
					print("Factory [{}] Failed to produce robot.".format(self.unit.id))
			

	def tryProduceRobot(self, unitType):
		if self.unit.is_factory_producing():
			print("Factory [{}] occupied, producing [{}] with [{}] rounds left".format(self.unit.id, self.unit.factory_unit_type, self.unit.factory_rounds_left))
			return False

		#if not self.gameController.can_produce_robot(self.unit.id, unitType):
			print("Factory [{}] cannot produce the [{}]. Current Karbonite: {}".format(self.unit.id, unitType, self.gameController.karbonite()))
		#	return False

		self.gameController.produce_robot(self.unit.id, unitType)
		return True

	def tryGarrision(self, unitId):
		# TODO create garrision units function.
		return True

	def tryUnloadUnits(self):
		garrison = self.unit.structure_garrison()
		garrisonCount = len(garrison)
		if garrisonCount > 0:
			print("Factory [{}] garrisoned with [{}] units.".format(self.unit.id,garrisonCount))
			direction = random.choice(self.directions)
			if self.gameController.can_unload(self.unit.id,direction):
				print("Factory unloaded {} with id {}.".format(garrison[0],garrison[0]))
				self.gameController.unload(self.unit.id,direction)
				
				return True
			else:
				print("Factory with id {} failed to unload.".format(self.unit.id))
				return False
		else:
			return False