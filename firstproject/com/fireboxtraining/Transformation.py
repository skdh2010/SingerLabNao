'''
Created on 2016. 4. 7.

@author: Nao
'''
import numpy as np
from numpy.linalg import inv
import lxml.etree as ET
from XMLinterpreter import XMLinterpreter
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

CONF95 = 5.991
#CONF95 = 3.841
CONF90 = 3.841

class Transformation(object):



    @staticmethod
    def yzExtract(arrNode):
        aList = []
        for item in arrNode:
            newNode = []
            newNode.append(item[1])
            newNode.append(item[0])
            aList.append(newNode)
        return aList
    
    
    #take away nodes with x coord smaller than cutVal
    @staticmethod
    def findRelatCoord(nodes, botX, topX):
        newDict = {}
        
        for item in nodes.keys():
            newDict.setdefault(item)
            aArray =  nodes[item].sort(key = lambda x:x[2])
            
            #print aArray
            
            MIN = aArray[0][2]
            
            Relength = (topX - MIN)/(topX - botX)
            newDict[item] = Relength
        return newDict;
    
    @staticmethod
    def findMin(nodes):
        minList = []
        for item in nodes.keys():
            aArray =  nodes[item].sort(key = lambda x:x[2])
            MIN = aArray[0][2]            
            minList.append(MIN)
            
        return min(minList)
    
    @staticmethod
    def cutCellX(nodes, cutVal):
        newDict = {}
        
        for item in nodes.keys():
            newDict.setdefault(item)
            
            aArray =  nodes[item].sort(key = lambda x:x[2])
            xKey = [thing[2] for thing in aArray]
            x = bisect_left(xKey, cutVal)
            
            #xSatisList = aArray[0: cutVal]        
        
            xSatisList = aArray[x:]
            
            newDict[item] = xSatisList
    
        return newDict
    
    
    """
    
    ratio1 < ratio2 !
    """
    @staticmethod
    def cutCell2(nodes, ratio1, ratio2):
       
        aArray =  nodes.sort(key = lambda x:x[2])
        #print aArray 
        xKey = []
        
        for item in aArray:
            xKey.append(item[2])
        
        
        #xKey = [thing[2] for thing in aArray]
            
        xTop = bisect_left(xKey, int(ratio2 * len(aArray)))
        xBot = bisect_left(xKey, int(ratio1 * len(aArray)))
        
            #xSatisList = aArray[0: cutVal]        
        
        xSatisList1 = aArray[:xTop]
 
 
        xSatisList2 = xSatisList1[xBot:]
 
        
        return xSatisList2
    
    """
    victimCellss [victimcells]
    
    """
    def Transformation2(self,addressTop, addressBot, victimCellss):
        condition = [True, True, True, True]
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
        
    
    
    @staticmethod
    def transformationCSV(filename, addressTop, addressBot, cutterCells, victimCells):
        condition = [True, True, True, True]
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
        
  
        
        preCellcut = XMLinterpreter(cutterCells)
        Cellcut = CellCointainer(preCellcut, condition)
        Nodescut= Cellcut.Nodes  #dictionary
        
        preCellvic = XMLinterpreter(victimCells)
        Cellvic = CellCointainer(preCellvic, condition)
        Nodesvic= Cellvic.Nodes #dictionary
        
        #Nodesvic = Cellvic.commentWithKeywordExtractDict("ibbon")
        
        ###
        NodesvicAid = Cellvic.Nodes
        ###
       
        
        #DicNodesCCells = {}
        #for item1 in Nodescut.keys():
        #    DicNodesCCells.setdefault(item1)
        #    temp = Transformation.convertCoord(coef, Nodescut[item1])
        #    
        #    DicNodesCCells[item1] = temp
        
        DicNodesVCells = {}
        
        for item2 in Nodesvic.keys():
            DicNodesVCells.setdefault(item2)
            temp1 = Transformation.convertCoord(coef, Nodesvic[item2])
            
            DicNodesVCells[item2] = temp1
            
            """##
        DicNodesVaidCells = {}
        
        for item3 in Nodesvic.keys(): 
            DicNodesVaidCells.setdefault(item3)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item3])
            
            DicNodesVaidCells[item3] = temp2
            """##
        
        with open(filename, 'wb') as csvfile:
            fieldnames = ['relative_length', 'area']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            for item4 in DicNodesVCells.keys():
                
                
                #writer.writeheader()
                
                aEllipse = Covariance.toEllipse(DicNodesVCells[item4])
            
                cellcorX = Transformation.getAvgPoint(DicNodesVCells[item4])[2]
                Relength2 = (topX - cellcorX)/(topX - botX)
                area = CONF95 * pi * aEllipse[2] * aEllipse[3]
                writer.writerow({'relative_length':str(Relength2) , 'area':str(area)})
 
    @staticmethod
    def areaVSrelength2(addressTop, addressBot, victimCells):
        condition = [True, True, True, True]
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
        

        
        preCellvic = XMLinterpreter(victimCells)
        Cellvic = CellCointainer(preCellvic, condition)
        
        Nodesvic= Cellvic.commentWithKeywordExtractDict("nput") #dictionary// smaller

        #Nodesvic = Cellvic.Nodes
        NodesvicAid = Cellvic.Nodes
        
        DicNodesVCells = {}
        DicNodesVaidCells = {}
        DicNodesError = {}
        ells = [] 
               
        for item1 in Nodesvic.keys():
            DicNodesVCells.setdefault(item1)
            
            temp1 = Transformation.convertCoord(coef, Nodesvic[item1])
            
            #temp1 = Transformation.convertCoord(coef, Transformation.cutCell2(Nodesvic[item2], 0.25, 0.75))
            
            cellcorX = Transformation.getMedianPoint(temp1)[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            DicNodesVCells[item1] = Relength2
            
            DicNodesError.setdefault(item1)
            
            stdev = Transformation.abstdev1D(temp1)
            stdev = stdev/(topX-botX)
            DicNodesError[item1] = stdev
            
            
            
            DicNodesVaidCells.setdefault(item1)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item1])
            #temp2 = temp1
            
            aEllipse = Covariance.toEllipse(temp2)
            DicNodesVaidCells[item1] = CONF95 * pi * aEllipse[2] * aEllipse[3]
            
            #if DicNodesVCells[item1] < 1.2:
            #    continue #showing mosaic bigger than 1.15            
            

            aEllipse = Covariance.toEllipse(temp2)
            
            #output [ycor zcor Principle1 Principle2 Angle cellname]
           
            temparr = []            
            
            xcordz = aEllipse[0]
            ycordz = aEllipse[1]
            widthz = aEllipse[2] * 2 * math.sqrt(CONF95) #
            heightz = aEllipse[3] * 2 * math.sqrt(CONF95)  #  
            anglez = aEllipse[4]
            
            xyz = []
            xyz.append(xcordz)
            xyz.append(ycordz)
            
            
            
            temparr.append(Ellipse(xy =xyz, width =widthz, height= heightz, angle = anglez * 180/ pi )) 
            temparr.append(xyz)
            temparr.append(item1)
            ells.append(temparr)            
                

             
        
        ####
        """
        for item4 in DicNodesVCells.keys():
            #if DicNodesVCells[item4] > 1.0:
            #    continue
            
            
            plt.scatter( DicNodesVCells[item4], DicNodesVaidCells[item4], color = Transformation.color(0.8,DicNodesError[item4]), s = 130 )
            
            plt.text(DicNodesVCells[item4], DicNodesVaidCells[item4], item4, ha="center", family='sans-serif', size=10)
            #plt.errorbar(DicNodesVCells[item4], DicNodesVaidCells[item4], xerr = DicNodesError[item4], linestyle = "None", ecolor = Transformation.color(0.8,DicNodesError[item4]))
        show()
        """
        
        ###             
        """
            
        fig = figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        
        for e in ells:
            print e
            ax.add_artist(e[0])
            e[0].set_clip_box(ax.bbox)
            e[0].set_alpha(0.3)
            e[0].set_facecolor(Transformation.color(0.8 ,DicNodesError[e[2]]))
            plt.text(e[1][0], e[1][1], e[2], ha="center", family='sans-serif', size=14)
            
        
        ax.set_xlim(-300000,300000)
        ax.set_ylim(-300000,300000)
        show()
        """
