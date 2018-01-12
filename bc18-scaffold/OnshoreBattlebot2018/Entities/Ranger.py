import random
import sys
import traceback

from .IRobot import IRobot

class Ranger(IRobot):
    # change init definition to include any controllers needed in the instructor as we need them
    # For example:  it will eventually need to access the Targeting and Pathfinding controllers
    def __init__(self, gameController, unitController, pathfindingController, unit):
        super().__init__(gameController, unitController, pathfindingController, unit)

    def run(self):
        pass

    def tryAttack(self, targetRobotId):
        #TODO check heat is low enough
        if not self.game_controller.can_attack(self.unit.id, targetRobotId):
            print("Ranger [{}] cannot attack the target [{}]".format(self.unit.id, targetRobotId))
            return False

        self.game_controller.attack(self.unit.id, targetRobotId)
        return True

    def trySnipe(self, targetLocation):
        #TODO check has research

        if not self.game_controller.is_begin_snipe_ready(self.unit.id):
            print("Snipe is not ready for ranger [{}]".format(self.unit.id))
            return False

        if not self.game_controller.can_begin_snipe(self.unit.id, targetLocation):
            print("Ranger [{}] cannot snipe target location".format(self.unit.id))
            return False

        self.game_controller.begin_snipe(self.unit.id, targetLocation)
        return True
