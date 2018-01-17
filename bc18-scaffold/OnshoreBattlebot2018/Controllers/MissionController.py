import random
import sys
import traceback

import battlecode as bc
from enum import Enum
from .StrategyController import *


class Missions(Enum):
    """These are the missions"""
    Idle = 0
    RandomMovement = 1 # Assign location to move to
    Mining = 2 # Assign location to mine
    FollowUnit = 3 # Assign Unit to follow
    Scout = 4 # Assign location to scout
    Patrol = 5 # Assign two locations to partrol
    DestroyTarget = 6 # Assign unit to destroy
    DefendTarget = 7 # Assign unit to defend
    Build = 8 # Assign location to build a factory
    CreateBlueprint = 9 # Assign location to lay down blueprint
    TrainBot = 10 # Instruct Factory to build a bot
    BuildRocket = 11 # Instruct Factory to build a rocket
    Garrison = 12 # Assign target factory to garrison
    HealTarget = 13 # Assign target to heal
    GoToRocket = 14 # Assign rocket and location
    LoadRocket = 14 # Assign unit to load
    UnloadRocket = 15 # Assign rocket to unload
    LuanchRocket = 16 # Assign rocket

class MissionTypes(Enum):
    """These are the mission types"""
    Worker = 0
    Healer = 1
    Combat = 2
    Factory = 3
    Rocket = 4

class Mission:
    """These are the Missions"""
    def __init__(self):
        self.action = None
        self.info = None

class MissionInfo:
    """These are the mission info"""
    def __init__(self):
        self.map_location = None
        self.unit_id = None
        self.unit = None
        self.isRocket = False