#############convex haul###########################################    
    
        ells1 = []
        for item2 in DicNodesVCells.keys():

            
            if DicNodesVCells[item2] > 1.0:
                continue #showing mosaic bigger than 1.15
## 
            newNode = []
            
            DicNodesVCells.setdefault(item2)
            
            temp1 = Transformation.convertCoord(coef, Nodesvic[item2])
            

            
            cellcorX = Transformation.getMedianPoint(temp1)[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            DicNodesVCells[item2] = Relength2
            
            DicNodesError.setdefault(item2)
            
            stdev = Transformation.abstdev1D(temp1)
            stdev = stdev/(topX-botX)
            DicNodesError[item2] = stdev
            
            
            
            DicNodesVaidCells.setdefault(item2)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item2])
            #print Transformation.yzExtract(temp2)
            hull = ConvexHull(Transformation.yzExtract(temp2))
            
            newNode.append(hull)
            newNode.append(item2)
            newNode.append(Transformation.yzExtract(temp2))
            ells1.append(newNode)
            
        
            
        fig = figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        for e in ells:
            
            #ax.add_artist(e[0])
            #e[0].set_clip_box(ax.bbox)
            #e[0].set_alpha(0.2)
            #e[0].set_facecolor(Transformation.color(0.8 ,DicNodesError[e[2]]))
            plt.text(e[1][0], e[1][1], e[2], ha="center", family='sans-serif', size=14)
                 
        
        
        
        for arr in ells1:
            
            points = arr[2]
            hull = arr[0]

            
            for vertex in hull.simplices:
 
                plt.plot([(points[(vertex[0])])[0], (points[(vertex[1])])[0]], [(points[(vertex[0])])[1],(points[(vertex[1])])[1]], c =Transformation.color(0.8 ,DicNodesError[arr[1]]) )
            
            
            #convex_hull_plot_2d(arr[0], ax)

        ax.set_xlim(-300000,300000)
        ax.set_ylim(-300000,300000)
        show()    
        
 
 
                
    @staticmethod
    def areaVSrelength(addressTop, addressBot, victimCells):
        condition = [True, True, True, True]
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
        

        
        preCellvic = XMLinterpreter(victimCells)
        Cellvic = CellCointainer(preCellvic, condition)
        
        Nodesvic= Cellvic.commentWithKeywordExtractDict("utput") #dictionary// smaller
        print Nodesvic
        #Nodesvic = Cellvic.Nodes
        NodesvicAid = Cellvic.Nodes
        
        DicNodesVCells = {}
        DicNodesVaidCells = {}
        DicNodesError = {}
        ells = [] 
               
        for item1 in Nodesvic.keys():
            DicNodesVCells.setdefault(item1)
            
            temp1 = Transformation.convertCoord(coef, Nodesvic[item1])
            
            #temp1 = Transformation.convertCoord(coef, Transformation.cutCell2(Nodesvic[item2], 0.25, 0.75))
            
            cellcorX = Transformation.getAvgPoint(temp1)[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            DicNodesVCells[item1] = Relength2
            
            DicNodesError.setdefault(item1)
            
            stdev = Transformation.stdev1D(temp1)
            stdev = stdev/(topX-botX)
            DicNodesError[item1] = stdev
            
            
            
            DicNodesVaidCells.setdefault(item1)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item1])
            #temp2 = temp1
            
            aEllipse = Covariance.toEllipse(temp2)
            DicNodesVaidCells[item1] = CONF95 * pi * aEllipse[2] * aEllipse[3]
            
            #if DicNodesVCells[item1] < 1.2:
            #    continue #showing mosaic bigger than 1.15            
            

            aEllipse = Covariance.toEllipse(temp2)
            
            #output [ycor zcor Principle1 Principle2 Angle cellname]
           
            temparr = []            
            
            xcordz = aEllipse[0]
            ycordz = aEllipse[1]
            widthz = aEllipse[2] * 2 * math.sqrt(CONF95) #
            heightz = aEllipse[3] * 2 * math.sqrt(CONF95)  #  
            anglez = aEllipse[4]
            
            xyz = []
            xyz.append(xcordz)
            xyz.append(ycordz)
            
            
            
            temparr.append(Ellipse(xy =xyz, width =widthz, height= heightz, angle = anglez * 180/ pi )) 
            temparr.append(xyz)
            temparr.append(item1)
            ells.append(temparr)            
        """        
        ## del ##
        
        DicNodesVCells.setdefault("top")
             
        cellcorX = Transformation.getAvgPoint(Nodestop)[2]
        Relength2 = (topX - cellcorX)/(topX - botX)
        DicNodesVCells["top"] = Relength2
            
        DicNodesError.setdefault("top")
            
        stdev = Transformation.stdev1D(Nodestop)
        stdev = stdev/(topX-botX)
        DicNodesError["top"] = stdev
            
            
            
        DicNodesVaidCells.setdefault("top")
        temp2 = Transformation.convertCoord(coef, Nodestop)
            #temp2 = temp1
            
        aEllipse = Covariance.toEllipse(temp2)
        DicNodesVaidCells["top"] = CONF95 * pi * aEllipse[2] * aEllipse[3]
        



        DicNodesVCells.setdefault("bot")
             
        cellcorX = Transformation.getAvgPoint(Nodesbot)[2]
        Relength2 = (topX - cellcorX)/(topX - botX)
        DicNodesVCells["bot"] = Relength2
            
        DicNodesError.setdefault("bot")
            
        stdev = Transformation.stdev1D(Nodesbot)
        stdev = stdev/(topX-botX)
        DicNodesError["bot"] = stdev
            
            
            
        DicNodesVaidCells.setdefault("bot")
        temp2 = Transformation.convertCoord(coef, Nodesbot)
            #temp2 = temp1
            
        aEllipse = Covariance.toEllipse(temp2)
        DicNodesVaidCells["bot"] = CONF95 * pi * aEllipse[2] * aEllipse[3]
        
        """     
        
        ####
        """
        for item4 in DicNodesVCells.keys():
            #if DicNodesVCells[item4] > 1.0:
            #    continue
            
            
            plt.scatter( DicNodesVCells[item4], DicNodesVaidCells[item4], color = Transformation.color(0.8,DicNodesError[item4]), s = 130 )
            
            plt.text(DicNodesVCells[item4], DicNodesVaidCells[item4], item4, ha="center", family='sans-serif', size=10)
            #plt.errorbar(DicNodesVCells[item4], DicNodesVaidCells[item4], xerr = DicNodesError[item4], linestyle = "None", ecolor = Transformation.color(0.8,DicNodesError[item4]))
        show()
        """
        
        

        ###             
        """
            
        fig = figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        
        for e in ells:
            print e
            ax.add_artist(e[0])
            e[0].set_clip_box(ax.bbox)
            e[0].set_alpha(0.3)
            e[0].set_facecolor(Transformation.color(0.8 ,DicNodesError[e[2]]))
            plt.text(e[1][0], e[1][1], e[2], ha="center", family='sans-serif', size=14)
            
        
        ax.set_xlim(-300000,300000)
        ax.set_ylim(-300000,300000)
        show()
        """
