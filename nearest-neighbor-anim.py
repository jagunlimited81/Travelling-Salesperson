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


# define
numVerticies = 26  # random.randrange(3, 25)
random.seed(126)

# available node names
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# sub array of letters up to numVerticies
nodeNames = letters[0:numVerticies]
#nodeNames = [str(n) for n in range(numVerticies)]

# create graph object
G = nx.Graph()
edgesAnimation = [[]]
frameCounter = 0
maxFrames = 0

# generate tuple, then add node to G
while len(G) < numVerticies:
    x = random.randrange(1, 100)
    y = random.randrange(1, 100)
    G.add_node(nodeNames[len(G)], pos=(x, y), visited=False)

# get node positions
pos = nx.get_node_attributes(G, 'pos')


# -- Nearest Neighbor portion -- #

availableVertecies = [n for n in range(numVerticies)]
randomStartingPoint = random.randrange(0, numVerticies-1)
visit(G, randomStartingPoint)
availableVertecies.remove(randomStartingPoint)
totalDistance = 0
edges = []

current = randomStartingPoint

while len(availableVertecies) != 0:
    smallest = (0, -1)
    for i in availableVertecies:
        dist = getDiststaceBetween(G, current, i)
        if smallest[1] == -1 or smallest[1] > dist:
            smallest = (i, dist)

    visit(G, smallest[0])
    availableVertecies.remove(smallest[0])
    totalDistance += smallest[1]
    edges.append((nodeNames[current], nodeNames[smallest[0]]))
    edgesAnimation.append([])
    for e in edges:
        edgesAnimation[frameCounter].append(e)
    frameCounter += 1
    maxFrames += 1
    current = smallest[0]
# connect the final edge to the first edge
edges.append((nodeNames[current], nodeNames[randomStartingPoint]))
totalDistance+= getDiststaceBetween(G, current, randomStartingPoint)
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
    ax.set_title("Nearest Neighbor Algorithm: Frame {}/{}\nTotal Cost: {}".format(num+1, maxFrames, int(totalDistance)))


ani = animation.FuncAnimation(
    fig, simple_update, frames=maxFrames, fargs=())
ani.save('nearest-neighbor.gif', writer='Jared Trembley and Nick Leonard')
