import random
import sys
import traceback
import battlecode as bc
from collections import deque
from .GraphNode import GraphNode

# Given a robot and destination, determines the best route to take
# Returns an array of directions to the calling robot
# Robot will follow the given directions until it determines that it needs to recalculate its path
# This is far more efficient than running Pathfinding every turn and more adaptive than \
# running it once only
# May implement multiple pathfinding methods and determine which to use based upon what's \
# needed or the distance
class PathfindingController:

	def __init__(self, gameController, mapController):
		self.gameController = gameController
		self.mapController = mapController
		self.plan = []
		self.Directions = [bc.Direction.North, bc.Direction.East, bc.Direction.South, bc.Direction.West] 

	def FindPathTo(self, currentLocation, destination):
		print("starting pathfinding")
		path = []
		explored = []
		frontier = deque([])
		startingLocation = self.mapController.GetNode(currentLocation.x, currentLocation.y)
		endingLocation = self.mapController.GetNode(destination.x, destination.y)
		node = GraphNode(startingLocation, None, None)
		endNode = GraphNode(endingLocation, None, None)
		frontier.append(node)
		while True:
			#print("FRONTIER LENGHT IS")
			#print(len(frontier))
			if len(frontier) == 0:
				#print("frontier is empty")
				return
			else:
				#print(frontier)
				node = frontier.popleft()
				#print("seeing if popleft is give me a dict or what i need")
				#print(node.room["x"])
			newNodes = self.Explore(node)
			explored.append(node.room)
			#newNodes = {elem for elem in newNodes if elem not in explored}
			for nodes in newNodes:
				#print("PRINTING WHAT IM ADDING TO FROntier")
				#print(nodes.room)
				#print(explored[0])
				#print("Nodes in Frontier")
				#print(len(frontier))
				if self.AlreadyExplored(nodes, explored):
					pass
					##print("NODE ALREADY IN EXPLORED")
					#print(len(explored))
					#print(len(frontier))
				else:
					if self.AlreadyFrontier(node, frontier):
						#print("adding to frontier")
						frontier.append(nodes)
			#print("nodes now in frontier")
			#print(len(frontier))
			#print(node.room)
			#print(endNode.room)
			if node.room == endNode.room:
				break
		while node.Parent is not None:
			#print("setting path now XXXXCXXXCXXCXXCXCXCXCXCXCXCXCX")
			path.append(node.Action)
			node = node.Parent
		print("Printing path now")
		print(path)
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
		#print("Printing the new current node")
		#print(currentnode.room)
		#print(currentnode.room["x"])
		if direction == bc.Direction.North:
			#print("PRINTING CURRENT NODE71")
			#print(currentnode.room["x"])
			newNode = self.mapController.GetNode(currentnode.room["x"], currentnode.room["y"] + 1)
		elif direction == bc.Direction.East:
			#print("PRINTING CURRENT NODE75")
			#print(currentnode.room)
			newNode = self.mapController.GetNode(currentnode.room["x"] + 1, currentnode.room["y"])
		elif direction == bc.Direction.South:
			#print("PRINTING CURRENT NODE79")
			#print(currentnode.room)
			newNode = self.mapController.GetNode(currentnode.room["x"], currentnode.room["y"] - 1)
		elif direction == bc.Direction.West:
			#print("PRINTING CURRENT NODE83")
			#print(currentnode.room)
			newNode = self.mapController.GetNode(currentnode.room["x"] - 1, currentnode.room["y"])
		#print("Printing newNode in Transitions")
		#print(newNode)
		newRoom = None
		if (newNode is not None):
			#print("ADDING to newRoom in Transition")
			newRoom = GraphNode(newNode, node, direction)
			#print(newRoom.room)
			#print("checking if newRoom is a dict not what i need")
			#print(newRoom.room["x"])
		return newRoom
		
	def AlreadyExplored(self, node, explored):
		isExplored = False
		for item in explored:
			if node.room["hash"] == item["hash"]:
				#print("Setting Is Explored to TRUE")
				#print(node.room["hash"])
				#print(item["hash"])
				isExplored = True
				break
		return isExplored

	def AlreadyFrontier(self, node, frontier):
		notInFrontier = True 
		for item in frontier:
			if node.room["hash"] == item.room["hash"]:
				notInFrontier = False
				break
		return notInFrontier

