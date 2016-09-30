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
        self.stateSpaceRange=[[5,405],[5,405]]
        self.angleRange=[0,359.99]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"   
        self.gridXscale=400
        self.gridYscale=400