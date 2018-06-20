# Pathfinder - Breadth First Search

# Utilizing dictionary plotting connections between different nodes, pathfinder
# calculates the shortest path from one node (start) to another (destination).
# Pathfinder utilizes the A* search algorithm to calculate this path and then
# converts list of nodes to visit en route to destination to left/right/forward
# directions for the product user.

from node_mapper import *

def directDist(currNode, endNode):
    # Calculates Euclidian distance between two points
    # if currNode and endNode are both elevators, do something else
    if isinstance(currNode, Elevator) and isinstance(endNode, Elevator):
        return 10**10
    else:
        # print("currNode: ", currNode.getCoords())
        # print("endNode: ", endNode.getCoords())
        # print("directDist: ", ((currNode.getCoords()[0] - endNode.getCoords()[0])**2 + \
                               # (currNode.getCoords()[1] - endNode.getCoords()[1])**2) ** 0.5)
        return ((currNode.getCoords()[0] - endNode.getCoords()[0])**2 + \
                (currNode.getCoords()[1] - endNode.getCoords()[1])**2) ** 0.5

def calcDCost(currNode, endNode):
    return directDist(currNode, endNode)

"""
def calcGCost(currNode, startNode, cameFrom):
    # Function calculates (recursively) the distance from the current node to
    # the origin via previously visited nodes.

    if currNode not in cameFrom.keys():
        return 0

    # if cameFrom[None] == currNode:
    #     return 0

    # if currNode == cameFrom[None]:
    #     return 0

    # if currNode == startNode:
    #     return 0

    # if not isinstance(currNode, Node):
    #     return 0

    print("cameFrom: ", cameFrom)
    print("currNode: ", currNode)
    print("cameFrom[currNode]: ", cameFrom[currNode])
    parentNode = cameFrom[currNode]
    return calcDCost(currNode, parentNode) + calcGCost(parentNode, startNode, cameFrom)
"""

def calcFCost(currNode, endNode, cameFrom):
    # Total cost of getting from startNode to endNode via currNode. Calculated
    # by finding cost from currNode to startNode via nodes plus direct distance
    # from currNode to endNode.
    return calcDCost(currNode, endNode) # + calcGCost(currNode, startNode, cameFrom)

def findLowestFCost(openNodes, endNode, cameFrom):
    # Finds the node among the currently open nodes that has the lowest F cost,
    # such that the F cost of a node is defined as cost of getting from the
    # origin to the destination via the selected node.
    bestNode = None
    bestCost = 10**42

    for node in openNodes:
        currFCost = calcFCost(node, endNode, cameFrom)
        if currFCost < bestCost:
            bestCost = currFCost
            bestNode = node
    return bestNode

#####################################################################
#####################################################################

# If nodes not on same floor, then do navigateNodes from origin to elevator of
# currFloor and then do navigateNodes from elevator of destFloor to destination.

def navigateNodes(startStr, endStr): # start and end are the objects of start node and end node
    allNodesMap = mapAllNodes() # dictionary mapping each node's name to its object
    allConnsMap = mapAllConnections() # dictionary mapping each node to its connected nodes

    # allNodesSet = set(allNodesMap.values().values())

    startFloor = "WH%s" % startStr[0]
    startNode = allNodesMap[startFloor][startStr]
    
    endFloor = "WH%s" % endStr[0]
    endNode = allNodesMap[endFloor][endStr]

    # if (startNode not in allNodesSet) or (endNode not in allNodesSet):
    #     return None

    closedNodes = set()
    openNodes = set()
    openNodes.add(startNode)

    cameFrom = dict()

    print("startNode: ", startNode)
    print("endNode: ", endNode)

    while len(openNodes) != 0:
        currNode = findLowestFCost(openNodes, endNode, cameFrom)
        print("    currNode: ", currNode)
        # print("fCost: ", calcFCost(currNode, startNode, endNode, cameFrom))


        if currNode == None:
            return None # there is no possible path to endNode

        openNodes.remove(currNode)
        closedNodes.add(currNode)

        if currNode == endNode:
            return reconstruct_path(cameFrom, currNode)

# allConnsMap[currNode.getName()]
        for neighbor in getAllConnections(allNodesMap, allConnsMap, currNode):
            print("neighbor: ", neighbor)
            print("cameFrom: ", cameFrom)
            if neighbor in closedNodes:
                continue # ignore already evaluated nodes
            tempFScore = calcFCost(currNode, endNode, cameFrom)
            if ((neighbor not in openNodes) or
                (tempFScore < calcFCost(neighbor, endNode, cameFrom))):
                print("gCost: ", calcFCost(neighbor, endNode, cameFrom))
                cameFrom[neighbor] = currNode

                if neighbor not in openNodes:
                    openNodes.add(neighbor)

#####################################################################
#####################################################################

def getAllConnections(allNodesMap, allConnsMap, currNode):
    # think about how elevators affect this (specifically the floor line)
    allNeighbors = [ ]

    for neighborStr in allConnsMap[currNode.getName()]:
        floor = "WH%s" % neighborStr[0]
        neighbor = allNodesMap[floor][neighborStr]
        allNeighbors.append(neighbor)

    return allNeighbors


def reconstruct_path(cameFrom, currNode): # Current is object, cameFrom is map
    fullPath = [currNode]

    while currNode not in cameFrom.keys():
        if currNode == None:
            return None

        currNode = cameFrom[currNode]
        fullPath.append(currNode)

    return fullPath

# nodesPath = navigateNodes("1001", "1321")
nodesPath = navigateNodes("1001", "1321")
print(nodesPath)












"""
# return isinstance(allNodesMap["WH1"]["1Elevator"], Elevator)

connections = { "1A": set(["1B", "1C"]),
                "1B": set(["1A", "1D"]),
                "1C": set(["1A", "1E"]),
                "1D": set(["1B"]),
                "1E": set(["1C"]),
                "1F": set([]) }

def find_path(connections, start, destination):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in connections[vertex] - set(path):
            if next == destination:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

print(list(find_path(connections, "1B", "1E")))
"""
