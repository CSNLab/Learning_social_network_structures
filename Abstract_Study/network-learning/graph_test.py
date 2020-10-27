import networkx as nx
from config import *
import matplotlib.pyplot as plt

network = nx.Graph()
network.add_edges_from(EDGES[1][9])
nx.draw(network)
plt.show()
