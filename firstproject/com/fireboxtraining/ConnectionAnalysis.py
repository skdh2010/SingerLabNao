'''
Created on 2016. 6. 7.

@author: Nao
'''
import numpy as np
from numpy.linalg import inv
import lxml.etree as ET
from com.fireboxtraining.XMLinterpreter import XMLinterpreter
from com.fireboxtraining.CellsCointainer import CellCointainer
from _bisect import bisect_left
from bisect import bisect_right
import sys
from numpy import pi
from Covariance import Covariance
import pprint
import math
from XMLutility import XMLutility
from scipy.spatial import convex_hull_plot_2d
from scipy.spatial import ConvexHull
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import xcorr
from numpy import average
from matplotlib.patches import Ellipse
import numpy as np
from pylab import figure, show, rand
import csv
from matplotlib.pyplot import *
from statsmodels.sandbox.nonparametric.densityorthopoly import FPoly
from Transformation import Transformation
from shapely.geometry import Polygon

CONF95 = 5.991
#CONF95 = 3.841
CONF90 = 3.841

class ConnectionAnalysis(object):
    
    """ AII first, CB next (small one first, then big one)"""
    @staticmethod    
    def areaVSconnection(addressTop, addressBot,address1,key1,address2,key2,threshold, extraname = ''):

        condition  = [True, True, True, True]
        preCB = XMLinterpreter(address1) #cb and ac are misnomers; i should correct it later.
        preAC = XMLinterpreter(address2)        
        
        CB = CellCointainer(preCB, condition)
        AC = CellCointainer(preAC, condition)
        comments1 = CB.commentWithKeywordExtract(key1)
        comments2 = AC.commentWithKeywordExtract(key2)
        comments1.sort(key = lambda x:x[1])
        comments2.sort(key = lambda x:x[1])
        comments1a = XMLutility.sortNodes(comments1)
        CBAC =XMLutility.compareTwoCellForFirst(CB.scale,comments1, comments2, threshold, 1)
        CBACsorted =XMLutility.sortNodes(CBAC)
        
       # CBACsorted = XMLutility.dictToCluster(CBACsorted, 200)
        CBACsorted1 =XMLutility.DLtoDDtoDCL(CBAC,200) #it works; i haven't looked at my actual code
        """ Part 1 above"""

        preCelltop = XMLinterpreter(addressTop)
        Celltop = CellCointainer(preCelltop, condition)
        Nodestop= Celltop.allNodesExtract(0)

        preCellbot = XMLinterpreter(addressBot)
        Cellbot = CellCointainer(preCellbot, condition)
        Nodesbot= Cellbot.allNodesExtract(0)
        
        coef = Transformation.getPlaneCoef2(Nodestop)
        
        Nodestop = Transformation.convertCoord(coef, Nodestop)
        Nodesbot = Transformation.convertCoord(coef, Nodesbot)
        
        topX = Transformation.getAvgPoint(Nodestop)[2]
        botX = Transformation.getAvgPoint(Nodesbot)[2]        
        
        Nodesvic = AC.Nodes
        #Nodesvic = AC.commentWithKeywordExtractDict("utput")
        
        #Nodescut = CB.Nodes
        Nodescut = CB.commentWithKeywordExtractDict("utput")
        
        DicPolyV = {}
        relLengV = {}
        
        for item1 in Nodesvic.keys():
            DicPolyV.setdefault(item1)
            relLengV.setdefault(item1)
            temp1 = Transformation.convertCoord(coef, Nodesvic[item1])
            
            xVal = Transformation.getAvgPoint(temp1)[2]
            relLengV[item1] = xVal
            
            points1=Transformation.yzExtract(temp1)
            hull1 = ConvexHull(points1)
            
            DicPolyV[item1] = Polygon(ConnectionAnalysis.vertexToPoly(hull1, points1))
            
        DicPolyC = {}
        for item2 in Nodescut.keys():
            DicPolyC.setdefault(item2)
            temp2 = Transformation.convertCoord(coef, Nodescut[item2])
            points2= Transformation.yzExtract(temp2)
            hull2 = ConvexHull(points2)
            
            DicPolyC[item2] = Polygon(ConnectionAnalysis.vertexToPoly(hull2, points2))
            
            """implement the drawing! """
            
        print DicPolyC
        print DicPolyV
            
        for item3 in DicPolyC.keys():
            
            fname = item3 + extraname+ '.pdf'
            fnameCSV = item3 +extraname+'.csv'
            fnamehull = item3+ extraname + '_hull.pdf'
            VAreaSet = set(CBACsorted1[item3].keys())
   
            for item4 in DicPolyV.keys():
                    
                    
                if item4 in VAreaSet:
                        # connection vs area
                    plt.text(len(CBACsorted1[item3][item4]), (DicPolyC[item3].intersection(DicPolyV[item4])).area, item4, ha = "center", family = 'sans-serif', size=10 )    
                    plt.scatter(len(CBACsorted1[item3][item4]), (DicPolyC[item3].intersection(DicPolyV[item4])).area )    
                        
                #else:
                    #plt.scatter(0, (DicPolyC[item3].intersection(DicPolyV[item4])).area )
                    #plt.text(0, (DicPolyC[item3].intersection(DicPolyV[item4])).area, item4, ha = "center", family = 'sans-serif', size=10 )
                    
                
            plt.savefig(fname, format = 'pdf')
            
            plt.clf()
            
            for item8 in ConnectionAnalysis.PolygonToDrawable(DicPolyC[item3]):
                plt.plot([item8[0], item8[1]], [item8[2], item8[3]], color ='k')
            textCoord = ConnectionAnalysis.PolygonAvgPoint(DicPolyC[item3])
            plt.text(textCoord[0], textCoord[1], item3, ha = "center", family = 'sans-serif', size=10)
                
                
            for item6 in DicPolyV.keys():
               if DicPolyC[item3].intersects(DicPolyV[item6]) and item6 in VAreaSet:
                
                    for item7 in ConnectionAnalysis.PolygonToDrawable(DicPolyV[item6]):
                        
                        
                        releng = (topX-relLengV[item6])/(topX-botX)
                        plt.plot([item7[0], item7[1]], [item7[2], item7[3]], color = Transformation.color3(releng))
                    textCoord = ConnectionAnalysis.PolygonAvgPoint(DicPolyV[item6])
                    plt.text(textCoord[0], textCoord[1], item6, ha = "center", family = 'sans-serif', size=10)
            
            plt.savefig(fnamehull, format = 'pdf')
           
            plt.clf()
                        
                        
            with open(fnameCSV, 'wb') as csvfile:
                fieldnames = ['connectTo','# of connection','intersecting area']
                writer = csv.DictWriter(csvfile, fieldnames =fieldnames)
                
                for item5 in DicPolyV.keys():
                    if item5 in VAreaSet:
                        writer.writerow({'connectTo': item5, '# of connection': str(len(CBACsorted1[item3][item5])), 'intersecting area':str((DicPolyC[item3].intersection(DicPolyV[item5])).area)})
                    else:
                        writer.writerow({'connectTo': item5, '# of connection': str(0), 'intersecting area':str((DicPolyC[item3].intersection(DicPolyV[item5])).area)})
            
           
           
            
    @staticmethod
    def PolygonToDrawable(bolygon):
        x,y = bolygon.exterior.xy
        returnList = []
        i = 0
        while i < len(x) -1:
            temp = []
            temp.append(x[i])
            
            temp.append(x[i+1])
            temp.append(y[i])
            temp.append(y[i+1])
            
            returnList.append(temp)
            i = i+1
        return returnList
    
    @staticmethod
    def PolygonAvgPoint(bolygon):
        x,y = bolygon.exterior.xy
        xsum = 0
        ysum = 0
        i = 0
        while i < len(x) - 1:
            xsum = xsum + x[i]
            ysum = ysum + y[i]
            i = i+1
        
        xsum = xsum/(len(x) - 1)
        ysum = ysum/(len(x) - 1)
        
        returnlist = []
        returnlist.append(xsum)
        returnlist.append(ysum)
        
        return returnlist
        
        
            
    
    
    @staticmethod
    def vertexToPoly(hull, points):
        returnList = []
        vertex = hull.vertices
        
        for item in vertex:
            returnList.append(points[item])
        return returnList
        
        
        