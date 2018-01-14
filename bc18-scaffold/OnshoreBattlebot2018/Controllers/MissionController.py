import random
import sys
import traceback

import battlecode as bc
from enum import Enum
from .StrategyController import *


class Missions(Enum):
    Idle = 0 
    RandomMovement = 1 # Assign location to move to
    Mining = 2 # Assign location to mine
    FollowUnit = 3 # Assign Unit to follow
    Scout = 4 # Assign location to scout
    Patrol = 5 # Assign two locations to partrol 
    DestroyTarget = 6 # Assign unit to destroy
    DefendTarget = 7 # Assign unit to defend
    BuildFactory = 8 # Assign location to build a factory
    CreateBlueprint = 9 # Assign location to lay down blueprint
    TrainBot = 10
    BuildRocket = 15
    Garrison = 16
    
    
class MissionTypes(Enum):
    Worker = 0
    Healer = 1
    Combat = 2
    Factory = 3

class Mission:
    def __init__(self):
        self.action = None
        self.info = None

class MissionInfo: 
    def __init__(self):
        self.mapLocation = None
        self.unitId = None  
        self.unit = None

# Controller that handles the creation and managment of missions
class MissionController:
    def __init__(self, gameController, strategyController, mapController):
        self.gameController = gameController
        self.strategyController = strategyController
        self.mapController = mapController

        self.combatMissions = []
        self.healerMissions = []
        self.workerMissions = []
        self.factoryMissions = []

    # Adds a new mission created by outside source
    def AddMission(self,mission,missionType,missionInfo):
        newMission = Mission()
        newMission.action = mission
        newMission.info = missionInfo
        if missionType == MissionTypes.Worker:
            self.workerMissions.append(newMission)
        elif missionType == MissionTypes.Healer:
            self.healerMissions.append(newMission)
        elif missionType == MissionTypes.Factory:
            self.factoryMissions.append(newMission)
        else:
            self.combatMissions.append(newMission)

    #Pops the highest priority mission for the given unit off the queue and returns it
    def GetMission(self,unitType):
        # Return a mission based on the type of unit
        # The mission will be based on the current strategy
        
        if unitType == bc.UnitType.Worker:
            if len(self.workerMissions) > 0:
                print("Worker mission assigned")
                return self.workerMissions.pop(0)
            else:
                return self.__CreateNewWorkerMission__()
        elif unitType == bc.UnitType.Healer:
            if len(self.healerMissions) > 0:
                print("Healer mission assigned")
                return self.healerMissions.pop(0)
            else:
                return self.__CreateNewHealerMission__()
        elif unitType == bc.UnitType.Factory:
            if len(self.factoryMissions) > 0:
                print("Factory mission assigned")
                return self.factoryMissions.pop(0)
            else:
                return self.__CreateNewFactoryMission__()
        else:
            if len(self.combatMissions) > 0:
                print("Combat mission assigned")
                return self.combatMissions.pop(0)
            else: 
                return self.__CreateNewCombatMission__()

    def __CreateNewWorkerMission__(self):
        #Determine what mission to assign based on the current strategy
        if self.strategyController.unitStrategy == UnitStrategies.Default:
            
            factoryCount = 0
            units = self.gameController.my_units()
            for other in units:
                if other.unit_type == bc.UnitType.Factory:
                    factoryCount += 1
            
            if factoryCount < 10:  
                newMission = Mission()
                newMission.action = Missions.CreateBlueprint
                mapLocation = bc.MapLocation(self.gameController.planet(),0,0)
                mapLocation.x = random.randint(0,10)
                mapLocation.y = random.randint(0,10)
                newMission.info = mapLocation # TODO get open location from the map
                return newMission
            elif self.gameController.karbonite() < 20:
                newMission = Mission()
                newMission.action = Missions.Mining
                mapLocation = bc.MapLocation(self.gameController.planet(),0,0)
                mapLocation.x = random.randint(0,10)
                mapLocation.y = random.randint(0,10)
                newMission.info = mapLocation # TODO get mining location from map
                return newMission
            else:
                newMission = Mission()
                newMission.action = Missions.Idle
                return newMission
    
    def __CreateNewHealerMission__(self):

        if self.strategyController.unitStrategy == UnitStrategies.Default:
            chance = random.randint(0,100)
            if chance > 50:
                if len(self.gameController.my_units()) > 1:
                    newMission = Mission()
                    newMission.action = Missions.FollowUnit
                    newMission.info = self.gameController.my_units().pop(0) # TODO creat logic for aquiring a target to follow
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

        if self.strategyController.unitStrategy == UnitStrategies.Default:
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
        productionChance = None
        if self.strategyController.unitStrategy == UnitStrategies.Default:
            productionChance = [80,60,40,20,0]
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
