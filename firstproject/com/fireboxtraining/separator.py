'''
Created on 2015. 9. 11.

@author: Nao
'''

import lxml.etree as ET
from lxml.builder import E
from lxml.builder import ElementMaker

from __builtin__ import str

def countmax(bile,cellname):
    tree = ET.parse(bile)
    things = tree.getroot()
    path = '//thing[@comment =' + '\'' + cellname + '\'' + ']'
    children1 = things.xpath(path)
    i=0
    for child in children1:
        for elem in child.iterfind('nodes/node'):
            x=int(elem.get('id'))
            if x>i :
                i=x
    return i

def countmin(bile,cellname):
    tree = ET.parse(bile)
    things = tree.getroot()
    path = '//thing[@comment =' + '\'' + cellname + '\'' + ']'
    children1 = things.xpath(path)
    i=10000000
    for child in children1:
        for elem in child.iterfind('nodes/node'):
            x=int(elem.get('id'))
            if x < i :
                i=x
    return i

def saveNodes(children):
    savenode = []
    for child in children:
        for elem in child.iterfind('nodes/node'):
            a=str(elem.get('z'))
            b=str(elem.get('y'))
            c=str(elem.get('x'))
            d=str(elem.get('id'))
            e=str(elem.get('time'))
            f=str(elem.get('inMag'))
            g=str(elem.get('inVp'))
            h=str(elem.get('radius'))
            numba = [a,b,c,d,e,f,g,h]
            savenode.append(numba)     
    return savenode

def saveBranch(bile, mini, maxi):
    tree = ET.parse(bile)
    things = tree.getroot()
    children = things.getchildren()
    savenode = []
    for child in children:
        for elem in child.iterfind('branchpoint'):
            aa=int(elem.get('id'))
            if aa >= mini and aa <= maxi:
                a=str(aa)
                savenode.append(a) 
    return savenode

def saveComment(bile, mini, maxi):
    tree = ET.parse(bile)
    things = tree.getroot()
    children = things.getchildren()
    savenode = []
    for child in children:
        for elem in child.iterfind('comment'):
            a=str(elem.get('content'))
            ba=int(elem.get('node'))
            if ba >= mini and ba <= maxi:
                b = str(ba)
                numba = [a,b]
                savenode.append(numba)


    return savenode
def saveEdge(children):
    savenode = []
    for child in children:
        for elem in child.iterfind('edges/edge'):
            d=str(elem.get('target')) 
            e=str(elem.get('source'))
            numba = [d,e]
            savenode.append(numba)
   
    return savenode





def separator(files, cellname):
    tree = ET.parse(files)
    things = tree.getroot()
    path = '//thing[@comment =' + '\'' + cellname + '\'' + ']'
    children1 = things.xpath(path)
    children = children1[0]
    maxi = countmax(files, cellname)
    mini = countmin(files, cellname)
    #nodes = saveNodes(children)
    branch = saveBranch(files, mini, maxi)
    comment = saveComment(files, mini, maxi)
    #edge = saveEdge(children)
    print maxi
    print mini
    print branch
    print comment
    
    root1 =ET.Element("things")
    Parameter = tree.find("parameters")
    root1.append(Parameter)
    root1.append(children)
    #newfile1 = "useless.xml"
    #pile = open(newfile1, "w")
    #pile.writelines(ET.tostring(root1, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    #pile.close()
    
   
    Comments = ET.SubElement(root1, "comments")
    Branchpoints = ET.SubElement(root1, "branchpoints")
    
    for index1 in range(len(comment)):
        commenti = ET.SubElement(Comments, "comment", content= comment[index1][0], node = comment[index1][1])
    for index2 in range(len(branch)):
        branchpointi = ET.SubElement(Branchpoints, "branchpoint", id = branch[index2])
    
    newfile = 'disjointfile.xml'
    pile = open(newfile, "w")
    pile.writelines(ET.tostring(root1, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    pile.close()
    
    

separator('d:/annotation.xml','OFF_CBa')

