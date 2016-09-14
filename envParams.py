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
        self.angelRange=[-180,180]
        self.initStateDist="uniform"  
        self.initThetaDist = "uniform"    