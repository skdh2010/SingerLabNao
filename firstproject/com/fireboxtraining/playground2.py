'''
Created on 2016. 3. 30.

@author: Nao
'''
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph();
G.add_node("spam")
G.add_edges_from([(1,2),(1,3)])
nx.draw(G)

plt.show()