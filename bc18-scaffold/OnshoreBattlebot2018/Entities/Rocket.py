import random
import sys
import traceback

from .IStructure import IStructure

class Rocket(IStructure):

    """This is the rocket"""

    def __init__(self, gameController, unitController, unit):
        super(Rocket, self).__init__(gameController, unitController, unit)

    def run(self):

        pass

    def tryLoad(self, targetRobotId):
        #TODO check heat of target unit is low enough
        if not self.gameController.can_load(self.unit.id, targetRobotId):
            print("Rocket [{}] cannot load the target [{}]".format(self.unit.id, targetRobotId))
            return False

        self.gameController.load(self.unit.id, targetRobotId)
        return True

    def tryUnload(self, targetRobotId):
        #TODO check heat of target unit is low enough
        if not self.gameController.can_unload(self.unit.id, targetRobotId):
            print("Rocket [{}] cannot unload the target [{}]".format(self.unit.id, targetRobotId))
            return False

        self.gameController.unload(self.unit.id, targetRobotId)
        return True

    def tryLaunch(self, destination):
        if not self.gameController.can_launch_rocket(self.unit.id, destination):
            print("Rocket [{}] could not launch to destination [{}]".format(self.unit.id, destination))
            return False

        self.gameController.launch_rocket(self.unit.id, destination)

        """This runs the rocket"""
        pass

    def try_load(self, target_robot_id):
        """Trys to load the rocket"""
        #TODO check heat of target unit is low enough
        if not self.game_controller.can_load(self.unit.id, target_robot_id):
            print("Rocket [{}] cannot load the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.load(self.unit.id, target_robot_id)
        return True

    def try_unload(self, target_robot_id):
        """Trys to unload the rocket"""
        #TODO check heat of target unit is low enough
        if not self.game_controller.can_unload(self.unit.id, target_robot_id):
            print("Rocket [{}] cannot unload the target [{}]".format(self.unit.id, target_robot_id))
            return False

        self.game_controller.unload(self.unit.id, target_robot_id)
        return True

    def try_launch(self, destination):
        """Trys to launch the rocket"""
        if not self.game_controller.can_launch_rocket(self.unit.id, destination):
            print("Rocket [{}] could not launch to destination [{}]".format(\
            self.unit.id, destination))
            return False

        self.game_controller.launch_rocket(self.unit.id, destination)

        return True
