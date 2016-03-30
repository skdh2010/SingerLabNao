'''
Created on 2016. 2. 29.

@author: Nao
'''
from __future__ import division
class state:
    def __init__(self, je, me, ge):
        self.j = je
        self.m = me
        self.g = ge
        

l2states = []

l1states = []

m1 = 2.5
while(m1 > -3):
    l2states.append(state(5/2, m1, 6/5))
    m1 = m1 - 1.0


m2 = 1.5
while(m2 > -2):
    l2states.append(state(3/2, m2, 4/5))
    m2 = m2 - 1.0
    
m3 = 1.5
while(m3 > -2):
    l1states.append(state(3/2, m3, 4/3))
    m3 = m3 - 1.0
    
m4 = 0.5
while(m4 > -1):
    l1states.append(state(1/2, m4, 2/3))
    m4 = m4 - 1.0

    
print len(l2states)
print len(l1states)

for elem1 in l1states:
    for elem2 in l2states:
        difm = elem1.m - elem2.m
        difj = elem1.j - elem2.j
        if( ((difm == 0) or (difm == 1) or (difm == -1))
            and  ((difj == 0) or (difj == 1) or (difj == -1))  ):
            
            a = 'l2 j: ' + str(elem2.j) + ' , m: ' + str(elem2.m) + ' , gl: ' + str(elem2.g)
            b = ' |  l1 j: ' + str(elem1.j) + ' , m: ' + str(elem1.m) + ' , gl: ' + str(elem1.g)
            c = elem2.m * elem2.g - elem1.m * elem1.g
            print a + b 
            print ' delta energy: ' + str(c)
        
        
        