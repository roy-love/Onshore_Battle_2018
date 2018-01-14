import random
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Mage(IRobot):

	# change init definition to include any controllers needed in the instructor as we need them
	# For example:  it will eventually need to access the Targeting and Pathfinding controllers
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
		super().__init__(gameController, unitController, pathfindingController, missionController, unit,bc.UnitType.Mage)

	def run(self):
		self.UpdateMission()

		if not self.mission is None:	
			if self.mission.action == Missions.Idle:
				self.Idle()
			
			elif self.mission.action == Missions.RandomMovement:
				self.RandomMovement()

			elif self.mission.action == Missions.DestoryTarget:
				self.DestroyTarget()
				

			#Attacks nearby units
			nearby = self.gameController.sense_nearby_units(self.unit.location.map_location(), 2)
			for other in nearby:
				if other.team != self.gameController.team() and self.gameController.is_attack_ready(self.unit.id) \
				and self.gameController.can_attack(self.unit.id, other.id):
					print('Knight {} attacked a thing!'.format(self.unit.id))
					self.gameController.attack(self.unit.id, other.id)
					break

	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Mage [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		return True

	def tryBlink(self, destination):
		#TODO check has research

		#Check cooldown of Blink ability
		if not self.gameController.is_blink_ready(self.unit.id):
			print("Blink is not ready for Mage [{}]".format(self.unit.id))
			return False

		if not self.gameController.can_blink(self.unit.id, destination):
			print("Mage [{}] cannot blink to the target location")
			return False

		self.gameController.blink(self.unit.id, destination)
		return True