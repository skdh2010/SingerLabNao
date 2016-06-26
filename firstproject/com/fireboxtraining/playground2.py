#coding: utf-8
'''
Created on 2016. 3. 30.

@author: Nao
'''
import time
from com.fireboxtraining.XMLinterpreter import XMLinterpreter
from com.fireboxtraining.XMLutility import XMLutility
from com.fireboxtraining.CellsCointainer import CellCointainer
from com.fireboxtraining.TreeBuilder import BranchAnalysis
from _elementtree import TreeBuilder
from gaussfitter import moments
import networkx as nx
from scipy import optimize
import matplotlib.pyplot as plt
from xml_to_vtk_many2 import converToVTK
import numpy as np
from pylab import figure, show, rand
from matplotlib.patches import Ellipse

import csv
with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

vheight = 0
circle = 0
rotate = 1



"""

NUM = 100 

ells = [Ellipse(xy=rand(2)*10, width=rand(), height=rand(), angle=rand()*360)
        for i in range(NUM)]

fig = figure()
ax = fig.add_subplot(111, aspect='equal')
for e in ells:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_alpha(rand())
    e.set_facecolor(rand(3))

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

show()
"""