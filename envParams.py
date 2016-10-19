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
        self.stateSpaceRange=[[5,505],[5,505]]
        self.angleRange=[0,360]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"   
        self.gridXscale=400
        self.gridYscale=400
        self.gridXLength=500
        self.gridYLength=500
        self.stateFeatureDim=500
        self.actionFeatureDim=350
        self.goalZoneRin=30
        self.goalZoneRout=50
        self.goalReward=100
        self.regularReward=-1
        self.discountFactor=0.99
        