#############convex haul###########################################    
    
        ells1 = []
        for item2 in DicNodesVCells.keys():

            
            #if DicNodesVCells[item2] < 1.2:
            #    continue #showing mosaic bigger than 1.15
## 
            newNode = []
            
            DicNodesVCells.setdefault(item2)
            
            temp1 = Transformation.convertCoord(coef, Nodesvic[item2])
            

            
            cellcorX = Transformation.getAvgPoint(temp1)[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            DicNodesVCells[item2] = Relength2
            
            DicNodesError.setdefault(item2)
            
            stdev = Transformation.stdev1D(temp1)
            stdev = stdev/(topX-botX)
            DicNodesError[item2] = stdev
            
            
            
            DicNodesVaidCells.setdefault(item2)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item2])
            #print Transformation.yzExtract(temp2)
            hull = ConvexHull(Transformation.yzExtract(temp2))
            
            newNode.append(hull)
            newNode.append(item2)
            newNode.append(Transformation.yzExtract(temp2))
            ells1.append(newNode)
            
        
            
        fig = figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        for e in ells:
            
            #ax.add_artist(e[0])
            #e[0].set_clip_box(ax.bbox)
            #e[0].set_alpha(0.2)
            #e[0].set_facecolor(Transformation.color(0.8 ,DicNodesError[e[2]]))
            plt.text(e[1][0], e[1][1], e[2], ha="center", family='sans-serif', size=14)
                 
        
        
        
        for arr in ells1:
            
            points = arr[2]
            hull = arr[0]

            
            for vertex in hull.simplices:
 
                plt.plot([(points[(vertex[0])])[0], (points[(vertex[1])])[0]], [(points[(vertex[0])])[1],(points[(vertex[1])])[1]], c =Transformation.color(0.8 ,DicNodesError[arr[1]]) )
            
            
            #convex_hull_plot_2d(arr[0], ax)
        
        i = 0
        
        while i < (len(ells1) - 1):
            fIndex = i
            sIndex = i-1
            
            first = Transformation.verticesToPoints(ells1[fIndex][0], ells1[fIndex][2])
            second = Transformation.verticesToPoints(ells1[sIndex][0], ells1[sIndex][2])
            
            
            i = i + 1
            
            collidng = Transformation.ClipPolygon(first, second)
            for item in collidng:
                 plt.scatter( item[0], item[1], s = 130 )
        
        
        ax.set_xlim(-300000,300000)
        ax.set_ylim(-300000,300000)
        show()    
    

    ####################################################################
    
    
    
    
    @staticmethod
    def verticesToPoints(hull, points):
        outputz = []
        for vertex in hull.vertices:
            newPt = []
            newPt.append(points[vertex][0])
            newPt.append(points[vertex][1])
            
            outputz.append(newPt)
            
            
        return outputz    
    
    @staticmethod
    def ClipPolygon(subjectPolygon, clipPolygon):
        def inside(p):
            return(cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0])
 
        def computeIntersection():
            dc = [ cp1[0] - cp2[0], cp1[1] - cp2[1] ]
            dp = [ s[0] - e[0], s[1] - e[1] ]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0] 
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3]
 
        outputList = subjectPolygon
      
        cp1 = clipPolygon[-1]
 
        for clipVertex in clipPolygon:
            cp2 = clipVertex
            inputList = outputList
            outputList = []
            print inputList
            s = inputList[-1]
 
            for subjectVertex in inputList:
                e = subjectVertex
                if inside(e):
                    if not inside(s):
                        outputList.append(computeIntersection())
                    outputList.append(e)
                elif inside(s):
                    outputList.append(computeIntersection())
                s = e
            cp1 = cp2
        return(outputList)
    
    
            
    """ for avg and std """
    @staticmethod
    def color(val1, std):
        if std < 0.1:
            return 'k'
        
        if std < 0.20 * val1:
            return 'b'
        
        
        if std < 0.3 * val1:
            return 'g'  
                
        if std < 0.4 * val1:
            return 'r'
        
        if std < 0.5 * val1:
            return 'm'
    
        else:
            return 'y'
    
    
    """ for median and med absolute std  """
    @staticmethod
    def color2(val1, std):
        if std < 0.1:
            return 'k'
        
        if std < 0.20 * val1:
            return 'b'
        
        
        if std < 0.3 * val1:
            return 'g'  
                
        if std < 0.4 * val1:
            return 'r'
        
        if std < 0.5 * val1:
            return 'm'
    
        else:
            return 'y'
    
    @staticmethod
    def color3(val1):
        
        if val1 > 1.15:
            return 'r'
        
        else:
            return 'b'

    
    """
     address cells == args """
    @staticmethod
    def Transformation(addressTop, addressBot, cutterCells, victimCells):
        condition = [True, True, True, True]
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
        
        preCellcut = XMLinterpreter(cutterCells)
        Cellcut = CellCointainer(preCellcut, condition)
        Nodescut= Cellcut.Nodes  #dictionary
        
        preCellvic = XMLinterpreter(victimCells)
        Cellvic = CellCointainer(preCellvic, condition)
        Nodesvic= Cellvic.Nodes #dictionary
        
        #Nodesvic = Cellvic.commentWithKeywordExtractDict("ibbon")
        
        ###
        #NodesvicAid = Cellvic.Nodes
        ###
       
        
        #DicNodesCCells = {}
        #for item1 in Nodescut.keys():
        #    DicNodesCCells.setdefault(item1)
        #    temp = Transformation.convertCoord(coef, Nodescut[item1])
        #    
        #    DicNodesCCells[item1] = temp
        
        DicNodesVCells = {}
        
        for item2 in Nodesvic.keys():
            DicNodesVCells.setdefault(item2)
            temp1 = Transformation.convertCoord(coef, Nodesvic[item2])
            
            DicNodesVCells[item2] = temp1
            
            """##
        DicNodesVaidCells = {}
        
        for item3 in Nodesvic.keys(): 
            DicNodesVaidCells.setdefault(item3)
            temp2 = Transformation.convertCoord(coef, NodesvicAid[item3])
            
            DicNodesVaidCells[item3] = temp2
           
        
       
        for item4 in DicNodesVCells.keys():
            
            aEllipse = Covariance.toEllipse(DicNodesVCells[item4])
            
            cellcorX = Transformation.getAvgPoint(DicNodesVCells[item4])[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            
            
            plt.scatter( Relength2  , CONF95 * pi * aEllipse[2] * aEllipse[3])
        
        show()
        
        #cutVal = Transformation.findMin(DicNodesCCells)
        #DicNodesVCells = Transformation.cutCellX(DicNodesVCells, cutVal)
        
        """
        ells = []
        
        for item3 in DicNodesVCells.keys():
                       
            cellcorX = Transformation.getAvgPoint(DicNodesVCells[item3])[2]
            Relength2 = (topX - cellcorX)/(topX - botX)
            
            if Relength2 > 1.15:
                continue #showing mosaic bigger than 1.15
            
            aEllipse = Covariance.toEllipse(DicNodesVCells[item3])
            
            #output [ycor zcor Principle1 Principle2 Angle cellname]
           
            temparr = []            
            
            xcordz = aEllipse[0]
            ycordz = aEllipse[1]
            widthz = aEllipse[2] * 2 * math.sqrt(CONF95) #
            heightz = aEllipse[3] * 2 * math.sqrt(CONF95)  #  
            anglez = aEllipse[4]
            
            xyz = []
            xyz.append(xcordz)
            xyz.append(ycordz)
            
            temparr.append(Ellipse(xy =xyz, width =widthz, height= heightz, angle = anglez * 180/ pi )) 
            temparr.append(xyz)
            temparr.append(item3)
            ells.append(temparr)
            
            
            
        fig = figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        for e in ells:
            ax.add_artist(e[0])
            e[0].set_clip_box(ax.bbox)
            e[0].set_alpha(rand())
            e[0].set_facecolor(rand(3))
            plt.text(e[1][0], e[1][1], e[2], ha="center", family='sans-serif', size=14)
            
        
        ax.set_xlim(-100000,200000)
        ax.set_ylim(000000,200000)
        show()
  
    
    @staticmethod
    def convertCoord(coef, allNodes):
        """
        change to x y z then convert to z y x. disaster from my old mistake.
        """
        FirstCol = []
        
        norm1 = coef[2] * coef[2] + coef[1] * coef[1] + coef[0] * coef[0]
        
        FirstCol.append(-coef[2]/norm1)
        FirstCol.append(-coef[1]/norm1)
        FirstCol.append(-coef[0]/norm1)


        tempY = []
        tempY.append(0)
        tempY.append(0)
        tempY.append(1)
        SecCol = Transformation.cross(tempY, FirstCol )
                
        ThrCol = Transformation.cross(FirstCol, SecCol)
        
        
        Matrix = []
        Matrix.append(FirstCol)
        Matrix.append(SecCol)
        Matrix.append(ThrCol)
           
        aMatrix = np.array(Matrix)
        aMatrix = np.transpose(aMatrix)
        invMat = inv(aMatrix)
        
        returner = []
        
        for item in allNodes:
            temper = []
            temper.append(item[2])
            temper.append(item[1])
            temper.append(item[0])
            Avector = np.array(temper)
            newCoord = (np.dot(invMat, Avector)).tolist()
            
            #print item
            item[2] = newCoord[0]
            item[1] = newCoord[1]
            item[0] = newCoord[2]
            
            returner.append(item)
            #print item
            
        return returner
        
        """
        print coef
        sinVal1 = coef[2]/math.sqrt(coef[2] * coef[2] + coef[1] * coef[1])
        cosVal1 = coef[1]/math.sqrt(coef[2] * coef[2] + coef[1] * coef[1])
        
        sinVal2 = math.sqrt(coef[2] * coef[2] + coef[1] * coef[1])/ math.sqrt(coef[2] * coef[2] + coef[1] * coef[1] + coef[0] * coef[0])
        cosVal2 = coef[0]/ math.sqrt(coef[2] * coef[2] + coef[1] * coef[1] + coef[0] * coef[0])
        
        for item in allNodes:
            new_x1 = sinVal1 * item[1] + cosVal1 * item[2]
            new_y1 = -sinVal1 * item[2] + cosVal1 * item[1]
            new_z1 = item[0]
            
            new_x2 = cosVal2 * new_x1 - sinVal2 * new_z1
            new_y2 = new_y1
            new_z2 = cosVal2 * new_z1 + sinVal2 * new_x1
            
            item[2] = new_x2
            item[1] = new_y2
            item[0] = new_z2
        
        
        
        
        return allNodes
        """
        
        
        
    @staticmethod
    def getNewCoord(allNodes):
        #preTop = XMLinterpreter(addressTop)
        #condition  = [True, False, False, False]
        Plane = Transformation.getPlaneCoef2(allNodes)
        
        coord = Transformation.getAvgPoint(allNodes)
        
        Plane.append(Transformation.getPlaneConst(Plane, coord))
        
        return Plane
            
    @staticmethod
    def getPlaneConst(coef, coord):
        d = -(coef[0]*coord[0] + coef[1] * coord[1] + coef[2] * coord[2])
        return d
    # ax + by + cz + d = 0, return [a,b,c]    
    @staticmethod
    def getPlaneCoef2(allNodes):
        
        # 3d square fitting
        length = len(allNodes)
        sum_zz = 0.0
        sum_z = 0.0
        sum_zy = 0.0
        sum_yy = 0.0
        sum_y = 0.0
        
        sum_zx = 0.0
        sum_yx = 0.0
        sum_x = 0.0
        for item in allNodes:
            z_cor = item[0]
            y_cor = item[1]
            x_cor = item[2]
        
            sum_zz = sum_zz + z_cor*z_cor
            sum_z = sum_z + z_cor
            sum_zy = sum_zy + z_cor*y_cor
            sum_yy = sum_yy + y_cor*y_cor
            sum_y = sum_y + y_cor
            
            sum_zx = sum_zx + z_cor*x_cor
            sum_yx = sum_yx + y_cor*x_cor
            sum_x = sum_x + x_cor
        Matrix = []
        firstrow = []
        firstrow.append(sum_zz)
        firstrow.append(sum_zy)
        firstrow.append(sum_z)
        
        secondrow = []
        secondrow.append(sum_zy)
        secondrow.append(sum_yy)
        secondrow.append(sum_y)
        
        thirdrow = []
        thirdrow.append(sum_z)
        thirdrow.append(sum_y)
        thirdrow.append(length)
        
        Matrix.append(firstrow)
        Matrix.append(secondrow)
        Matrix.append(thirdrow)
        
        vector = []
        vector.append(sum_zx)
        vector.append(sum_yx)
        vector.append(sum_x)
    
        Amatrix = np.array(Matrix)
        Ainverse= inv(Amatrix)
        Avector = np.array(vector)
        Coef = (np.dot(Ainverse, Avector)).tolist()
        #print Coef;
        c = []
        
        c.append(Coef[0])
        c.append(Coef[1])
        c.append(-1)
        c.append(Coef[2])
        
        return c;
        """
        comp1 = Coef[0]
        comp2 = Coef[1]
        comp3 = Coef[2]
        
        normalization = math.sqrt(comp1 * comp1 + comp2 * comp2 + comp3 * comp3)
        
        comp1 = comp1/normalization
        comp2 = comp2/normalization
        comp3 = comp3/normalization    
        
        c = []
        c.append(comp1)
        c.append(comp2)
        c.append(comp3)
        #print c
        
        return c
        """
        
        
        
    """
    [z,y,x ...
    
    
    """
    @staticmethod
    def stdev1D (aList):
        sum = 0
        for item in aList:
            sum = sum + item[2]
        avg = sum/len(aList)
        
        
        var = 0
        for item in aList:
            var = var + (item[2] - avg) * (item[2] - avg)
            
        var = var/len(aList)  # it should be n - 1, but it make no difference
        
        return math.sqrt(var)
    
    @staticmethod
    def abstdev1D (aList):
        avgVal = Transformation.getAvgPoint(aList)[2]
        newList = []
        
        for item in aList:
            newList.append(math.fabs(item[2]-avgVal))
        
        newList.sort()
        print newList
        val = newList[len(newList)/2]
        
        return val
    
    
    @staticmethod
    def getPlaneCoef1(Cell):
        #ignore x coordinates
        allNodesY = Cell.allNodesExtract(1) 
        allNodesZ = Cell.allNodesExtract(0)
        
        Length = len(allNodesY)
        Average = Transformation.getAvgPoint(allNodesY)
        
        Ylow = Transformation.getAvgPoint(allNodesY[:Length/2])
        Yhigh = Transformation.getAvgPoint(allNodesY[Length/2:])
        Yvector = Transformation.generateVector(Ylow, Yhigh)
        
        Zlow = Transformation.getAvgPoint(allNodesZ[:Length/2])
        Zhigh = Transformation.getAvgPoint(allNodesZ[Length/2:])
        Zvector = Transformation.generateVector(Zlow, Zhigh)
        
        crossProduct = Transformation.cross(Yvector, Zvector)
        return crossProduct
    
    @staticmethod    
    def cross(a, b):
        comp1 = a[1]*b[2] - a[2]*b[1]
        comp2 = a[2]*b[0] - a[0]*b[2]
        comp3 = a[0]*b[1] - a[1]*b[0]

        normalization = math.sqrt(comp1 * comp1 + comp2 * comp2 + comp3 * comp3)
        
        comp1 = comp1/normalization
        comp2 = comp2/normalization
        comp3 = comp3/normalization    
        
        c = []
        c.append(comp1)
        c.append(comp2)
        c.append(comp3)
        
        return c
        
        
    @staticmethod
    def generateVector(coordinate1, coordinate2):
        zcor = coordinate1[0] - coordinate2[0]
        ycor = coordinate1[1] - coordinate2[1]
        xcor = coordinate1[2] - coordinate2[2]
        vector = []
        
        vector.append(zcor)
        vector.append(ycor)
        vector.append(xcor)
        return vector
    
    @staticmethod
    def getAvgPoint(aList):
        xsum = 0
        ysum = 0
        zsum = 0
        length = len(aList)
        
        for item in aList:
            zsum = zsum + item[0]
            ysum = ysum + item[1]
            xsum = xsum + item[2]
            
        xsum = xsum/length
        ysum = ysum/length
        zsum = zsum/length
        #lets keep them z, y, x
        avgPoint = []
        avgPoint.append(zsum)
        avgPoint.append(ysum)
        avgPoint.append(xsum)
        
        return avgPoint
    
    
    @staticmethod
    def getMedianPoint(aList):
   
        
        xArray =  sorted(aList, key = lambda x:x[2])
        
        
        
        
        yArray =  sorted(aList, key = lambda y:y[1])
        zArray =  sorted(aList, key = lambda z:z[0])
        
        returnList = []

        returnList.append(zArray[len(aList)/2][0])
        returnList.append(yArray[len(aList)/2][1])
        returnList.append(xArray[len(aList)/2][2])
        
        return returnList
        
        