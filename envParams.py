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
        self.angleRange=[0,360]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"   
        self.gridXscale=400
        self.gridYscale=400
#         self.gridXLength=500
#         self.gridYLength=500
        self.stateFeatureDimX=10
        self.stateFeatureDimY=5
        self.stateFeatureDim=self.stateFeatureDimX*self.stateFeatureDimY
        self.actionFeatureDim=10
        self.goalReward=10
        self.regularReward=0
        self.wallReward=-1
        self.discountFactor=0.9
        