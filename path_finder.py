# Pathfinder - Breadth First Search

# Utilizing dictionary plotting connections between different nodes, pathfinder
# calculates the shortest path from one node (start) to another (destination).
# Pathfinder utilizes the A* search algorithm to calculate this path and then
# converts list of nodes to visit en route to destination to left/right/forward
# directions for the product user.

from node_mapper import *

"""
connections = { "1A": set(["1B", "1C"]),
                "1B": set(["1A", "1D"]),
                "1C": set(["1A", "1E"]),
                "1D": set(["1B"]),
                "1E": set(["1C"]),
                "1F": set([]) }
"""




def directDist(start, end):
    # Calculates Euclidian distance between two points


    return ((start[0] - end[0])**2 + \
            (start[1] - end[1])**2) ** 0.5






def findLowestFCost(nodes, destination):
    pass


def navigateNodes(start, end):
    allNodesMap = mapAllNodes() # dictionary mapping each node's name to its object
    allConnsMap = mapAllConnections() # dictionary mapping each node to its connected nodes

    # if start not in allNodes or end not in allNodes:
    #     return None

    closedNodes = set()
    openNodes = set()
    # openNodes.add(start)

    cameFrom = dict()

    while len(openNodes) != 0:
        currentNode = 0

    return isinstance(allNodesMap["WH1"]["1Elevator"], Elevator)





"""
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
