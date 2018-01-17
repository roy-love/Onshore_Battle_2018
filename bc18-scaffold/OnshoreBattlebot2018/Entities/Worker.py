import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot


class Worker(IRobot):
    """This is the Worker robot"""
    # change init definition to include any controllers needed in the instructor as we need them
    # For example:  it will eventually need to access the Targeting and Pathfinding controllers
    def __init__(self, gameController, unitController, \
    pathfindingController, missionController, unit,mapController):
        super().__init__(gameController, unitController, \
        pathfindingController, missionController, unit, bc.UnitType.Worker,mapController)
    

    #overrides IRobot run method
    def run(self):
        if not self.unit.location.is_in_garrison() and not self.unit.location.is_in_space():
            
            if self.unit_controller.workerCount < 10:
                direction = random.choice(self.directions)
                if self.game_controller.can_replicate(self.unit.id, direction):
                    self.try_replication(direction)
            
            #print("Worker bot with id {} run() called.".format(self.unit.id))
            self.update_mission()
            
            #if self.mission.action == Missions.Idle:
            #    self.idle()

            #if self.mission.action == Missions.RandomMovement:
            #   self.one_random_movement()

            if self.mission.action == Missions.Mining:
                self.one_random_movement()
                if self.game_controller.can_harvest(self.unit.id, bc.Direction.Center):
                    self.try_harvest(bc.Direction.Center)
                self.reset_mission()

            elif self.mission.action == Missions.CreateBlueprint:
                #print("Worker {} creating blueprint.".format(self.unit.id))
                can_afford = False
                if self.mission.info.isRocket:
                    if self.game_controller.karbonite() >= bc.UnitType.Rocket.blueprint_cost():
                        can_afford = True
                else:       
                    if self.game_controller.karbonite() >= bc.UnitType.Factory.blueprint_cost():
                        can_afford = True
                
                # TODO Upgrade logic with better pathfinding
                if can_afford:

                    if not self.perform_second_action and self.target_location is None:
                        if self.path == None or len(self.path) == 0:
                            #print("Build location path is null. Making a new one.")
                            #self.target_location = self.mission.info.map_location 
                            newLocation = self.map_controller.GetRandomEarthNode()
                            self.target_location = newLocation
                            #print("Wants to move from {},{} to {},{}".format(\
                            #self.unit.location.map_location().x, self.unit.location.map_location().y, \
                            #self.target_location.x, self.target_location.y))
                            self.update_path_to_target()
                            

                    if self.has_reached_destination():
                        #self.one_random_movement()
                        direction = random.choice(list(bc.Direction))
                        if self.mission.info.isRocket:
                            if self.try_blueprint(bc.UnitType.Rocket, direction):
                                print("Worker {} created blueprint for Rocket.".format(self.unit.id))
                            else:
                                self.one_random_movement()
                        else:
                            if self.try_blueprint(bc.UnitType.Factory, direction):
                                print("Worker {} created blueprint for Factory.".format(self.unit.id))
                            else:
                                self.one_random_movement()
                        #self.reset_mission()
                    else:
                        self.follow_path()
            elif self.mission.action == Missions.Build:
                #if self.mission.info.unit.structure_is_built():
                unit = self.game_controller.unit(self.mission.info.unit_id)
                if unit.structure_is_built():
                    print("Structure {} is complete!".format(unit))
                    self.reset_mission()
                else:
                    if self.try_build(self.mission.info.unit_id):
                        map_location = self.unit.location.map_location()
                        print("Worker {} building structure location: {},{} - unit location: {},{}".format(self.unit.id, \
                        self.mission.info.map_location.x,self.mission.info.map_location.y,\
                        map_location.x,map_location.y))
                    else:
                        self.reset_mission()
            

    def try_blueprint(self, unit_type, direction):
        """Trys a blueprint"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_blueprint(self.unit.id, unit_type, direction):
            print("Worker [{}] cannot blueprint [{}] in direction [{}]".\
            format(self.unit.id, unit_type, direction))
            return False

        self.game_controller.blueprint(self.unit.id, unit_type, direction)
        #print("BLUEPRINT_RESULT: {}".format(result))
        info = MissionInfo()
        info.map_location = self.unit.location.map_location()
        team = self.game_controller.team()
        nearby = self.game_controller.sense_nearby_units_by_team(info.map_location, 5,team)
        structure = None
        for other in nearby:
            #print(other.unit_type)
            if bc.UnitType.Factory == other.unit_type or bc.UnitType.Rocket == other.unit_type:
                structure = other
                print("Factory {} Build Mission Created for unit {}".format(structure.id,self.unit.id))
                self.mission = self.mission_controller.CreateBuildMission(structure)
                print("new build mission [{}] ".format(self.mission))
        
        return True

    def try_build(self, blueprint_id):
        """Trys to build"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_build(self.unit.id, blueprint_id):
            print("Worker [{}] cannot build [{}]".format(self.unit.id, blueprint_id))
            return False

        self.game_controller.build(self.unit.id, blueprint_id)
        print("Worker {} performed build SUCCESSFULLY on {}".format(self.unit.id,blueprint_id))
        return True

    def try_harvest(self, direction):
        """Trys to harvest"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_harvest(self.unit.id, direction):
            #print("Worker [{}] cannot harvest in direction [{}]".format(self.unit.id, direction))
            return False

        self.game_controller.harvest(self.unit.id, direction)
        #print("Worker [{}] HARVESTED.".format(self.unit.id))
        return True

    def try_repair(self, structure_id):
        """Trys to repair"""
        if self.unit.worker_has_acted():
            print("Worker [{}] has already acted this turn".format(self.unit.id))
            return False

        if not self.game_controller.can_repair(self.unit.id, structure_id):
            print("Worker [{}] cannot repair structure [{}]".format(self.unit.id, structure_id))
            return False

        self.game_controller.repair(self.unit.id, structure_id)
        return True

    def try_replication(self, direction):
        """Trys to replicate"""
        if not self.game_controller.can_replicate(self.unit.id, direction):
            print("Worker [{}] cannot replicate in direction [{}]".format(self.unit.id, direction))
            return False

        self.game_controller.replicate(self.unit.id, direction)
        return True
