'''
Created on 2015. 10. 8.

@author: Nao
'''
from com.fireboxtraining.XMLinterpreter import XMLinterpreter

class CellCointainer(object):
    """
    condition boolean list: [node comment edge branch]
   
   Nodes { cell: [z y x id cellName]}
   Comments { cell: [z y x id cellName comment]}
   Edges { cell: [target source]}
   Branches { cell: [z y x id cellName branchpoint]}
   Names [name of cell]
   MinMax non-used
   Parameter xml.parameter
   scale: [z y x]
    """
    def __init__(self, secondInput = None, NCBEboolean = None, Cellnames = None):
        self.Nodes = None
        self.Comments = None
        self.Edges = None
        self.Branches = None
        self.Names = None
        self.MinMax = None
        self.Parameter = None
        self.scale = secondInput.scale
        if(NCBEboolean == None):
            raise Exception('no inputbro')
        
        elif(isinstance(secondInput,XMLinterpreter)):
            Name = secondInput.nameExtract()
            self.Names = self.__getNameOfCells(Name, Cellnames)
            #minmax = secondInput.minmaxExtract()
            #self.MinMax = self.__minmaxExtract(minmax)
            self.Parameter = secondInput.parameterExtract()
            
            if(NCBEboolean[0]):
                Nodes = secondInput.nodesExtract()
                self.Nodes =self.__cellExtract(Nodes)
            if(NCBEboolean[1]):
                Comment = secondInput.commentExtract()
                self.Comments = self.__commentExtract(Comment,0)
            if(NCBEboolean[2]):
                self.Edges = secondInput.edgesExtract()
            if(NCBEboolean[3]):
                Branch = secondInput.branchExtract()
                self.Branches = self.__branchNodeExtract(Branch)
            
            ##self.Node = secondInput.nodesExtract()
            ##self.Branch = secondInput.comment
           
        elif(isinstance(secondInput,CellCointainer)):
            Name = secondInput.Names
            self.Names = self.__getNameOfCells(Name, Cellnames)
            #minmax = secondInput.MinMax
            #self.MinMax = self.__minmaxExtract(minmax)
            self.Parameter = secondInput.Parameter
            if(NCBEboolean[0]):
                Nodes = secondInput.Names
                self.Nodes = self.__cellExtract(Nodes)
            if(NCBEboolean[1]):
                Comment = secondInput.__allCommentComnined()
                self.Comments = self.__commentExtract(Comment,3)
            if(NCBEboolean[2]):
                raise Exception('not yet implemented')
                self.Edges = secondInput.Edges
            if(NCBEboolean[3]):
                raise Exception('not yet implemented' )
        else:
            raise Exception('no inputbro')
   
    def __minmaxExtract(self, minmax):
        newMinMax = {}
        for elem in self.Names:
            newMinMax.setdefault(elem)
            newMinMax[elem] = minmax[elem]
        return newMinMax

    
    
    
    def __cellExtract(self, Nodes):
        newNodes = {}
        for elem in self.Names:
            newNodes.setdefault(elem)
            newNodes[elem] = Nodes[elem]
        return newNodes
    
    def __getNameOfCells(self,Cellnames, KeyTerm):
        if (KeyTerm == None):
            return Cellnames
        else:
            newCellNames = []
            for cellName in Cellnames:
                if cellName.find(KeyTerm) != -1:
                    newCellNames.append(cellName)
            if (len(newCellNames)== 0):
                raise Exception('there is no cell with the name of ' + KeyTerm)
            return newCellNames

    
    #def __privAllNodesExtract(self):
    #    allNodes = []
    #    for nodes in self.Nodes.values():
    #        allNodes = allNodes + nodes
    #    return allNodes        
           
    def __commentExtract(self, Comment, indexnumber):
        #NodeSet = set(x[3] for x in self.__privAllNodesExtract())
        #print Comment
        CommentSet = set(x[indexnumber] for x in Comment)
        comment = {}
        #print CommentSet
        for key in self.Nodes:
            comment.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivCellNodSet = set(x[3] for x in indivCellNode)
            intersection = indivCellNodSet & CommentSet
            #intersection_list = [item for item in indivCellNode if item[3] in intersection]
            #print intersection_list
            int_list = []
            for item in indivCellNode:
                if item[3] in intersection:
                    temp = item
                    for commenta in Comment:
                        if commenta[0] == item[3]:
                            temp.append(commenta[1])
                            break;
                    int_list.append(temp)
            #int_list.sort(key = lambda x:x[3])
            comment[key] = int_list
        return comment
    
    def __branchNodeExtract(self, Branches):
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            
            indivEdge = set(Branches)
            EdgeNode[key] = [item for item in indivCellNode if item[3] in indivEdge]
       
        return EdgeNode
    
    def __edgeNodeExtract(self):
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivEdge = self.Edges[key]
            indEdSource = set(x[1] for x in indivEdge)
            EdgeNode[key] = [item for item in indivCellNode if item[3] in indEdSource]
       
        return EdgeNode
    def __allCommentComnined(self):
        allComments = []
        for comments in self.Comments.values():
            allComments = allComments + comments
        return allComments
    """
    return edges in dictionary form
    { cell: [z y x id cellName]}
    id is the source only! 
    """
    def sortEdgeExtract(self):
        Keys = self.Nodes.keys()
        EdgeNode = {}
        for key in Keys:
            EdgeNode.setdefault(key)
            indivCellNode = self.Nodes[key]
            indivEdge = self.Edges[key]
            indEdSource = set(x[1] for x in indivEdge)
            EdgeNode[key] = [item for item in indivEdge if item[0] in indEdSource]
       
        return EdgeNode
    """
    return nodes in list form
    you have freedome to sort this however you want. 0 -z 1- y 2-x 
    {[z y x id cellName]}
    """
    def allNodesExtract(self, sortIndex):
        allNodes = []
        for nodes in self.Nodes.values():
            allNodes = allNodes + nodes
        allNodes.sort(key = lambda x:x[sortIndex])
        return allNodes
    """
    return edges in list form
    you have freedome to sort this however you want. 0 -z 1- y 2-x 
    {[z y x id cellName]}
     id is the source only! 
    """
    def allEdgesExtract(self,sortIndex):
        EdgeNode = self.__edgeNodeExtract()      
        allEdges = []
        for edges in EdgeNode.values():
            allEdges = allEdges + edges
        allEdges.sort(key = lambda x:x[sortIndex]) 
            
        return allEdges
    """
    return nodes without comments in dictionary form
     You should use this with commentWithKeywordExtract 
    {[z y x id cellName]} 
    """
    def allNodesNotCommentedExtract(self, Comment):
        AllNodes = self.Nodes
        #Comment = self.__allCommentComnined()
        CommentSet = set(x[3] for x in Comment)
        UncommentedNodes = {}
        for key in AllNodes:
            UncommentedNodes.setdefault(key)
            indivCellNode = AllNodes[key]
            indivCellNodSet = set(x[3] for x in indivCellNode)
            indivCellNodSet.difference_update(CommentSet)
            UncommentedNodes[key] = [item for item in indivCellNode if item[3] in indivCellNodSet]
        return UncommentedNodes
    """
    return nodes with specific comments in list form
     You can use comment
    {[z y x id cellName comment]} 
    """
    
    def commentWithKeywordExtract(self,*args):
        Comments = self.__allCommentComnined()
        newComments = []
        for comment in Comments:
            for keyword in args:
                if comment[5].find(keyword) != -1:
                    newComments.append(comment)
                    break
        return newComments
    #def __findWantedComment(self, Comments, index, *inputs):
    #    newComment = []
    #    for comment in Comments:
    #        if self.__commentInputCompare(input, *inputs):
                
            
    #def __commentInputCompare(self, cellComment, *inputs):
    #    for input in inputs:
    #        if cellComment.find(input) != -1:
    #            return True
    #    return False
          
        
