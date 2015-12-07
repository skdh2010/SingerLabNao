'''
Created on 2015. 9. 22.

@author: Nao
'''


import lxml.etree as ET
from lxml.builder import E
from lxml.builder import ElementMaker
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

from __builtin__ import str



class XMLinterpreter(object):
    """
    order- Node: z y x id cellname comment
           Edge: target source
           Comment: node content
           Branch: branchpoint
    Attributes://
    z y x id all Int, cellname String 
    z y x are all multiplied by 26 13.2 13.2 and turned into integers
    
    Node: (Dictionary)(cellname : (list)[(list)nodes[z,y,x,id]])
    
    Edge: (Dictionary)(cellname : (list)[(list)edges[soruce,target]]
    Branch2: (list)BranchPointID[]

    comment2: (list)comment[nodes, comment]
    MinMax: (Dictionary)(cell name: (list)MinMax[])
    XMLfile:
    KeyTerm
    """
     
    """
    splitcopy = [copyobject, String]
    
    constructor and extractcopy constructor
    copy constructor finds copy all the nodes in an object and sort out nodes with specific name
    
    
    9/24/15 PLAY WITH DICTIONARY AND SAVE NODES IN DICTIONARY
    """
    
    def __init__(self, fileLocAndName= None):
        if fileLocAndName == None:
            raise Exception('no input bro')
        else:
            self.XMLfile = ET.parse(fileLocAndName)
            self.scale = self.scaleExtract()
            #self.Nodes = self.nodesExtract()
            #self.Comments = self.commentExtract()
            #self.Edges = self.edgesExtract()
            #self.branchExtract()
            
            
            
            #self.Nodes = self.nodesExtact()
    """
    return xml.parameter
    """
    def parameterExtract(self):
        parameter = self.XMLfile.find("parameters") 
        return parameter       
    """
    return scale [z y x]
    currently it is [26 13.2 13.2]
    """
    def scaleExtract(self):
        things= self.XMLfile.getroot()
        children = things.find('parameters/scale')
        scale =[]
        #z = float(children.get("z"))
        #y = float(children.get("y"))
        #x = float(children.get("x"))
        scale.append(26)
        scale.append(13.2)
        scale.append(13.2)
        return scale
    """
    return nodes in dictionary form
    { cell: [z y x id cellName]}
    """
    def nodesExtract(self):
        NonNamedCellIndex = 1
        Nodes = {}
        things = self.XMLfile.getroot()
        #children = things.getchildren()  
        children = things.iterfind('thing')
        for child in children:
            thingCellName = child.get('comment')
            if thingCellName == None:
                thingCellName = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex+1

            Nodes.setdefault(thingCellName)
            Nodes[thingCellName] = []
            for elem in child.iterfind('nodes/node'):
                node = []
                a=int(self.scale[0]*int(elem.get('z')))
                b=int(self.scale[1]*int(elem.get('y')))
                c=int(self.scale[2]*int(elem.get('x')))
                d=int(elem.get('id'))
                node.append(a)
                node.append(b)
                node.append(c)
                node.append(d)
                node.append(thingCellName)
                Nodes[thingCellName].append(node)
            #Nodes[thingCellName].sort(key = lambda x: x[0]) 
        return Nodes
    
    """
    return min and max node number in a cell
    [min max]
    """
    def minmaxExtract(self):
        minmax = {}
        things = self.XMLfile.getroot()
        children = things.iterfind('thing')
        for child in children:
            thingCellName = child.get('comment')
            minmax.setdefault(thingCellName)
            minmax[thingCellName] = []
            mini = 1000000000
            maxi = 0
            for elem in child.iterfind('nodes/node'):
                a = int(elem.get('id'))
                if( a> maxi):
                    maxi = a
                if(a < mini):
                    mini = a        
            minmax[thingCellName].append(mini)
            minmax[thingCellName].append(maxi)
        return minmax
    """
    return list of comments
    [node content]
    """
    def commentExtract(self):
        NonNamedCellIndex = 1
        Comments = []
        things = self.XMLfile.getroot()
        children = things.getchildren()  
        for child in children:
            for elem in child.iterfind('comment'):
                
                
                comment = []
                a = int(elem.get('node'))
                b = elem.get('content')
                if b == None:
                    b = "John Doe" + str(NonNamedCellIndex)
                    NonNamedCellIndex = NonNamedCellIndex+1
                if a == None:
                    continue
                
                
                comment.append(a)
                comment.append(b)
                Comments.append(comment)
        return Comments
    """
    return list of branchpoints
    [branchpoints]
    """
    def branchExtract(self):
        Branches = []
        things = self.XMLfile.getroot()
        children = things.getchildren()  
        for child in children:
            for elem in child.iterfind('branchpoint'):
                a = int(elem.get('id'))
                Branches.append(a)
        return Branches
    
    """
    return edge in dictionary form
    { cell: [target source]}
    """
    def edgesExtract(self):
        Edges = {}
        NonNamedCellIndex = 1
        things = self.XMLfile.getroot()
        #children = things.getchildren()
        children = things.iterfind('thing')  
        for child in children:
            thingCellName = child.get('comment')
            if thingCellName == None:
                thingCellName = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex+1
            Edges.setdefault(thingCellName)
            Edges[thingCellName] = []
            for elem in child.iterfind('edges/edge'):
                edge = []
                a=int(elem.get('target'))
                b=int(elem.get('source'))
                edge.append(a)
                edge.append(b)
                edge.append(thingCellName)
                Edges[thingCellName].append(edge)
        return Edges
    """
    return list of names of cells
    [cellname]
    """
    def nameExtract(self):

        Names = []
        NonNamedCellIndex = 1
        things = self.XMLfile.getroot()
        children = things.iterfind('thing')  
        for child in children:
            Cellname = child.get('comment')
            if Cellname == None:
                Cellname = "Jane Doe" + str(NonNamedCellIndex)
                NonNamedCellIndex = NonNamedCellIndex +1
            Names.append(Cellname)
        return Names
    
    

    
        
#a = XMLinterpreter('d:/annotation.xml')
#print a.nodesExtract()
#print a.edgesExtract()
#print a.commentExtract()
#print a.branchExtract()
#print a.nameExtract()
#print a.minmaxExtract()

    
        