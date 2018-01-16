import random
import sys
import traceback
import battlecode as bc
from enum import Enum
from .StrategyController import *
from Strategies import *


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
        
        #Mission strategy references
        self.defaultMissions = DefaultMissions(gameController)

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
            return self.defaultMissions.CreateNewWorkerMission()

        elif self.strategyController.unitStrategy == UnitStrategies.WorkerRush:
    
    def __CreateNewHealerMission__(self):

        if self.strategyController.unitStrategy == UnitStrategies.Default:
            return self.defaultMissions.CreateNewHealerMission()

    
    def __CreateNewCombatMission__(self):

        if self.strategyController.unitStrategy == UnitStrategies.Default:
            return self.defaultMissions.CreateNewCombatMission()

    def __CreateNewFactoryMission__(self):
        
        if self.strategyController.unitStrategy == UnitStrategies.Default:
            return self.defaultMissions.CreateNewFactoryMission()
