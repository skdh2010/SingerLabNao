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
    def FindStartingPoint(Edge):
        Source = set()
        Target = set()
        for item in Edge:
            Source.add(item[1])
            Target.add(item[0])
        
        Source.difference_update(Target)
        return list(Source)
    
    @staticmethod
    def EdgeToDict(Edge):
        StartList = BranchAnalysis.FindStartingPoint(Edge)
        if(len(StartList) !=1):
            raise Exception('Error in Data: No starting point')
        else:
            Edges = set()
            for item in Edge:
                Edges.add(item[0])
                Edges.add(item[1])
            #sort by Source [1]
            
            Dict = {}
            for item in Edges:
                Dict.setdefault(item)
                Dict[item] = []
                for item1 in Edge:
                    if(item1[1] == item):
                        Dict[item].append(item1[0])
            
            return Dict
        
    @staticmethod
    def simplification(Edge):
        Dict = BranchAnalysis.EdgeToDict(Edge)
        startPoint = BranchAnalysis.FindStartingPoint(Edge)
        output = {}
        print startPoint
        BranchAnalysis.recurSimplify(startPoint[0], Dict, output)
        return output
    
    
    @staticmethod
    def recurSimplify(startPoint, dict0, output):
        if(len(dict0[startPoint])==0):
            output.setdefault(startPoint)
            output[startPoint] = ["EndMark"]
        
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
                    BranchAnalysis.recurSimplify(item, dict0, output)
                
                
    