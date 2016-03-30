#!/usr/bin/python

##imports math and XPath tools
from DistanceCalculator import Dist
from math import fabs
from pprint import pprint
import lxml.etree as ET
from lxml.builder import E
from lxml.builder import ElementMaker
from copy import deepcopy
from copy import copy
import csv

"""
PURPOSE: This reads a Knossos XML file, finds potential points of contact between skeletons,
and writes those points as unlinked nodes in a new skeleton file.
"""

"""
#creates a file to which output can be written 
c = csv.writer(open("coordinates_new.csv", "wb"))
headerArray = ["Cell 1","Cell 2","Mid X","Mid Y","Mid Z"]
c.writerow(headerArray) #writes first row header to the csv file

#would write to a csv file 
c.writerow(temp_dist[1]) 

#would print the output XML file
newfile = (ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
print newfile
"""

"""
FIRST: a XML file holding the skeletons to be analysed is loaded and parsed
"""
					
#prompts for file and threshold
file = 'annotation.xml' #raw_input("File to open: ")
threshold = 1500 #int(raw_input("Detection threshold (nm): "))

#imports a merged tree and maps children
tree = ET.parse(file)
things = tree.getroot()
children = things.getchildren()

#creates an array containing x, y, z scaling
for elem in things.iterfind('parameters/scale'):
	xscale = float(elem.get('x'))
	yscale = float(elem.get('y'))
	zscale = float(elem.get('z'))
	scaling = [xscale,yscale,zscale]


"""
NEXT: the string variables for node ids, etc... in a new XML file are defined
"""
#thing attributes
id_t="1" 
rgb_t="-1." 
a_t="1." 
comment_t="PutativeContact"
#node attributes
id_n = "1"
rad_n = "1.5"
x_n = "1"
y_n = "1"
z_n = "1"
inVp_n = "1"
inMag_n = "1"
time_n = "0"
#edge attributes
source = "1"
target = "2"
#comment attributes
node_comment = "1"
content_comment = "putative"

"""
NEXT: a new XML file is laid out to hold the contacts found
NOTE: as of July 30, 2015, the new XML file must be modified in two ways:
1) a duplicate <parameters/> must be removed
2) in <thing/>, the "color" keys must be modified, e.g., "colorr" changed to "color.r"
"""

#sets up a new XML file to hold the contacts
root=ET.Element("things")
parameters=ET.SubElement(root, "parameters") 
#root.append(copy(things[0]))
thing=ET.SubElement(root, "thing", id='%s' %id_t, colorr='%s' %rgb_t, colorg='%s' %rgb_t, colorb='%s' %rgb_t, colora='%s' %a_t, comment='%s' %comment_t)
comments=ET.SubElement(root, "comments")
nodes=ET.SubElement(thing, "nodes")
edges=ET.SubElement(thing, "edges")
#edge=ET.SubElement(edges, "edge", source='%s' %source, target='%s' %target)

#maps the things (parameters, cell skeletons, comments)
i=0
for child in children: 
	temp_voxel_1=[]
	#gets the comment of each child
	attributes_1 = child.attrib
	temp_1 = attributes_1.get('comment')
	#if the comment is of type CB
	if (temp_1 != None) and ("CB" in temp_1): #LOOK AT CBa FOR TROUBLESHOOTING
		tempchild_1 = child
		for elem in tempchild_1.iterfind('edges/edge'): #look only at linked nodes
			val = int(elem.get('target')) #returns the first linked node
			for elem in tempchild_1.iterfind("nodes/node[@id='%d']" % val): #searches for the node id 	
			#returns voxel coordinates of node
				x = int(elem.get('x'))
				y = int(elem.get('y'))
				z = int(elem.get('z'))
				temp_voxel_1 = [temp_1,val,x,y,z]
				for child in children:
					temp_voxel_2=[]
					#gets the comments of each child	
					attributes_2 = child.attrib
					temp_2 = attributes_2.get('comment')
					#if the comment is of type AII
					if (temp_2 != None) and ("AII" in temp_2):
						tempchild_2 = child	
						for elem in tempchild_2.iterfind('edges/edge'): #look only at linked nodes
							val = int(elem.get('target')) #returns the first linked node
							for elem in tempchild_2.iterfind("nodes/node[@id='%d']" % val): #searches for the node id 	
								#returns voxel coordinates of node
								x = int(elem.get('x'))
								y = int(elem.get('y'))
								z = int(elem.get('z'))
								temp_voxel_2 = [temp_2,val,x,y,z]
								#do_dist = fabs(temp_voxel_2[2]-temp_voxel_1[2])*scaling[0] #if voxel x values are close, find distance between voxels
								if (temp_voxel_1[0] != temp_voxel_2[0]): #double check that the voxels are from different skeletons
									temp_dist = Dist(temp_voxel_1,temp_voxel_2,scaling) 
									if (temp_dist[0] < threshold): #temp_dist[1]=[A[0],B[0],midx,midy,midz]
										#this will be the node id
										i=i+1	
										id_n = str(i)
										#node coordinates
										x_n = str(temp_dist[1][2])
										y_n = str(temp_dist[1][3])
										z_n = str(temp_dist[1][4])
										#make a new node in tree
										node=ET.SubElement(nodes, "node", id='%s' %id_n, radius='%s' %rad_n, x='%s' %x_n, y='%s' %y_n, z='%s' %z_n, inVP='%s' %inVp_n, inMag='%s' %inMag_n, time='%s' %time_n)
										#comment attributes
										node_comment = id_n
										content_comment = (temp_dist[1][0]+" contacts "+temp_dist[1][1]) 
										#make a new comment in tree
										comment=ET.SubElement(comments, "comment", node='%s' %node_comment, content='%s' %content_comment)

#writes the new nodes and comments to a XML file
newfile = 'contact_map_073015.nml'
file = open(newfile, "w")
file.writelines(ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
file.close()

numcells = 0 #counts finds the highest thingid and returns an id for a new thing
for elem in things.iterfind('thing'):
	temp = int(elem.get('id'))
	if temp>numcells:
		numcells=temp
numcells = numcells+1 #cells start with thing 1; thing 0 is parameters

		