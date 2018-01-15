import random
import sys
import traceback
import battlecode as bc
from collections import deque
from .GraphNode import GraphNode

# Given a robot and destination, determines the best route to take
# Returns an array of directions to the calling robot
# Robot will follow the given directions until it determines that it needs to recalculate its path
# This is far more efficient than running Pathfinding every turn and more adaptive than running it once only
# May implement multiple pathfinding methods and determine which to use based upon what's needed or the distance
class PathfindingController:

	def __init__(self, gameController, mapController):
		self.gameController = gameController
		self.mapController = mapController
		self.plan = []
		self.Directions = [bc.Directions.North, bc.Direction.East, bc.Direction.South, bc.Direction.West] 

	def FindPathTo(self, currentLocation, destination):
		print("starting pathfinding")
		path = []
		explored = []
		frontier = deque([])
		node = GraphNode(currentLocation, None, None)
		frontier.append(node)
		while True:
			if len(frontier) == 0:
				return
			else:
				node = frontier.popleft()
			newNodes = self.Explore(node)
			explored.append(node)
			newNodes = {elem for elem in newNodes if elem not in explored}
			for nodes in newNodes:
				frontier.append(nodes)
			if node == destination:
				break
		while node.Parent is not None:
			path.append(node.Action)
			node = node.Parent
		
		return path

	def Explore (self, node):
		discovered = []
		for direction in self.Directions:
			newNode = self.Transition(node , direction)
			if newNode is not None:
				discovered.append(newNode)
		return discovered

	def Transition(self, node, direction):
		currentnode = node
		if direction == bc.Directions.North:
			newNode = self.mapController.GetNode(currentnode.room.x, currentnode.room.y + 1)
		elif direction == bc.Directions.East:
			newNode = self.mapController.GetNode(currentnode.room.x + 1, currentnode.room.y)
		elif direction == bc.Directions.South:
			newNode = self.mapController.GetNode(currentnode.room.x, currentnode.room.y - 1)
		elif direction == bc.Directions.West:
			newNode = self.mapController.GetNode(currentnode.room.x - 1, currentnode.room.y)
		newRoom = None
		if (newNode is not None):
			newRoom = GraphNode(newRoom, node, direction)
		return newRoom
		
