import random
import sys
import traceback

from .IStructure import IStructure

class Factory(IStructure):
	def __init__(self, gameController, unitController, unit):
		super(Factory, self).__init__(gameController, unitController, unit)

	def run(self):
		pass

	def tryProduceRobot(self, unitType):
		if self.gameController.is_factory_producing():
			print("Factory [{}] occupied, producing [{}] with [{}] rounds left".format(self.unit.id, self.unit.factory_unit_type, self.unit.factory_rounds_left))
			return False

		if not self.gameController.can_produce_robot(self.unit.id, unitType):
			print("Factory [{}] cannot produce the [{}]".format(self.unit.id, unitType))
			return False

		self.gameController.produce_robot(self.unit.id, unitType)
		return True