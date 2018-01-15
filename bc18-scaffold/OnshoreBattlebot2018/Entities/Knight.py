import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IRobot import IRobot

class Knight(IRobot):
    """This is the Knight robot"""
    # change init definition to include any controllers needed in the instructor as we need them
    # For example:  it will eventually need to access the Targeting and Pathfinding controllers
    def __init__(self, gameController, unitController, pathfindingController, missionController, unit):
        super().__init__(gameController, unitController, pathfindingController, missionController, unit, bc.UnitType.Knight)
        self.mission = None
        self.target_location = None
        self.path = None
        self.is_garrisoned = False

    def run(self):

        #if not self.is_garrisoned:
        self.update_mission()

        if not self.mission is None:
            if self.mission.action == Missions.Idle:
                self.idle()

            elif self.mission.action == Missions.RandomMovement:
                self.one_random_movement()

            elif self.mission.action == Missions.DestoryTarget:
                self.destroy_target()

            #Attacks nearby units
            nearby = self.game_controller.sense_nearby_units(self.unit.location.map_location(), 2)
            for other in nearby:
                if other.team != self.game_controller.team() \
                and self.game_controller.is_attack_ready(self.unit.id) \
                and self.game_controller.can_attack(self.unit.id, other.id):
                    print('Knight {} attacked a thing!'.format(self.unit.id))
                    self.game_controller.attack(self.unit.id, other.id)
                    break

    def is_enemy_sighted(self):
        """Lets you know if enemy is sighted"""
        #TODO determine if this unit is able to see an enemy.
        #TODO refactor code to IRobot so that all robots can sight enemies.
        pass

    def try_attack(self, target_robot_id):
        """Trys to attack"""
        #TODO check heat is low enough
        if not self.game_controller.can_attack(self.unit.id, target_robot_id):
            print("Knight [{}] cannot attack the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.attack(self.unit.id, target_robot_id)
        return True

    def try_javelin(self, target_robot_id):
        """Trys the javelin"""
        #TODO check has research

        if not self.game_controller.is_javelin_ready(self.unit.id):
            print("Javelin is not ready for knight [{}]".format(self.unit.id))
            return False

        if not self.game_controller.can_javelin(self.unit.id, target_robot_id):
            print("Knight [{}] cannot javelin target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.javelin(self.unit.id, target_robot_id)
        return True
