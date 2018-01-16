import random
import sys
import traceback
import battlecode as bc
from .IRobot import IRobot

class Healer(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Healer)

	def run(self):
		super(Healer,self).UpdateMission()

		if self.mission == "Walk Randomly":
			print("walking randomly")
			if self.path == None or len(self.path) == 0:
				print("Path is null.  Making a new one")
				self.targetLocation = self.unit.location.map_location().clone()
				self.targetLocation.x += 3
				self.targetLocation.y += 2

				print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
				self.UpdatePathToTarget()
				self.FollowPath()
		return super(Healer, self).run()
  
	def tryHeal(self, targetUnitId):
		#TODO check heat is low enough
		if not self.gameController.can_heal(self.unit.id, targetUnitId):
			print ("Healer [{}] cannot heal the target [{}]".format(self.unit.id, targetUnitId))
			return False

		self.gameController.heal(self.unit.id, targetUnitId)
		return True

	def tryOvercharge(self, targetUnitId):
		#TODO check has research
		
		#Check cooldown of Overcharge ability
		if not self.gameController.is_overcharge_ready(self.unit.id):
			print("Overcharge is not ready for Healer [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_overcharge(self.unit.id, targetUnitId):
			print("Healer [{}] cannot Overcharge the target [{}]".format(self.unit.id, targetUnitId))
			return False

		self.gameController.overcharge(self.unit.id, targetUnitId)
		return True
