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
            