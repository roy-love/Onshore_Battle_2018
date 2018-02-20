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
		#Possible directions, only using 4 to make it alittle simpler
		self.Directions = [bc.Direction.North, bc.Direction.East, bc.Direction.South, bc.Direction.West]
		#The nodes that are blocked either by map obstacles 
		self.earthBlockedNodes = []

	def FindPathTo(self, planet, currentLocation, destination):
		#First step is to find all of the blocked nodes on the map
		self.earthBlockedNodes = self.blockEarthNodes()
		#create the path object that will be returned
		path = []
		#create the explored object that will hold all of the nodes we have explored so far
		explored = []
		#create the frontier object that will hold all of the nodes we have found but not explored so far
		frontier = deque([])
		#set the starting location node
		startingLocation = self.mapController.GetNode(planet, currentLocation.x, currentLocation.y)
		#set the goal location, where we want to get to
		endingLocation = self.mapController.GetNode(planet, destination.x, destination.y)
		#create a starting GraphNode that holds the starting location and has no parent and no action
		node = GraphNode(startingLocation, None, None)
		#creates the ending GraphNode
		endNode = GraphNode(endingLocation, None, None)
		#Create the list of nodes that will be blocked by units
		blockedLocations = []
		#Get all visible units on the map
		units = self.gameController.units()
		#Interate through the units
		for unit in units:
			unitMapLoc = unit.location.map_location()
			#Added nodes with units to the list of blocked nodes
			blockedLocations.append(self.mapController.GetNode(unitMapLoc.planet, unitMapLoc.x, unitMapLoc.y))
		#add the starting node to the frontier so we know where to start from
		frontier.append(node)
		while True:
			#check if the frontier is empty if it is no path was found to the goal and we need to break out
			if len(frontier) == 0:
				return
			else:
				#using popleft from the frontier deque to get the first node that was push in 
				node = frontier.popleft()
			#Take the node we just popped out of the frontier and call the explore method with it
			newNodes = self.Explore(planet, node)
			#Add the current node to the explored nodes so we don't explore it again
			explored.append(node.room)
			#For the newly discovered nodes check to see if they have already been explored, 
			# are ready in the frontier, are blocked if not then add them to the frontier 
			for nodes in newNodes:
				#if it is already explored do nothing
				if self.AlreadyExplored(nodes, explored):
					pass
				else:
					#check if it is already in the frontier if so do nothing
					if self.AlreadyFrontier(nodes, frontier):
						#check if node is open
						if self.IsNodeOpen(nodes, blockedLocations):
							#if the node is not explored, in the frontier, or blocked add it to the frontier
							frontier.append(nodes)
			#If the current node is the room we are looking for break out we are done
			if node.room == endNode.room:
				break
		#once we have found the goal node we need to go back through all of the nodes and record the actions that go us to the goal node
		while node.Parent is not None:
			#Append the node action, the direction we went to get to this node to the path
			path.append(node.Action)
			#Set the node to be the parent node, once we reach a node with no parent we know we are at the start node
			node = node.Parent
		if path is None:
			#print("no path found")
			pass
		#print(path)
		#return the path to the calling method 
		return path

	def Explore (self, planet, node):
		#Creating the discovered object to hold newly discovered nodes 
		discovered = []
		#Interate through the directions to find new nodes
		for direction in self.Directions:
			#for each direction we are going to transition to the node in that direction if it exist and isn't blocked
			newNode = self.Transition(planet, node , direction)
			#if there node exist add it to the discovered object to be returned once we have went through all of the directions
			if newNode is not None:
				discovered.append(newNode)
		#return the discovered nodes 
		return discovered

	def Transition(self, planet, node, direction):
		currentnode = node
		#Check which direction we are going and transition to that node if it exist
		if direction == bc.Direction.North:
			newNode = self.mapController.GetNode(planet, currentnode.room["x"], currentnode.room["y"] + 1)
		elif direction == bc.Direction.East:
			newNode = self.mapController.GetNode(planet, currentnode.room["x"] + 1, currentnode.room["y"])
		elif direction == bc.Direction.South:
			newNode = self.mapController.GetNode(planet, currentnode.room["x"], currentnode.room["y"] - 1)
		elif direction == bc.Direction.West:
			newNode = self.mapController.GetNode(planet, currentnode.room["x"] - 1, currentnode.room["y"])
		newRoom = None
		#if the node exist create a new Graphnode with the node, its parent node, and the action we took to get here
		if (newNode is not None):
			newRoom = GraphNode(newNode, node, direction)
		#return the new GraphNode 
		return newRoom
		
	def AlreadyExplored(self, node, explored):
		isExplored = False
		#Interate through the explored nodes to see if the current node is there if it is return true
		for item in explored:
			if node.room["hash"] == item["hash"]:
				isExplored = True
				break
		return isExplored

	def AlreadyFrontier(self, node, frontier):
		notInFrontier = True 
		#Interate through the frontier to see if the current node is there if it is return true
		for item in frontier:
			if node.room["hash"] == item.room["hash"]:
				notInFrontier = False
				break
		return notInFrontier

	def IsNodeOpen(self, node, blockedLocations):
		#default node is open to true
		nodeOpen = True
		#interate through the nodes that are blocked on the map
		for nodes in self.earthBlockedNodes:
			#the room["hash"] is a unique hash of the x and y coordantes so we can check and see if we are looking at the same node easily
			if node.room["hash"]  == nodes["hash"] :
				#if the node is in the earthblockednodes return false because it a blocked node
				return False
		for nodes in blockedLocations:
			#if the node is in the blocked locations return false because the node is currently blocked by a robot or structure
			if node.room["hash"] == nodes["hash"] :
				return False
		#return True if node is not in the earthblocked or the robot blocked list
		return nodeOpen

	def blockEarthNodes(self):
		blockedNodes = []
		#the map is a 2d array of nodes you have to interate through all of the Y coordinates for each of the X coordinates
		for xNodes in self.mapController.earth_map:
			for node in xNodes:
				#check if the node is passable
				if not node["isPassable"]:
					#if not add it to the blocked nodes
					blockedNodes.append(node)
		#return the list of blocked nodes
		return blockedNodes
