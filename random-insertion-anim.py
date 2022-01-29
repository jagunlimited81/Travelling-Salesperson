import matplotlib.pyplot as plt
from matplotlib import animation
import networkx as nx
import numpy as np
import random


def getDiststaceBetween(G, n1: int, n2: int):
    attr = nx.get_node_attributes(G, 'pos')
    x1 = attr[nodeNames[n1]][0]
    x2 = attr[nodeNames[n2]][0]
    y1 = attr[nodeNames[n1]][1]
    y2 = attr[nodeNames[n2]][1]
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    return distance


def visit(G, n: int):
    nx.set_node_attributes(G, {nodeNames[n]: True}, "visited")


def getDistanceOfCycle(G, nodeList):
    distance = 0
    for i in range(len(nodeList)):
        distance += getDiststaceBetween(G, nodeNames.index(
            nodeList[i]), nodeNames.index(nodeList[(i+1) % len(nodeList)]))

    return distance


# define
numVerticies = 26  # random.randrange(3, 25)
random.seed(126)

# available node names
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# sub array of letters up to numVerticies
nodeNames = letters[0:numVerticies]
#nodeNames = [str(n) for n in range(numVerticies)]
edgesAnimation = []
frameCounter = 0
maxFrames = 0
# create graph object
G = nx.Graph()

# generate tuple, then add node to G
while len(G) < numVerticies:
    x = random.randrange(1, 100)
    y = random.randrange(1, 100)
    G.add_node(nodeNames[len(G)], pos=(x, y), visited=False)

# get node positions
pos = nx.get_node_attributes(G, 'pos')


# -- Insertion portion -- #

availableVertecies = [n for n in range(numVerticies)]
calculatedDistance = 0
totalDistance = 0

# select three vertecies to create cycle
nodeOrder = []
edges = []  # drawing object

# starting point and add to list
randomStartingPoint = random.randrange(0, numVerticies-1)
visit(G, randomStartingPoint)
availableVertecies.remove(randomStartingPoint)
current = randomStartingPoint
nodeOrder.append(nodeNames[current])

# select furthest away and add to list
furthest = (0, -1)
for i in availableVertecies:
    dist = getDiststaceBetween(G, current, i)
    if furthest[1] == -1 or furthest[1] < dist:
        furthest = (i, dist)
        totalDistance = dist
nodeOrder.append(nodeNames[furthest[0]])
availableVertecies.remove(furthest[0])


# loop through all verticies and add the one that changes the distance the least to the list
while len(nodeOrder) < numVerticies:
    # randomly select vertex and find the order in the nodelist that grows the cycle size the least
    current = random.choice(availableVertecies)  # select vertex
    calculatedDistance = 0
    minIndexAndValue = (0, -1)

    for i in range(len(nodeOrder)+1):  # loop through the possible places to put the node
        copyofList = nodeOrder.copy()
        copyofList.insert(i, nodeNames[current])  # try insertion
        calculatedDistance = getDistanceOfCycle(G, copyofList)
        if minIndexAndValue[1] == -1 or minIndexAndValue[1] > calculatedDistance:
            minIndexAndValue = (i, calculatedDistance)

    nodeOrder.insert(minIndexAndValue[0], nodeNames[current])
    availableVertecies.remove(current)
    totalDistance = minIndexAndValue[1]
    i += 1
    edges = []
    for i in range(len(nodeOrder)):
        edges.append((nodeOrder[i], nodeOrder[(i+1) % len(nodeOrder)]))
    edgesAnimation.append([])
    for e in edges:
        edgesAnimation[frameCounter].append(e)
    frameCounter += 1
    maxFrames += 1


print("Total cost: " + str(totalDistance))


fig, ax = plt.subplots(figsize=(6, 4))


frameCounter = 0


def simple_update(num):
    ax.clear()

    # Draw the graph with random node colors
    nx.draw_networkx_nodes(G, pos, node_size=200)
    nx.draw_networkx_nodes(G, pos, nodelist=nodeNames[randomStartingPoint],
                           node_size=200, node_color="r", label="Starting Point for NN alg")

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edgesAnimation[num], width=5)

    # labels for vertex
    nx.draw_networkx_labels(G, pos, font_size=12,
                            font_family="sans-serif")  # vertex labels
    # Set the title
    ax.set_title("Random Insertion Algorithm: Frame {}/{}\nTotal Cost={}".format(num+1, maxFrames, int(totalDistance)))


ani = animation.FuncAnimation(
    fig, simple_update, frames=maxFrames, fargs=())
ani.save('random-insertion.gif', writer='Pillow')


# plt.show() #bugged in python 3.9
