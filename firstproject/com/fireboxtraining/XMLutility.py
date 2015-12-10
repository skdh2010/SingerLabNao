'''
Created on 2015. 10. 19.

@author: Nao
'''
"""
XMLutility
    pre: Nodes1 and 2 are sorted by y// Nodes2 can have comment
XMLprinter
    pre: cells= [cell...cell]
    
"""
import lxml.etree as ET
from XMLinterpreter import XMLinterpreter
from com.fireboxtraining.CellsCointainer import CellCointainer
from _bisect import bisect_left
from bisect import bisect_right
import sys
import pprint
sys.setrecursionlimit(150000000)

class XMLutility(object):
    
    """basics"""
    
    """
    Compare Two cells and return mid point
    [z y x newID "cellname1--cellname2"]
    """
    
    @staticmethod
    def compareTwoCellandReturnMidPoint(Nodes1, Nodes2,threshold, i):
        yKey = [item[1] for item in Nodes2]
        newNodes = []
        for item in Nodes1:
            left=bisect_left(yKey,item[1]-threshold)
            right=bisect_right(yKey,item[1]+threshold)
            ySatisList = Nodes2[left: right+1];
            for node in ySatisList:
                if node[2]<(item[2]+threshold) and node[2]>(item[2]-threshold) and node[0]<(item[0]+threshold) and node[0]>(item[0]-threshold):
                    z= int((node[0]+item[0])/52)
                    y= int((node[1]+item[1])/26.4)
                    x= int((node[2]+item[2])/26.4)
                    ide= i
                    cellname = item[4]+"--"+node[4]
                    newnode = []
                    newnode.append(z)
                    newnode.append(y)
                    newnode.append(x)
                    newnode.append(ide)
                    newnode.append(cellname)
            
                    
                    newNodes.append(newnode)
                    i = i+1
        return newNodes
    
    """
    return names of cells in a tree in list form
    [names]
    """
    @staticmethod
    def findCellnames(Nodes):
        CellnameSet= set(x[4] for x in Nodes)
        myList = list(CellnameSet)
        return myList;
    """
    return list form of nodes to dictionary form of nodes
    {cell: [z y x id cellname etc]
    """
    @staticmethod
    def sortNodes(Nodes):
        dict = {}
        for cellname in XMLutility.findCellnames(Nodes):
            dict.setdefault(cellname)
            dict[cellname] = []
        for item in Nodes:
            dict[item[4]].append(item)
        
        return dict
    """comment vs comment """
    #################CommentVSComment################
    """
    Compare Two cells and return mid point
    [z y x idOFtheFirst cellnameOFtheFirst cellnameOFtheSecond]
    """    
    
    @staticmethod
    def compareTwoCellForFirst(scale, Nodes1, Nodes2,threshold, i):
        yKey = [item[1] for item in Nodes2]
        newNodes = []
        for item in Nodes1:
            left=bisect_left(yKey,item[1]-threshold)
            right=bisect_right(yKey,item[1]+threshold)
            ySatisList = Nodes2[left: right+1];
            for node in ySatisList:
                if node[2]<(item[2]+threshold) and node[2]>(item[2]-threshold) and node[0]<(item[0]+threshold) and node[0]>(item[0]-threshold):
                    z= int((item[0])/scale[0])
                    y= int((item[1])/scale[1])
                    x= int((item[2])/scale[2])
                    ide= int(item[3])
                    cellname = item[4]
                    newnode = []
                    newnode.append(z)
                    newnode.append(y)
                    newnode.append(x)
                    newnode.append(ide)
                    newnode.append(cellname)
                    newnode.append(node[4])
            
                    
                    newNodes.append(newnode)

                    
        return newNodes
        #return XMLutility.killDuplication(newNodes)
    """
    kill nodes with duplicated index in a list form
    [z y x id cellname etc]
    """
    @staticmethod
    def killDuplication(Nodes1):
        s = set()
        returner = []
        seta = set(item[3] for item in Nodes1)
        for item in Nodes1:
            if item[3] not in s:
                s.add(item[3])
                returner.append(item)
        return returner
    @staticmethod
    def findCellnames1(Nodes):
        CellnameSet= set(x[5] for x in Nodes)
        myList = list(CellnameSet)
        return myList;
    @staticmethod
    def sortNodes1(Nodes):
        dict = {}
        for cellname in XMLutility.findCellnames1(Nodes):
            dict.setdefault(cellname)
            dict[cellname] = []
        for item in Nodes:
            dict[item[5]].append(item)
        
        return dict
    
    
    @staticmethod
    def DLtoDDtoDCL(Dic, threshold):
        Dic1 = XMLutility.sortNodes(Dic)
        keys= Dic1.keys()
        for item in keys:
            lista = Dic1[item]
            Dic1[item] = XMLutility.sortNodes1(lista)
            #Dic1[item] = XMLutility.dictToCluster(Dic1[item], threshold)
        return Dic1
    @staticmethod
    def DicToList(dic):
        returner = []
        keys = dic.keys()
        for item in keys:
            returner = returner + dic[item]
        return returner
    @staticmethod
    def TempCvsCprinter(OriginalDict, DicDic, outputname, key1):
        f = open(outputname, 'w')
            
        keys1 = DicDic.keys()
        tanzania = keys1[0][:3]
        i = len(keys1)
        j = 0
        k = 0
        for item in keys1:
            Dic2 = DicDic[item]
            #f.write( item + " has "+ str(len(XMLutility.DicToList(Dic2))) +" " + key1 +"\n")
            f.write( item + " has "+ str(len(OriginalDict[item])) +" " + key1 +"\n")
            Keys2 = Dic2.keys()
            arabia = Keys2[0][:3] # might yield error empty
            f.write( "it contacts " + str(len(Keys2)) + " " + arabia +"\n" )
            f.write("")
            j= j + len(Keys2)
            for item2 in Keys2:
                f.write( item + " to " + item2 + " has " + str(len(Dic2[item2])) + " " + key1 +"\n" )
                k = k + len(Dic2[item2])
            f.write( "\n\n" )   
                
                
        f.write("On average, 1 " + tanzania + " contacts " + str(j/i) + " with " + str(k/i) + " " + str(key1) + "\n")
        f.close()
    #############################################
    @staticmethod
    def XMLTempPrinter(Parameter, dict, filename):
        root = ET.Element("things")
        root.append(Parameter)
        rgb_t="-1." 
        a_t="1." 
        NodeName = dict.keys()
        ij = 1
        nodeide = 1
        for item in NodeName:
            thing=ET.SubElement(root, "thing", id=str(ij), colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment=item)
            node1 = ET.SubElement(thing, "nodes")
            nodes = dict[item]
            ij = ij+1
            for item1 in nodes:
                
                a = str(item1[0])
                b = str(item1[1])
                c = str(item1[2])
                d = str(nodeide)
                e = item1[4]
                nodeide = nodeide +1
                node=ET.SubElement(node1, "node", id= d, radius="1.5", x=c, y=b, z=a, inVP="1", inMag="1", time="0")    
                
        print("done")
        newfile = filename
        pile = open(newfile, "w")
        pile.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        pile.close()   
 
    @staticmethod
    def XMLTempPrinter1(Parameter, dict, filename):
        root = ET.Element("things")
        root.append(Parameter)
        rgb_t="-1." 
        a_t="1." 
        NodeName = dict.keys()
        ij = 1
        nodeide = 1
        for item in NodeName:
            thing=ET.SubElement(root, "thing", id=str(ij), colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment=item)
            node1 = ET.SubElement(thing, "nodes")
            nodes = dict[item]
            ij = ij+1
            for item1 in nodes:
                
                a = str(item1[0])
                b = str(item1[1])
                c = str(item1[2])
                d = str(nodeide)
                e = item1[4]
                nodeide = nodeide +1
                node=ET.SubElement(node1, "node", id= d, radius="10", x=c, y=b, z=a, inVP="1", inMag="1", time="0")    
                
        print("done")
        newfile = filename
        pile = open(newfile, "w")
        pile.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        pile.close()    
 
    """ Separator Printer  """
    @staticmethod
    def separtor(Cellcoin, cellname):
        node = Cellcoin.Nodes[cellname]
        edge = Cellcoin.Edges[cellname]
        comment = Cellcoin.Comments[cellname]
        branch = Cellcoin.Branches[cellname]
        Parameter = Cellcoin.Parameter
        
        root = ET.Element("things")
        root.append(Parameter)
        rgb_t="-1." 
        a_t="1." 
        ij = 1
        nodeide = 1
        thing=ET.SubElement(root, "thing", id=str(ij), colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment=cellname)
        node1 = ET.SubElement(thing, "nodes")
        ij = ij+1
        for item1 in node:
                
            a = str(int(item1[0]/26))
            b = str(int(item1[1]/13.2))
            c = str(int(item1[2]/13.2))
            d = str(item1[3])
            e = item1[4]
            nodeide = nodeide +1
            node=ET.SubElement(node1, "node", id= d, radius="10", x=c, y=b, z=a, inVP="1", inMag="1", time="0")    
        edge1 = ET.SubElement(thing, "edges")
        for item2 in edge:
            a = str(item2[0])
            b = str(item2[1])
            
            node=ET.SubElement(edge1, "edge", target = a, source = b )
            
        comment1 =ET.SubElement(root, "comments")
        for item3 in comment:
            a = str(item3[3])
            b = str(item3[4])
            node=ET.SubElement(comment1, "comment", node = a, content = b )
        
        branch1 =ET.SubElement(root, "branchpoints")
        for item3 in branch:
            a = str(item3[3])
            node=ET.SubElement(comment1, "branchpoint", id = a)
        
        print("done")
        newfile = cellname
        pile = open(newfile, "w")
        pile.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        pile.close()    
        
        
    @staticmethod
    def MultiSeparator(CellCoin):
        hello = CellCoin.Name
        for item in hello:
            XMLutility.separtor(CellCoin, item) 
    
       
        
    """CLUSTER ANALYSIS"""      
    @staticmethod  
    def distanceCal( list1, list2,threshold):
        if (list2[0]-threshold<list1[0]) and (list1[0] < list2[0]+threshold)  and (list2[1]-threshold<list1[1]) and (list1[1] < list2[1]+threshold) and (list2[2]-threshold<list1[2]) and (list1[2] < list2[2]+threshold):
            return True
        else:
            return False
    @staticmethod
    def ClusterFinder_Aux(OriginalList, OneCluster, threshold, switch):
        if len(OriginalList)==0 or switch == 0:
            print "boithc"
            return (OriginalList, OneCluster)
        elif len(OneCluster) == 0:
            OneCluster.append(OriginalList[0])
            del OriginalList[0]
            return XMLutility.ClusterFinder_Aux(OriginalList, OneCluster,  threshold, 1)
        else:
            change = 0
            temp = []
            old = list(OneCluster)
            LeftOver= []
            for item2 in OriginalList:
                for item1 in OneCluster:
                    if XMLutility.distanceCal(item1, item2, threshold):
                        temp.append(item2)
                        change = change +1 
                        break;
                    else:
                        LeftOver.append(item2)
                
            NodeNumber= set(x[3] for x in temp)
            
            leftoverNodenumber = set(x[3] for x in LeftOver)
            NewList = [item for item in OriginalList if item[3] in NodeNumber] + old
            
            NewLeftOver = [item for item in OriginalList if item[3] in leftoverNodenumber]
        #### works but NEED TO MODIFY IT ! 
        
            return XMLutility.ClusterFinder_Aux(NewLeftOver, NewList, threshold, change)
            
        
        
        
        
    @staticmethod
    def ClusterFinder_Aux2(OriginalList, Clusters, threshold):
        if len(OriginalList)==0:
            return Clusters
        else:
    
            OneCluster = []
            temp = XMLutility.ClusterFinder_Aux(OriginalList, OneCluster, threshold, 1)
            Clusters.append(temp[1])
            return XMLutility.ClusterFinder_Aux2(temp[0], Clusters, threshold)
    @staticmethod
    def Average( Nodes):
        x= 0
        y= 0
        z= 0
        for item in Nodes:
            z = x+ item[0]
            y= y+item[1]
            x= z+item[2]
        length = len(Nodes)
        x = x/length
        y = y/length
        z = z/length
        node = []
        node.append(z)
        node.append(y)
        node.append(x)
        
        return node
        
        
        
    @staticmethod
    def ClusterFinder(OriginalList, threshold):
        Clusters = []
        Nodes = []
        NodeID = 1
        clusters = XMLutility.ClusterFinder_Aux2(OriginalList, Clusters, threshold)
        for item in clusters:
          
            node = XMLutility.Average(item)
            node.append(NodeID)
            cellID = item[0][4]
            node.append(cellID)
            NodeID = NodeID +1
            Nodes.append(node)
        return Nodes
    @staticmethod
    def dictToCluster(OriginalDict, threshold):
        Keys = OriginalDict.keys()
        for item in Keys:
            
            temp = OriginalDict[item]
            result = XMLutility.ClusterFinder(temp, threshold)
            OriginalDict[item] =result
            
        return OriginalDict
    """###############################################
    #############################################
    ########################################"""
    @staticmethod    
    def CompareTwoCellsCommentAndEdgeAndPrint(address1, address2, threshold, outputname, *args):
        preCB = XMLinterpreter(address1)
        preAC = XMLinterpreter(address2)
        condition  = [True, True, True, False]
        CB = CellCointainer(preCB, condition)
        AC = CellCointainer(preAC, condition)
        comments = CB.commentWithKeywordExtract(*args)
        comments.sort(key = lambda x:x[1])
        edges = AC.allEdgesExtract(1)
        
        
        CBAC =XMLutility.compareTwoCellandReturnMidPoint(comments, edges, threshold, 1)
        CBACsorted =XMLutility.sortNodes(CBAC)
        #CBACsorted = XMLutility.dictToCluster(CBACsorted, threshold)
        printCBAC = XMLutility.XMLTempPrinter(CB.Parameter, CBACsorted, outputname)
      




    @staticmethod    
    def CompareTwoCellsNodeAndPrintMidPoint(address1, address2, threshold, outputname):
        preCB = XMLinterpreter(address1)
        preAC = XMLinterpreter(address2)
        condition  = [True, False, False, False]
        CB = CellCointainer(preCB, condition)
        AC = CellCointainer(preAC, condition)
        
        CBAC =XMLutility.compareTwoCellandReturnMidPoint(CB.allNodesExtract(1), AC.allNodesExtract(1), threshold, 1)
        CBACsorted =XMLutility.sortNodes(CBAC)
        CBACsorted = XMLutility.dictToCluster(CBACsorted, 200)
        printCBAC = XMLutility.XMLTempPrinter1(CB.Parameter, CBACsorted, outputname)
    
    @staticmethod    
    def CompareTwoCellsComments(address1,key1,address2,key2,threshold,outputname, outputname2, outputname3):
        preCB = XMLinterpreter(address1)
        preAC = XMLinterpreter(address2)
        condition  = [True, True, False, False]
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
        CBACsorted1 =XMLutility.DLtoDDtoDCL(CBAC,200)
        XMLutility.TempCvsCprinter(comments1a, CBACsorted1, outputname, key1)
        #print CBACsorted
        with open(outputname2, 'wt') as out:
            pprint.pprint(CBACsorted1, stream=out)
        printCBAC = XMLutility.XMLTempPrinter(CB.Parameter, CBACsorted, outputname3)
        #pile.writelines()
        #pile.close()   
    