import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Healer(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Healer)

	def run(self):
		self.UpdateMission()

		if not self.mission is None:	
			if self.mission.action == Missions.Idle:
				self.Idle()
			
			elif self.mission.action == Missions.RandomMovement:
				self.OneRandomMovement()

			elif self.mission.action == Missions.HealTarget:
				if not self.performSecondAction and self.targetLocation is None:
					if self.path is None or len(self.path) == 0:
						#print("Path is null.  Making a new one")
						self.targetLocation = self.mission.info.mapLocation

						#print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
						self.UpdatePathToTarget()
				
				if self.HasReachedDestination():
					# harvest at the current map location: 0 = Center
					if self.tryHeal(self.mission.info.unitId):
						self.ResetMission()
				else:
					self.FollowPath()
				

			#Attacks nearby units
			nearby = self.gameController.sense_nearby_units(self.unit.location.map_location(), 2)
			for other in nearby:
				if other.team != self.gameController.team() and self.gameController.is_attack_ready(self.unit.id) \
				and self.gameController.can_attack(self.unit.id, other.id):
					print('Knight {} attacked a thing!'.format(self.unit.id))
					self.gameController.attack(self.unit.id, other.id)
					break
		
  
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
