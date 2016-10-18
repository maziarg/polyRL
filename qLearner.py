'''
Created on Oct 17, 2016

@author: Maziar Gomorkchi and Susan Amin
'''
import random
import numpy as np
import math
import random
from envParams import envParams
from ExplorationPolicy import polyExplorer 

class QLearner(object):
    '''
    This is the function approximation implementation of QLearning algorithm
    '''


    def __init__(self, learningRate, epsilon, actionSampleingDensity, polyExplorar):
        #Should initialize the weight vector
        self.envparams = envParams()
        self.weightVectorDim=self.envparams.stateFeatureDim+self.envparams.actionFeatureDim
        self.weightVector=np.zeros(self.weightVectorDim)
        self.epsilon= epsilon
        self.numberOfMoves=20000
        self.stepSize=1
        self.persistenceLength=200
        self.polyexp= polyExplorar
        self.LearnigRate= learningRate
        self.actionSampleingDesnisty= actionSampleingDensity
        
    def setEpsilon(self, epsilon):
        self.epsilon=epsilon
        
    def phi(self, state, action) :
        phiVec=np.zeros(self.envparams.stateFeatureDim+self.envparams.actionFeatureDim)
        #actionWidth=math.floor(((self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.envparams.actionFeatureDim))
        actionRegion= math.floor(action*self.envparams.actionFeatureDim/(self.envparams.angleRange[1]-self.envparams.angleRange[0]))
        phiVec[actionRegion+self.envparams.stateFeatureDim-1]=1
        gridDiag= math.floor((self.envparams.gridXscale**2+self.envparams.gridYscale**2)**0.5)
        x=int(state[0])
        y=int(state[1])
        stateWidth = math.floor(gridDiag/self.envparams.stateFeatureDim)
        stateRegion= math.floor(((x**2+y**2)**0.5)/stateWidth)
        phiVec[stateRegion]=1
        return phiVec
        #returns a vector in self.weightVector Dim
           
    
    def getQValue(self, state , action):
        return np.dot(self.weightVector,self.phi(state,action))  
    
    def sampelActionSet(self):
        step = math.floor((self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.actionSampleingDesnisty)
        sampledActionSet=[]
        for i in range(self.actionSampleingDesnisty):
            temp=random.choice(range(self.envparams.angleRange[0], self.envparams.angleRange[1], step))
            if temp in sampledActionSet:
                i-=1
                continue
            else:
                sampledActionSet.append(temp)
        return sampledActionSet
        
    
    def getValue(self, state):
        sampledActionSet =self.sampelActionSet()
        maxTemp= self.envparams.regularReward
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
    def isInGoalZone(self,state):
        if state[0]<=self.envparams.goalZone[1][0] and state[0]>=self.envparams.goalZone[0][0] and state[1]<=self.envparams.goalZone[1][1] and state[0]>=self.envparams.goalZone[1][0]:
            return True
        else:
            return False
    
    def getReward(self, state):
        if self.isInGoalZone(state):
            return self.envparams.goalReward
        else:
            return self.envparams.regularReward
    def decision(self):
        if random.uniform(0, 1)<=self.epsilon:
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
        qError= reward + self.envparams.discountFactor*self.getValue(nextState)-self.getQValue(state, action)
        self.weightVector=self.weightVector+ self.LearnigRate*qError*self.phi(state,action)
        return self.weightVector
    
            
                      
    
        
        
        