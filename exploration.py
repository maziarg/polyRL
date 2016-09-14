'''
Created on Sep 7, 2016

@author: mgomrokchi
'''
from envParams import envParams
import numpy as np

class polyExplorer(object):
    '''
    2D exploration policy based on persistence length idea
    In this implementation we construct the chain over time-steps 
    The aim is to compute the maximum number of states visited given a fixed persistence length  
    N=Number of steps of fixed size (stepSize) 
    N_s=Total number of distinct steps visited 
    Assumption: For the simplicity of our implememntaion we are assuming theta to be fixed but in the later experiments we have to 
    use the fact that E[(stepSize)^2*cos(theta)]=e^(-1/p) in order to sample a theta ~ N(cos^(-1)(e^(-1/p)),var^2)
    Assumption: We are using normal-tangent coordinate system 
    Assumption: The randomness used in this implementation is following python randomeness which
    might not be uniform
    '''
    def __init__(self, numberOfsteps, stepSize, persistenceLength):
        self.numberOfsteps= numberOfsteps
        self.stepSize= stepSize
        self.persistenceLength= persistenceLength
        self.envparams = envParams()
        self.postion_0 = self.drawInitState()
        self.theta_0=self.computeTheta_0()
        self.theta_base = self.setBaseTheta(self.theta_0)
        self.theta= self.computeTheta()
            
    def setBaseTheta(self,theta_base):
        self.theta_base=theta_base

    def drawInitState(self):
        x=np.random.randint(self.envparams.stateSpaceRage[0][0],self.envparams.stateSpaceRage[0][1])
        y=np.random.randint(self.envparams.stateSpaceRage[1][0],self.envparams.stateSpaceRage[1][1])
        return [x,y]
    
        
    def xIsInRange(self,x):
        if x<0 or x>10: 
            return False
            
    def yIsInRange(self,y):
        if y<0 or y>10:
            return False
             
    def computeTheta_0(self):
        return np.random.uniform(self.envparams.angelRange[0],self.envparams.angelRange[1])
        
    def computeDirectionalAngle(self):
        HT=np.random.randint(0,2)
        if HT==0:
            self.setBaseTheta(self.theta_base-self.theta)
        else:
            self.setBaseTheta(self.theta_base+self.theta)
                
    def reflect(self,x,y):
        #Mirror-like deflection 
        return [x,y]
    def deflect(self,currentPosition, x, y, xflag,yflag):
        if xflag==1:
            if x>self.envparams.stateSpaceRage[0][1]:
                x= self.envparams.stateSpaceRage[0][1]
            else:
                x= self.envparams.stateSpaceRage[0][0]
            y=np.math.sqrt(np.math.pow(self.stepSize,2) - np.math.pow(np.abs(x-currentPosition[0]),2))
            
        if yflag==1:
            if x>self.envparams.stateSpaceRage[1][1]:
                x= self.envparams.stateSpaceRage[1][1]
            else:
                x= self.envparams.stateSpaceRage[1][0] 
    
    def move(self,currentPosition):
        x= currentPosition[0]+self.stepSize*np.math.cos(self.theta_base)
        y= currentPosition[1]+self.stepSize*np.math.sin(self.theta_base)
        while not self.xIsInRange(x) or not self.yIsInRange(y):
            if not self.xIsInRange(x):
                if not self.yIsInRange(y):
                    [x,y]=self.reflect(x, y)
                    #Adjust both x and y based on the minimum deviation of thata with respect to the closes walls
                    #and reflect
                else:
                    #Adjust x to 10 or 0 and y with respect to the stepSize
                    xflag = 1
                    yflag = 0
                    [x,y]=self.deflect(currentPosition, x, y, xflag, yflag)


            if not self.yIsInRange(y):
                if not self.xIsInRange(x):
                    #Adjust both x and y
                    [x,y]=self.reflect(x, y)
                else:
                    #Adjust y to 10 or 0 and x with respect to the stepSize
                    yflag = 1
                    xflag = 0
                    [x,y]=self.deflect(currentPosition, x, y, xflag, yflag)

        if self.xAndyAreExceptional(x, y):
            return self.refelect(x,y)
            
        return [x,y]