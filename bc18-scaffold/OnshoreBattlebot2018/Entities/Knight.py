import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Knight(IRobot):
	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Knight)
		self.mission = None
		self.targetLocation = None
		self.path = None
		self.IsGarrisoned = False


	def run(self):

		#if not self.IsGarrisoned:
		self.UpdateMission()
		
		if self.mission.action == Missions.Idle:
			print("worker idle!")
			if  self.gameController.round >= self.missionStartRound + 5:
				self.ResetMission()
		
		elif self.mission.action == Missions.RandomMovement:
			print("walking randomly")
			if self.targetLocation is None:
				if self.path is None or len(self.path) == 0:
					#print("Path is null.  Making a new one")
					self.targetLocation = self.unit.location.map_location().clone()
					x = random.randint(-3,3)
					y = random.randint(-3,3)
					self.targetLocation.x += x
					self.targetLocation.y += y

					#print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
					self.UpdatePathToTarget()
			
			self.FollowPath()
			if self.HasReachedDestination():
				self.ResetMission()

		elif self.mission.action == Missions.DestoryTarget:
			
			#TODO Determine what to do when mining
			if not self.performSecondAction and self.targetLocation is None:
				if self.path is None or len(self.path) == 0:
					#print("Path is null.  Making a new one")
					self.targetLocation = self.mission.info.mapLocation

					#print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
					self.UpdatePathToTarget()
			
			if self.HasReachedDestination():
				# harvest at the current map location: 0 = Center
				self.tryAttack(self.mission.info.unitId)
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
		

	def IsEnemySighted(self):
		#TODO determine if this unit is able to see an enemy.
		#TODO refactor code to IRobot so that all robots can sight enemies.
		pass

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Knight [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		return True
	

	def tryJavelin(self, targetRobotId):
		#TODO check has research

		if not self.gameController.is_javelin_ready(self.unit.id):
			print("Javelin is not ready for knight [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_javelin(self.unit.id, targetRobotId):
			print("Knight [{}] cannot javelin target [{}]".format(self.unit.id, targetRobotId))
			return False

		self.gameController.javelin(self.unit.id, targetRobotId)
		return True