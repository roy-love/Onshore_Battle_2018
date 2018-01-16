"""This is our Factory"""
import random
import sys
import traceback
import battlecode as bc
from Controllers.MissionController import *
from .IStructure import IStructure

class Factory(IStructure):
    """This is the factory"""
    def __init__(self, gameController, unitController, unit, missionController):
        super(Factory, self).__init__(gameController, unitController, unit, missionController)

        self.round_start_production = 0
        self.is_working = False
        self.directions = list(bc.Direction)

    def run(self):
        """This runs the garrison"""
        self.update_mission()

        garrison = self.unit.structure_garrison()
        if len(garrison) > 0:
            print("Factory [{}] Garrisoned Units".format(self.unit.id))
            for other in garrison:
                print("Unit with id [{}] is currently garrisoned.".format(other))

        if not self.mission is None:

            if self.mission.action == Missions.TrainBot:
                print("Factory [{}] TRAIN_BOT {} {}".format(\
                self.unit.id, self.is_working, self.unit.is_factory_producing()))
                if self.is_working and not self.unit.is_factory_producing():
                    if self.try_unload_units():
                        print("Factory [{}] successfully unloaded a unit.".format(self.unit.id))
                        self.mission = None
                        self.is_working = False
                elif not self.is_working and self.try_produce_robot(self.mission.info):
                    self.is_working = True
                else:
                    print("Factory [{}] producing robot. Rounds Left: {}".\
                    format(self.unit.id, self.unit.factory_rounds_left()))

    def try_produce_robot(self, unit_type):
        """This trys to produce robots"""
        if self.unit.is_factory_producing():
            print("Factory [{}] occupied, producing [{}] with [{}] rounds left".format(\
            self.unit.id, self.unit.factory_unit_type, self.unit.factory_rounds_left))
            return False

        #if not self.gameController.can_produce_robot(self.unit.id, unit_type):
            print("Factory [{}] cannot produce the [{}]. Current Karbonite: {}".\
            format(self.unit.id, unit_type, self.game_controller.karbonite()))
        #    return False

        self.game_controller.produce_robot(self.unit.id, unit_type)
        return True

    def try_garrision(self, unit_id):
        """This trys the garrision"""
        # TODO create garrision units function.
        return True

    def try_unload_units(self):
        """This trys to unload the units"""
        garrison = self.unit.structure_garrison()
        garrison_count = len(garrison)
        if garrison_count > 0:
            print("Factory [{}] garrisoned with [{}] units.".format(self.unit.id, garrison_count))
            direction = random.choice(self.directions)
            if self.game_controller.can_unload(self.unit.id, direction):
                print("Factory unloaded {} with id {}.".format(garrison[0], garrison[0]))
                self.game_controller.unload(self.unit.id, direction)

                return True
            else:
                print("Factory with id {} failed to unload.".format(self.unit.id))
                return False
        else:
            return False
