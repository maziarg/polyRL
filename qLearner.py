'''
Created on Oct 17, 2016

@author: Maziar Gomorkchi and Susan Amin
'''
import random
import numpy as np
import math
from envParams import envParams
from ExplorationPolicy import polyExplorer 

class QLearner(object):
    '''
    This is the function approximation implementation of QLearning algorithm
    '''


    def __init__(self, learningRate, epsilon):
        #Should initialize the weight vector
        self.weightVectorDim=envParams.stateFeatureDim+envParams.actionFeatureDim
        self.weightVector=np.zeros(self.weightVectorDim)
        self.epsilon= epsilon
        self.numberOfMoves=20000
        self.stepSize=1
        self.persistenceLength=200
        self.polyexp= polyExplorer(self.numberOfMoves, self.stepSize, self.persistenceLength)
        
    def phi(self, state, action) :
        weightVec=np.zeros(envParams.stateFeatureDim+envParams.actionFeatureDim)
        actionWidth=math.floor(((envParams.angleRange[1]-envParams.angleRange[0])/envParams.actionFeatureDim))
        actionRegion= math.floor(action*actionWidth/(envParams.angleRange[1]-envParams.angleRange[0]))
        weightVec[actionRegion+envParams.stateFeatureDim-1]=1
        gridDiag= math.floor((envParams.gridXscale**2+envParams.gridYscale**2)**0.5)
        x=int(state[0])
        y=int(state[1])
        stateWidth = math.floor(gridDiag/envParams.stateFeatureDim)
        stateRegion= math.floor(((x**2+y**2)**0.5)/stateWidth)
        weightVec[stateRegion]=1
        
        #returns a vector in self.weightVector Dim
           
    
    def getQValue(self, state , action):
        return np.dot(self.weightVector,self.Phi(state,action))  
    
    def getValue(self, state):
        sampledActionSet= self.sampelActionSet()
        maxTemp= envParams.regularReward
        for action in sampledActionSet:
            if self.getQValue(state, action)>maxTemp:
                maxTemp=self.getQValue(state, action)
            else:
                continue
        return maxTemp
    
    def getPolicy(self, state):
        sampledActionSet= self.sampelActionSet()
        action= self.polyexp.theta_base
        maxTemp=self.getQValue(state, action)
        for act in sampledActionSet:
            if self.getQValue(state, act)>maxTemp:
                maxTemp=self.getQValue(state, act)
                action=act
            else:
                continue
        return action
        
    def decision(self):
        if np.random.rand()<=self.epsilon:
            return 0
        else:
            return 1
    
    def getAction(self,state):
        
        if self.decision()==0:
            #Exploration only
            action= self.polyexp.theta_base
        else:
            action= self.getPolicy(state)
        return action
    
    def update(self, state, action, nextState, reward):
        qError= reward + envParams.discountFactor*self.getValue(nextState)-self.getQValue(state, action)
        self.weightVector=self.weightVector+ envParams.learningRate*qError*self.phi(state,action)
        return self.weightVector
    
            
                      
        
        
        
        