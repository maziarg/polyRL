'''
Created on Sep 7, 2016

@author: mgomrokchi
'''

class envParams(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.stateSpaceDim=2
        self.stateSpaceRage=[[0,100],[0,100]]
        self.angelRange=[0,360]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"   
        self.gridXscale=100
        self.gridYscale=100