#!/usr/bin/python

from math import sqrt
from math import pow

def Dist(A,B,scale):
	#x coordinates
	xVal = [A[2],B[2]]
	xVal.sort()
	x_dif1 = (xVal[1]-xVal[0])
	x_dif2 = x_dif1*scale[0]
	#y coordinates
	yVal = [A[3],B[3]]
	yVal.sort()
	y_dif1 = yVal[1]-yVal[0]
	y_dif2 = y_dif1*scale[1]
	#z coordinates
	zVal = [A[4],B[4]]
	zVal.sort()
	z_dif1 = zVal[1]-zVal[0]
	z_dif2 = z_dif1*scale[2]
	#finds the distance
	distance = sqrt((pow(x_dif2,2)+pow(y_dif2,2)+pow(z_dif2,2)))
	#finds the middle points 
	midx = (xVal[0]+(x_dif1/2))
	midy = (yVal[0]+(y_dif1/2))
	midz = (zVal[0]+(z_dif1/2))
	#returns the midpoint voxel, includes cell names
	midpoint = [A[0],B[0],midx,midy,midz]
	return distance, midpoint