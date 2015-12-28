'''
Created on 2015. 12. 2.

@author: Nao
'''
from _elementtree import TreeBuilder
class TreeNode:
    def __init__(self, node):
        self.Node = node #integer
        self.SubTree = []
    
    def addTree(self, TreeNode):
        self.SubTree.append(TreeNode)
    def getNode(self):
        return self.Node



class BranchAnalysis:

    @staticmethod
    def StrahlerCalc(intlist):
        count = 0
        biggest = 0
        for item in intlist:
            if item > biggest:
                biggest = item
        for item1 in intlist:
            if item1 == biggest:
                count = count +1
        if count <2:
            return biggest
        else:
            return biggest + 1        
        
           
    @staticmethod
    def singleStrahlerAux(dictTree, point):
        hello = dictTree[point]
        listPass = []
        if len(hello) == 0:
            return 1;
        elif len(hello) ==1:
            if hello[0] == -1:
                return 0; 
            else:
                return BranchAnalysis.singleStrahlerAux(dictTree, hello[0])
        else:
            for item in hello:
                listPass.append(BranchAnalysis.singleStrahlerAux(dictTree, item))
            return BranchAnalysis.StrahlerCalc(listPass)
    
    ## fix THIZ
    @staticmethod 
    def singleStrahler(Edge, startPoint):
        Tree = BranchAnalysis.simplification1(Edge, startPoint)

        print Tree 
        return BranchAnalysis.singleStrahlerAux(Tree, startPoint)
    @staticmethod
    def Strahler(Cell):
        edges = Cell.Edges
        startPoints = Cell.findStartingPoints()
        returner = []
        for item in edges.keys():
            returner.append(BranchAnalysis.singleStrahler(edges[item]), startPoints[item])
        return returner
    
    @staticmethod
    def debugStart(Cell):
        edges = Cell.Edges
        returner = {}
        for item in edges.keys():
            returner.setdefault(item)
            returner[item] = BranchAnalysis.FindStartingPoint(edges[item])

        return returner
    """build undirected tree"""
    @staticmethod
    def treefy(Edge):
        AllEdge = set()
        Tree = {}
        for item in Edge:
            AllEdge.add(item[1])
            AllEdge.add(item[0])
        for item1 in AllEdge:
            Tree.setdefault(item1)
            Tree[item1] = set()
        for item2 in Edge:
            Tree[item2[0]].add(item2[1])
            Tree[item2[1]].add(item2[0])
        return Tree
        
    """undirected -> directed """
    @staticmethod
    def directify(Edge, startingP):
        UDtree =BranchAnalysis.treefy(Edge)
        
        BranchAnalysis.directify_Aux(None, startingP, UDtree)
        return UDtree
        
        
    """ delete predecessor and run recursion on thiz"""
    @staticmethod
    def directify_Aux(pred, thiz, Tree):
        if pred != None:
            Tree[thiz].discard(pred)
        for item in Tree[thiz]:
            BranchAnalysis.directify_Aux(thiz, item, Tree)
        return Tree
    @staticmethod
    def transition(tree):
        for item in tree.keys():
            tree[item] = list(tree[item])
        return tree
    @staticmethod
    def simplification1(Edge, startingP):
        Dict = BranchAnalysis.transition(BranchAnalysis.directify(Edge, startingP))
        startPoint = startingP
        output = {}
        print startPoint
        BranchAnalysis.recurSimplify1(startPoint, Dict, output)
        return output
    
    
    @staticmethod
    def recurSimplify1(startPoint, dict0, output):
        if(len(dict0[startPoint])==0):
            negativeList = []
            negativeList.append(-1)
            
            output.setdefault(startPoint)
            output[startPoint] = negativeList
        
        else:
            tmp =dict0[startPoint]
            
            markEdge = startPoint
            
            while(len(tmp)==1):
                tmp1 =tmp[0]
                tmp = dict0[tmp1]
                markEdge = tmp1
            output.setdefault(startPoint)
            output[startPoint] = tmp
            
            if(len(tmp)==0):
                output.setdefault(startPoint)
                output[startPoint] = []
            
            else:
                for item in tmp:
                    BranchAnalysis.recurSimplify1(item, dict0, output)

        
        
         