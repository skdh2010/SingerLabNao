'''
Created on 2016. 5. 23.

@author: Nao
'''
import numpy as np
from numpy import linalg as LA
import math



class Covariance(object):

    '''
    find 2D confidence ellipse

    input: [[z y ....]]
    output [ycor zcor Principle1 Principle2 Angle ]
    
    Angle to the first principle// radian
    '''
    @staticmethod
    def toEllipse(nodes):
        y_avg = 0.0
        z_avg = 0.0
        
        for item in nodes:
            z_avg = z_avg + item[0]
            y_avg = y_avg + item[1]
        
            
        
        y_avg = y_avg/len(nodes)
        z_avg = z_avg/len(nodes)
        
        newList = []
        
        for item1 in nodes:
            newNode = []
            newNode.append(item1[0] - z_avg)
            newNode.append(item1[1] - y_avg)
            
            newList.append(newNode)
        
        Cyy = 0.0
        Czz = 0.0
        Cyz = 0.0
        
        for item2 in newList:
            Cyy = Cyy + item2[1] * item2[1]
            Czz = Czz + item2[0] * item2[0]
            Cyz = Cyz + item2[1] * item2[0]
        
        covList = []
        tempCov1 = []
        tempCov2 = []
        
        tempCov1.append(Cyy)
        tempCov1.append(Cyz)
        tempCov2.append(Cyz)
        tempCov2.append(Czz)
        
        covList.append(tempCov1)
        covList.append(tempCov2)
        
        CovMatrix = np.array(covList)
        
        eigVal, eigVec = LA.eig(CovMatrix)
        
        EigenValues = eigVal.tolist()
        
        '''
        first eigenVec
        '''
        tempFirstEigen = eigVec[:,0]
        firstEigen = tempFirstEigen.tolist()
        #print firstEigen
        TanAngle = firstEigen[1]/firstEigen[0] #y/z
        Angle = math.atan(TanAngle)
        
        returner = []
        returner.append(y_avg)
        returner.append(z_avg)
        returner.append(math.sqrt(EigenValues[0]/len(nodes)))
        returner.append(math.sqrt(EigenValues[1]/len(nodes)))
        returner.append(Angle)
        
        return returner
        
        
        
     
            
