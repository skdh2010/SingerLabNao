
'''
Created on 2015. 9. 24.

@author: Nao
'''
import time
import numpy as np
from com.fireboxtraining.XMLinterpreter import XMLinterpreter
from com.fireboxtraining.XMLutility import XMLutility
from com.fireboxtraining.CellsCointainer import CellCointainer
from com.fireboxtraining.TreeBuilder import BranchAnalysis
from _elementtree import TreeBuilder
from com.fireboxtraining.Transformation import Transformation
from ConnectionAnalysis import ConnectionAnalysis
import sys
from shapely.geometry import Polygon

import re

start = time.time()
#condition = [True, True, True, True]

#Transformation.Transformation("c:/e/SAC1.xml","c:/e/SAC1.xml", "Ads" )
#"""
#f1 = open('workfile1.txt', 'w')
#f2 = open('workfile2.txt', 'w')
#"""


ConnectionAnalysis.areaVSconnection("c:/e/SAC1.xml", "c:/e/SAC2.xml", "d:/AIIs_052616.xml", "nput", "d:/CBs_052616.xml", "ibbon", 500, ' input ')
#ConnectionAnalysis.areaVSconnection("c:/e/SAC1.xml", "c:/e/SAC2.xml", "d:/CBs_052616.xml", "nput","d:/AIIs_052616.xml", "utput",  500)
##square = Polygon([(0,0),(1,0),(1,1),(0,1)])

#rect = Polygon([(0.5,0),(0.8,0.5),(1.5,0.7),(2,0)])
#rect = Polygon([[3,0],[2,1],[2,0]])
#print rect.exterior.xy
#x,y = square.intersection(rect).exterior.xy
##print rect.area




#Transformation.areaVSrelength2("c:/e/SAC1.xml", "c:/e/SAC2.xml",  "c:/r/CBs_052616.xml")
#Transformation.Transformation("cb:/e/SAC1.xml", "c:/e/SAC2.xml", "c:/e/annotation.xml", "c:/e/annotation.xml")


"""
f1.writelines(str(cellcoin2.allNodesExtract(1)))

f2.writelines(str(Transformation.convertCoord(a, cellcoin2.allNodesExtract(1))))

f1.close()
f2.close()
"""
#XMLutility.MultiSeparator(cellcoin)
#print cellcoin.allNodesExtract(1)
#XMLutility.separtor(cellcoin, "cellname")
#preCB = XMLinterpreter("c:/d/OFF_CBs_111715.xml")
#print preCB.scaleExtract()
#preAC = XMLinterpreter("e:/ACs_040116.xml")
#preRB= XMLinterpreter("e:/RBs_040116.xml")
#AC = CellCointainer(preAC, condition)
#RB = CellCointainer(preRB, condition)
#XMLutility.CompareTwoCellsNodeAndPrintMidPoint("c:/a/RBs_040116.xml", "c:/a/ACs_040116.xml", 1000, "nocluster.xml")
#print CB.Edges
#print RB.Edges['RB68']
#print BranchAnalysis.singleStrahler(RB.Edges['RB68'], 11803)
#print BranchAnalysis.Strahler(RB)
#preTest =XMLinterpreter("d:/testsoma.xml")
#Test = CellCointainer(preTest, condition)
#print "SOMA".lower() == "Soma".lower()
#print Test.findStartingPointsVar()
#print BranchAnalysis.Strahler(Test)

"""  """
#print RB.Edges['RB78']
#print BranchAnalysis.simplification(RB.Edges['RB78'])


#AII = CellCointainer(preAII, condition)
#print AII.Edges['AIId']
#print BranchAnalysis.simplification(AII.Edges['AIId'])
#print BranchAnalysis.singleStrahler(cellcoin.Edges['AIId'])
#print BranchAnalysis.debugStart(AII)
#AC = CellCointainer(preAC, condition)
#print AC.allNodesExtract(1)
#print AC.allNodesExtract(2)
#print AC.edgeNodeExtract()
#print preRB.commentExtract()
#print RB.Branches
#print RB.allEdgesExtract(1)
#print RB.commentWithKeywordExtract('put')
#XMLutility.CompareTwoCellsCommentAndEdgeAndPrint("c:/d/OFF_CBs_110515.xml", "c:/d/AIIs_110515.xml", 1000, "ribbonOF_CB_ToAII.xml", "ibbon")
#XMLutility.CompareTwoCellsCommentAndEdgeAndPrint("c:/d/AIIs_110515.xml", "c:/d/OFF_CBs_110515.xml", 1000, "InputOF_AII_ToOFFCB.xml", "nput")
#XMLutility.CompareTwoCellsNodeAndPrintMidPoint("c:/d/OFFCBs_102215.xml", "c:/d/AIIs_102215.xml", 1000, "withCluster.xml")

#XMLutility.CompareTwoCellsComments("c:/d/OFFCBs111815.xml", "ibbon","c:/d/AIIs_111715.xml","nput",  200, "CBribbonToinput.txt", "Ribbon-input.txt", "CBribbonToinput.xml")
#XMLutility.CompareTwoCellsComments("c:/d/AIIs_111715.xml","utput","c:/d/OFFCBs111815.xml", "nput",  200, "AIoutputToinput.txt", "output-input.txt", "AIoutputToinput.xml")
#XMLutility.CompareTwoCellsComments("c:/d/OFFCBs111815.xml", "ibbon","c:/d/AIIs111815.xml","nput",  100, "CBinputribbon2.txt", "CBdata22.txt", "CBinputribbon2.xml")
#XMLutility.CompareTwoCellsCommentsAndChangeComment("c:/d/OFFCBs111815.xml", "ibbon","c:/d/AIIs111815.xml","nput",  100, "Goddman.xml")
#s =" signature"

mid = time.time()
print mid-start

#for item in RB.allNodesExtract(1):
#    if item[4] == None:
#        asd = True
#print asd


#CBAC =XMLutility.compareTwoCellandReturnMidPoint(CB.allNodesExtract(1), AC.allNodesExtract(1), 1000, 1)
#RBAC =XMLutility.compareTwoCellandReturnMidPoint(RB.allNodesExtract(1), AC.allNodesExtract(1), 1000, 1)
#ACAII =XMLutility.compareTwoCellandReturnMidPoint(AC.allNodesExtract(1), AII.allNodesExtract(1), 1000, 1)

#CBACsorted =XMLutility.sortNodes(CBAC)
#RBACsorted =XMLutility.sortNodes(RBAC)
#ACAIIsorted =XMLutility.sortNodes(ACAII)

#printCBAC = XMLutility.XMLTempPrinter(CB.Parameter, CBACsorted, "connection.CB-AC.xml")
#printRBAC = XMLutility.XMLTempPrinter(RB.Parameter, RBACsorted, "connection.RB-AC.xml")
#printACAII = XMLutility.XMLTempPrinter(AC.Parameter, ACAIIsorted, "connection.AC-AII.xml")





