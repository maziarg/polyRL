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


    def __init__(self, learningRate, epsilon, actionSamplingDensity, polyExplorar):
        #Should initialize the weight vector
        self.envparams = envParams()
        self.weightVectorDim=self.envparams.stateFeatureDim+self.envparams.actionFeatureDim
        self.weightVector=np.zeros(self.weightVectorDim)
        self.epsilon= epsilon
        self.numberOfMoves=20000
        self.stepSize=1
        self.persistenceLength=200
        self.polyexp= polyExplorar
        self.LearningRate= learningRate
        self.actionSamplingDensity= actionSamplingDensity
        self.exploitFlag=0
        self.weightHeatMap=np.zeros((self.envparams.stateSpaceRange[0][1]-self.envparams.stateSpaceRange[0][0],self.envparams.stateSpaceRange[1][1]-self.envparams.stateSpaceRange[1][0]))

            
        
    def setEpsilon(self, epsilon):
        self.epsilon=epsilon
        
    def phi(self, state, action) :
        phiVec=np.zeros(self.envparams.stateFeatureDim+self.envparams.actionFeatureDim)
        #actionWidth=math.floor(((self.envparams.angleRange[1]-self.envparams.angleRange[0])/self.envparams.actionFeatureDim))
        actionRegion= math.floor(action*self.envparams.actionFeatureDim/(self.envparams.angleRange[1]-self.envparams.angleRange[0]))
        phiVec[actionRegion+self.envparams.stateFeatureDim-1]=1
        gridDiag= math.floor((self.envparams.gridXLength**2+self.envparams.gridXLength**2)**0.5)
        x=int(state[0])
        y=int(state[1])
        stateWidth = math.floor(gridDiag/self.envparams.stateFeatureDim)
        stateRegion= math.floor(((x**2+y**2)**0.5)/stateWidth)
        phiVec[stateRegion-1]=1
        return phiVec
        #returns a vector in self.weightVector Dim
           
    
    def getQValue(self, state , action):
        return np.dot(self.weightVector,self.phi(state,action))  
    
    def sampleActionSet(self,state):
        wallIndicator=self.polyexp.isOnWall(state)
        if not wallIndicator:
            lower=self.envparams.angleRange[0]
            upper=self.envparams.angleRange[1]
        elif state[0]==self.envparams.stateSpaceRange[0][0]:
            if state[1]==self.envparams.stateSpaceRange[1][0]:
                lower=0
                upper=90
            elif state[1]==self.envparams.stateSpaceRange[1][1]:
                lower=-90
                upper=0
            else:
                lower=-90
                upper=90
        elif state[0]==self.envparams.stateSpaceRange[0][1]:
            if state[1]==self.envparams.stateSpaceRange[1][0]:
                lower=90
                upper=180
            elif state[1]==self.envparams.stateSpaceRange[1][1]:
                lower=180
                upper=270
            else:
                lower=90
                upper=270
        elif state[1]==self.envparams.stateSpaceRange[1][0]:
                lower=0
                upper=180
        elif state[1]==self.envparams.stateSpaceRange[1][1]:
                lower=180
                upper=360
        step = math.floor((upper-lower)/self.actionSamplingDensity)
        sampledActionSet=[]
        for i in range(self.actionSamplingDensity):
            temp=random.choice(range(lower+(i)*step, lower+(i+1)*step))
            if temp in sampledActionSet:
                i-=1
                continue
            else:
                sampledActionSet.append(temp)
        return sampledActionSet
        
    
    def getValue(self, state):
        sampledActionSet =self.sampleActionSet(state)
        maxTemp= self.envparams.regularReward
        for action in sampledActionSet:
            if self.getQValue(state, action)>maxTemp:
                maxTemp=self.getQValue(state, action)
            else:
                continue
        return maxTemp
    
    def getPolicy(self, state):
        sampledActionSet= self.sampleActionSet(state)
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
        radious= math.floor(((int(state[0])**2+int(state[1])**2)**0.5).real)
        
        if radious>=self.envparams.goalZoneRin and radious<=self.envparams.goalZoneRout:
            return True
        else:
            return False
    
    def getReward(self, state):
        if self.isInGoalZone(state):
            return self.envparams.goalReward
        else:
            return self.envparams.regularReward
    def decision(self):
        self.exploitFlag=0
        if random.uniform(0, 1)<=self.epsilon:
            return 0 #Explore
        else:
            return 1  #Exploit
    
    def getAction(self,state):
        
        if self.decision()==0:
            #Exploration only
            action= self.polyexp.theta_base
        else:
            self.exploitFlag=1
            action= self.getPolicy(state)
        return action
    
    def update(self, state, action, nextState, reward):
        qError= reward + self.envparams.discountFactor*self.getValue(nextState)-self.getQValue(state, action)
        self.weightVector=self.weightVector+ self.LearningRate*qError*self.phi(state,action)
        return self.weightVector
    
            
                      
    
        
        
        