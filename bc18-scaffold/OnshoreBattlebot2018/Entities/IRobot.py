import battlecode as bc
import random
import sys
import traceback


class IRobot:
	def __init__(self, gameController, unitController, pathfindingController, missionController, unit,unitType):
		self.gameController = gameController
		self.unitController = unitController
		self.pathfindingController = pathfindingController
		self.missionController = missionController

		#Reference to the BattleCode unit object that the server side code tracks
		self.unit = unit
		self.unitType = unitType

		#Current mission dictates the robot's actions for the turn
		self.mission = None

		#Location that the robot will move to, regardless of what the mission type is
		self.targetLocation = None

		#List of directions to reach the target location
		self.path = None

		#Round that the current mission started on.
		self.missionStartRound = 0

		#To allow for Missions that have a secondary action
		self.performSecondAction = False

		
	#Actions that will be run at the end of every robot's turn
	def run(self):
		pass

	def UpdateMission(self):
		if self.mission == None:
			self.mission = self.missionController.GetMission(self.unitType)
			self.missionStartRound = self.gameController.round()
			self.targetLocation = None
			print("Robot with id {} obtaining new mission {}".format(self.unit.id,self.mission.action))

	def ResetMission(self):
		self.performSecondAction = False
		self.mission = None

	#TODO Check that the next direction is still possible.  If not, recalculate
	def UpdatePathToTarget(self):
		if self.targetLocation is not None and (self.path is None or len(self.path) == 0):
			print("Creating new path from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
			self.path = self.pathfindingController.FindPathTo(self.unit.location.map_location(), self.targetLocation)
		

	def FollowPath(self):
			if len(self.path) > 0:
				direction = self.path[-1]
				print("Walking in direction {}".format(direction))
				if self.tryMove(direction):
					self.path.pop()
			else:
				print("destination reached")
				
				

	def HasReachedDestination(self):
		if self.targetLocation is None:
			return True
		else:
			if self.unit.location.map_location().x == self.targetLocation.x and \
				self.unit.location.map_location().y == self.targetLocation.y:
				self.targetLocation = None
				self.performSecondAction = True
				print("Robot with id {} has reached it's destination.".format(self.unit.id))
				return True
			else:
				print("Robot with id {} still moving to destination.".format(self.unit.id))
				return False

			
	def tryMove(self, direction):
		if not self.gameController.is_move_ready(self.unit.id):
			print("Move for Robot [{}] is not ready".format(self.unit.id))
			return False
		if not self.gameController.can_move(self.unit.id, direction):
			print("Robot [{}] cannot move in direction {}".format(self.unit.id, direction))
			return False
		
		self.gameController.move_robot(self.unit.id, direction)
		return True
	
	def tryAttack(self, targetRobotId):
		#TODO check heat is low enough
		if not self.gameController.can_attack(self.unit.id, targetRobotId):
			print("Bot [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
			return False
		
		self.gameController.attack(self.unit.id, targetRobotId)
		print("Bot [{}] attacked the target [{}]".format(self.unit.id, targetRobotId))
		return True
	
	def selfDestruct(self):
		"Robot [{}] self destructing".format(self.unit.id)
		self.gameController.disintegrate_unit(self.unit.id)

# Default Missions
	def Idle(self):
		print("bot idle!")
		if  self.gameController.round >= self.missionStartRound + 10:
			self.ResetMission()
	
	def RandomMovement(self):
		print("bot walking randomly")
		if self.targetLocation is None:
			if self.path is None or len(self.path) == 0:
				#print("Path is null.  Making a new one")
				self.targetLocation = self.unit.location.map_location().clone()
				x = random.randint(-5,5)
				y = random.randint(-5,5)
				self.targetLocation.x += x
				self.targetLocation.y += y

				#print("Wants to move from {},{} to {},{}".format(self.unit.location.map_location().x, self.unit.location.map_location().y, self.targetLocation.x, self.targetLocation.y))
				self.UpdatePathToTarget()
		
		self.FollowPath()
		if self.HasReachedDestination():
			self.ResetMission()

	def DestroyTarget(self):
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