'''
Created on 2015. 9. 24.

@author: Nao
'''
import time
from com.fireboxtraining.XMLinterpreter import XMLinterpreter
from com.fireboxtraining.XMLutility import XMLutility
from com.fireboxtraining.CellsCointainer import CellCointainer
from com.fireboxtraining.TreeBuilder import BranchAnalysis

start = time.time()
condition = [True, True, True, True]
preAII = XMLinterpreter("c:/d/AIIs_102215.xml")
#preCB = XMLinterpreter("c:/d/OFF_CBs_111715.xml")
#print preCB.scaleExtract()
#preAC = XMLinterpreter("c:/d/ACs_102215.xml")
#preRB= XMLinterpreter("c:/d/RBs_102215.xml")
#CB = CellCointainer(preCB, condition)
#RB = CellCointainer(preRB, condition)
#print CB.Edges
#print RB.Edges['RB68']
#print BranchAnalysis.simplification(RB.Edges['RB68'])
#print RB.Edges['RB78']
#print BranchAnalysis.simplification(RB.Edges['RB78'])


AII = CellCointainer(preAII, condition)
#print AII.Edges['AIId']
print BranchAnalysis.simplification(AII.Edges['AIId'])[13895]

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

#XMLutility.CompareTwoCellsComments("c:/d/OFFCBs111815.xml", "ibbon","c:/d/AIIs111815.xml","nput",  200, "CBribbonToinput.txt", "Ribbon-input.txt", "CBribbonToinput.xml")
#XMLutility.CompareTwoCellsComments("c:/d/AIIs111815.xml","utput","c:/d/OFFCBs111815.xml", "nput",  200, "AIoutputToinput.txt", "output-input.txt", "AIoutputToinput.xml")
#XMLutility.CompareTwoCellsComments("c:/d/OFFCBs111815.xml", "ibbon","c:/d/AIIs111815.xml","nput",  100, "CBinputribbon2.txt", "CBdata22.txt", "CBinputribbon2.xml")

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