# Controller that handles the creation and managment of missions
class MissionController:
    """This is the mission controller"""
    def __init__(self, gameController, strategyController, mapController, researchTreeController):
        self.game_controller = gameController
        self.strategy_controller = strategyController
        self.map_controller = mapController
        self.researchTreeController = researchTreeController

        self.combat_missions = []
        self.healer_missions = []
        self.worker_missions = []
        self.factory_missions = []
        self.rocket_missions = []

        self.rocketCount = 0
        self.MustBuildRocket = False
        self.structureNeedsBuild = False

    # Adds a new mission created by outside source
    def AddMission(self, mission, mission_type, mission_info):
        """This adds missions"""
        new_mission = Mission()
        new_mission.action = mission
        new_mission.info = mission_info
        if mission_type == MissionTypes.Worker:
            self.worker_missions.append(new_mission)
        elif mission_type == MissionTypes.Healer:
            self.healer_missions.append(new_mission)
        elif mission_type == MissionTypes.Factory:
            self.factory_missions.append(new_mission)
        elif mission_type == MissionTypes.Rocket:
            self.rocket_missions.append(new_mission)
        else:
            self.combat_missions.append(new_mission)

    #Pops the highest priority mission for the given unit off the queue and returns it
    def get_mission(self, unit_type):
        """This gets the mission"""
        # Return a mission based on the type of unit
        # The mission will be based on the current strategy

        if unit_type == bc.UnitType.Worker:
            if len(self.worker_missions) > 0:
                print("Worker mission assigned {}".format(self.worker_missions[0].action))
                return self.worker_missions.pop(0)
            else:
                return self.__create_new_worker_mission__()
        elif unit_type == bc.UnitType.Healer:
            if len(self.healer_missions) > 0:
                print("Healer mission assigned")
                return self.healer_missions.pop(0)
            else:
                return self.__create_new_healer_mission__()
        elif unit_type == bc.UnitType.Factory:
            if len(self.factory_missions) > 0:
                print("Factory mission assigned")
                return self.factory_missions.pop(0)
            else:
                return self.__create_new_factory_mission__()
        elif unit_type == bc.UnitType.Rocket:
            if len(self.factory_missions) > 0:
                print("Factory mission assigned")
                return self.rocket_missions.pop(0)
            else:
                return self.__create_new_factory_mission__()
        else:
            if len(self.combat_missions) > 0:
                print("Combat mission assigned")
                return self.combat_missions.pop(0)
            else:
                return self.__create_new_combat_mission__()

    def CreateBuildMission(self,structure):
        new_mission = Mission()
        new_mission.action = Missions.Build
        new_mission.info = MissionInfo()
        new_map_location = structure.location.map_location().clone()
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        if x == 0 and y == 0:
            x = 1
        new_mission.info.map_location = bc.MapLocation(bc.Planet.Earth,new_map_location.x + x,new_map_location.y + y )
        new_mission.info.map_location = new_map_location
        new_mission.info.unit_id = structure.id
        new_mission.info.unit = structure
        if structure.unit_type == bc.UnitType.Rocket:
            new_mission.info.isRocket = True
        return new_mission

    def CreateFactoryBlueprintMission(self, location):
        new_mission = Mission()
        new_mission.action = Missions.CreateBlueprint
        new_mission.info = MissionInfo()
        #map_location = bc.MapLocation(self.game_controller.planet(), 0, 0)
        #map_location.x = random.randint(0, 12)
        #map_location.y = random.randint(0, 12)
        new_mission.info.map_location = location # TODO get open location from the map
        
        return new_mission

    def CreateRocketBlueprintMission(self,location):
        new_mission = Mission()
        new_mission.action = Missions.CreateBlueprint
        new_mission.info = MissionInfo()
        new_mission.info.isRocket = True
       # map_location = bc.MapLocation(self.game_controller.planet(), 0, 0)
       # map_location.x = random.randint(0, 12)
        #map_location.y = random.randint(0, 12)
        new_mission.info.map_location = location # TODO get open location from the map
        #self.rocketCount += 1
        #self.MustBuildRocket = False
        return new_mission

    def __create_new_worker_mission__(self):
        #Determine what mission to assign based on the current strategy
        if self.strategy_controller.unitStrategy == UnitStrategies.Default:

            #Mine Karbonite
            new_mission = Mission()
            new_mission.action = Missions.Mining
            map_location = bc.MapLocation(self.game_controller.planet(), 0, 0)
            map_location.x = random.randint(0, 10)
            map_location.y = random.randint(0, 10)
            new_mission.info = map_location # TODO get mining location from map
            return new_mission

    def __create_new_healer_mission__(self):

        if self.strategy_controller.unitStrategy == UnitStrategies.Default:
            chance = random.randint(0, 100)
            if chance > 50:
                if len(self.game_controller.my_units()) > 1:
                    new_mission = Mission()
                    new_mission.action = Missions.FollowUnit
                    new_mission.info = self.game_controller.my_units()[0]
                    # TODO creat logic for aquiring a target to follow
                    return Missions.FollowUnit
                else:
                    new_mission = Mission()
                    new_mission.action = Missions.Idle
                    return new_mission
            else:
                new_mission = Mission()
                new_mission.action = Missions.Idle
                return new_mission

    def __create_new_combat_mission__(self):

        if self.strategy_controller.unitStrategy == UnitStrategies.Default:
            chance = random.randint(1, 100)
            if chance > 0:
                new_mission = Mission()
                new_mission.action = Missions.RandomMovement
                return new_mission
            elif chance > 25:
                new_mission = Mission()
                new_mission.action = Missions.Patrol
                new_mission.info = MissionInfo()
                map_location = bc.MapLocation(self.game_controller.planet(), 0, 0)
                #TODO better patrol location
                map_location.x = random.randint(0, 20)
                map_location.y = random.randint(0, 20)
                new_mission.info.map_location = map_location
                return new_mission
            else:
                new_mission = Mission()
                new_mission.action = Missions.Idle
                return new_mission

    def __create_new_factory_mission__(self):
        production_chance = None
        if self.strategy_controller.unitStrategy == UnitStrategies.Default:
            production_chance = [50, 0, 40, 20, 0] # Workers and Knights
            #production_chance = [80, 60, 40, 20, 0]
            #Balanced production chance

        chance = random.randint(1, 100)
        #if not self.MustBuildRocket and chance > production_chance[0]:
        #    new_mission = Mission()
        #    new_mission.action = Missions.TrainBot
        #    new_mission.info = bc.UnitType.Worker
        #    return new_mission
        #elif not self.MustBuildRocket and  chance > production_chance[1]:
        #    new_mission = Mission()
        #    new_mission.action = Missions.TrainBot
        #    new_mission.info = bc.UnitType.Knight
        #    return new_mission
        #elif not self.MustBuildRocket and  chance > production_chance[2]:
        #    new_mission = Mission()
        #    new_mission.action = Missions.TrainBot
        #    new_mission.info = bc.UnitType.Healer
        #    return new_mission
        if not self.MustBuildRocket:
            new_mission = Mission()
            new_mission.action = Missions.TrainBot
            new_mission.info = bc.UnitType.Ranger
            return new_mission
        #elif not self.MustBuildRocket and  chance > production_chance[4]:
        #    new_mission = Mission()
        #    new_mission.action = Missions.TrainBot
        #    new_mission.info = bc.UnitType.Mage
        #    return new_mission
        else:
            new_mission = Mission()
            new_mission.action = Missions.Idle
            return new_mission

    def __create_new_rocket_mission__(self):
    
        if self.strategy_controller.unitStrategy == UnitStrategies.Default:
            chance = random.randint(1, 100)
            if chance > 0:
                new_mission = Mission()
                new_mission.action = Missions.RandomMovement
                return new_mission
            elif chance > 25:
                new_mission = Mission()
                new_mission.action = Missions.Patrol
                new_mission.info = MissionInfo()
                map_location = bc.MapLocation(self.game_controller.planet(), 0, 0)
                #TODO better patrol location
                map_location.x = random.randint(0, 20)
                map_location.y = random.randint(0, 20)
                new_mission.info.map_location = map_location
                return new_mission
            else:
                new_mission = Mission()
                new_mission.action = Missions.Idle
                return new_mission