import battlecode as bc
import random
from .MissionStructures import *
from Controllers.StrategyController import UnitStrategies


class DefaultMissions():
    def __init__(self,gameController):
        self.gameController = gameController
   
    def CreateNewWorkerMission(self):
        #Determine what mission to assign based on the current strategy
        factoryCount = 0
        units = self.gameController.my_units()
        for other in units:
            if other.unit_type == bc.UnitType.Factory:
                factoryCount += 1
        chance = random.randint(1,100)
        if factoryCount < 5 and chance > 50:  
            newMission = Mission()
            newMission.action = Missions.CreateBlueprint
            mapLocation = bc.MapLocation(self.gameController.planet(),0,0)
            mapLocation.x = random.randint(0,12)
            mapLocation.y = random.randint(0,12)
            newMission.info = mapLocation # TODO get open location from the map
            return newMission
        elif self.gameController.karbonite() < 20 and chance > 25:
            newMission = Mission()
            newMission.action = Missions.Mining
            mapLocation = bc.MapLocation(self.gameController.planet(),0,0)
            mapLocation.x = random.randint(0,10)
            mapLocation.y = random.randint(0,10)
            newMission.info = mapLocation # TODO get mining location from map
            return newMission
        elif True:
            newMission = Mission()
            newMission.action = Missions.RandomMovement
            return newMission
        else:
            newMission = Mission()
            newMission.action = Missions.Idle
            return newMission

    def CreateNewHealerMission(self):

        chance = random.randint(0,100)
        if chance > 50:
            if len(self.gameController.my_units()) > 1:
                newMission = Mission()
                newMission.action = Missions.FollowUnit
                newMission.info = self.gameController.my_units()[0] # TODO creat logic for aquiring a target to follow
                return Missions.FollowUnit
            else:
                newMission = Mission()
                newMission.action = Missions.Idle
                return newMission
        else:
            newMission = Mission()
            newMission.action = Missions.Idle
            return newMission

    def __CreateNewCombatMission__(self):

        chance = random.randint(1,100)
        if chance > 0:
            newMission = Mission()
            newMission.action = Missions.RandomMovement
            return newMission
        elif chance > 25:
            newMission = Mission()
            newMission.action = Missions.Patrol
            newMission.info = MissionInfo()
            mapLocation = bc.MapLocation(self.gameController.planet(),0,0) #TODO better patrol location
            mapLocation.x = random.randint(0,20)
            mapLocation.y = random.randint(0,20)
            newMission.info.mapLocation = mapLocation
            return newMission
        else:
            newMission = Mission()
            newMission.action = Missions.Idle
            return newMission
            

    def __CreateNewFactoryMission__(self):
        
        productionChance = [80,60,40,20,0] # Workers and Knights
        #productionChance = [80,60,40,20,0]
        #Balanced production chance

        chance = random.randint(1,100)
        if chance > productionChance[0]:
            newMission = Mission()
            newMission.action = Missions.TrainBot
            newMission.info = bc.UnitType.Worker
            return newMission
        elif chance > productionChance[1]:
            newMission = Mission()
            newMission.action = Missions.TrainBot
            newMission.info = bc.UnitType.Knight
            return newMission
        elif chance > productionChance[2]:
            newMission = Mission()
            newMission.action = Missions.TrainBot
            newMission.info = bc.UnitType.Healer
            return newMission
        elif chance > productionChance[3]:
            newMission = Mission()
            newMission.action = Missions.TrainBot
            newMission.info = bc.UnitType.Ranger
            return newMission
        elif chance > productionChance[4]:
            newMission = Mission()
            newMission.action = Missions.TrainBot
            newMission.info = bc.UnitType.Mage
            return newMission
        else:
            newMission = Mission()
            newMission.action = Missions.Idle
            return newMission