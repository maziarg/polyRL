'''
Created on Sep 7, 2016

@author: mgomrokchi
'''
from envParams import envParams
import numpy as np
import math
import random
from _overlapped import NULL
from cmath import sqrt
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
        self.theta_base = 0
        self.theta= self.computeTheta()
        self.setBaseTheta(self.theta_0)
        self.cornerIndex=0
        
            
    def setBaseTheta(self,theta_base):
        self.theta_base=theta_base

    def drawInitState(self):
        x=random.randint(self.envparams.stateSpaceRage[0][0],self.envparams.stateSpaceRage[0][1])
        y=random.randint(self.envparams.stateSpaceRage[1][0],self.envparams.stateSpaceRage[1][1])
        return [x,y]
    
        
    def xIsInRange(self,x):
        if x<self.envparams.stateSpaceRage[0][0] or x>self.envparams.stateSpaceRage[0][1]: 
            return False
        else:
            return True
            
    def yIsInRange(self,y):
        if y<self.envparams.stateSpaceRage[1][0] or y>self.envparams.stateSpaceRage[1][1]:
            return False
        else: 
            return True
    
    def computeTheta(self):
        exp=(float)(-1/self.persistenceLength)
        return math.degrees(math.acos(math.pow(math.e,exp)/(self.stepSize**2)))
             
    def computeTheta_0(self):
        return random.uniform(self.envparams.angelRange[0],self.envparams.angelRange[1])
        
    def computeDirectionalAngle(self):
        HT=random.randint(0,1)
        if HT==0:
            self.setBaseTheta(((self.theta_base)-self.theta+360)%360)
        else:
            self.setBaseTheta(((self.theta_base)+self.theta)%360)
        return self.theta_base
                
    def findWallIntersection(self, xflag, yflag, currentPosition, nextPosition):
        if (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])>0:
            self.setBaseTheta(90)
        elif (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])<0:
            self.setBaseTheta(270)
        elif ((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])>0) or((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])<0):
            self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+180)
        elif (nextPosition[0]-currentPosition[0])>0 and (nextPosition[1]-currentPosition[1])<0:
            self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+360)
        else:
            self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0]))))
        slope= math.tan(self.theta_base)
        yIntercept= currentPosition[1]- slope*currentPosition[0]
        if xflag==1 and yflag==0:
            if nextPosition[0]<self.envparams.stateSpaceRage[0][0]:
                x=self.envparams.stateSpaceRage[0][0]
            elif nextPosition[0]>self.envparams.stateSpaceRage[0][1]:
                x=self.envparams.stateSpaceRage[0][1]
            return [x, slope*x+yIntercept]
        if yflag==1 and xflag==0:
            if nextPosition[1]<self.envparams.stateSpaceRage[1][0]:
                y=self.envparams.stateSpaceRage[1][0]
            elif nextPosition[1]>self.envparams.stateSpaceRage[1][1]:
                y=self.envparams.stateSpaceRage[1][1]
            return [(currentPosition[1]-yIntercept)/slope,y]
        if yflag==1 and xflag==1:
            if nextPosition[0]<self.envparams.stateSpaceRage[0][0]:
                x=self.envparams.stateSpaceRage[0][0]
            elif nextPosition[0]>self.envparams.stateSpaceRage[0][1]:
                x=self.envparams.stateSpaceRage[0][1]
            if nextPosition[1]<self.envparams.stateSpaceRage[1][0]:
                y=self.envparams.stateSpaceRage[1][0]
            elif nextPosition[1]>self.envparams.stateSpaceRage[1][1]:
                y=self.envparams.stateSpaceRage[1][1]   
            if slope*x+yIntercept < self.envparams.stateSpaceRage[0][0] or slope*x+yIntercept > self.envparams.stateSpaceRage[0][1]:
                return [(currentPosition[1]-yIntercept)/slope,y]
            else: 
                return [x, slope*x+yIntercept]
        if yflag==0 and xflag==0:
            return nextPosition
    
    def OnWallDeflect(self,currentPosition, nextPosition,current_x_index, current_y_index):
        #On x Wall
        if current_x_index==1 and current_y_index==0:
            if currentPosition[1] > nextPosition[1]:
                if currentPosition[1]-(self.stepSize) < self.envparams.stateSpaceRage[1][0]:
                    nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][0]]
                    print("booooooommmmmmmm corner hit")
                    self.cornerIndex=1
                else:
                    nextPosition= [currentPosition[0],currentPosition[1]-(self.stepSize)]
            else:
                if currentPosition[1]+(self.stepSize) > self.envparams.stateSpaceRage[1][1]:
                    nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][1]]
                    print("booooooommmmmmmm corner hit")
                    self.cornerIndex=1
                else:
                    nextPosition= [currentPosition[0],currentPosition[1]+(self.stepSize)]
        #On y Wall
        elif current_x_index==0 and current_y_index==1:
            if currentPosition[0] > nextPosition[0]:
                if currentPosition[0]-(self.stepSize) < self.envparams.stateSpaceRage[0][0]:
                    nextPosition= [self.envparams.stateSpaceRage[0][0], currentPosition[1]]
                    print("booooooommmmmmmm corner hit")
                    self.cornerIndex=1
                else:

                    nextPosition= [currentPosition[0]-(self.stepSize), currentPosition[1]]
            else:
                if currentPosition[0]+(self.stepSize) > self.envparams.stateSpaceRage[0][1]:
                    nextPosition= [self.envparams.stateSpaceRage[0][1],currentPosition[1]]
                    print("booooooommmmmmmm corner hit")
                    self.cornerIndex=1
                else:
                    nextPosition= [currentPosition[0]+(self.stepSize), currentPosition[1]]
        
        return nextPosition , currentPosition
    
    def deflect(self,currentPosition, nextPosition, xflag,yflag, distanceTravelled):
        x_index=0
        y_index=0
        if self.envparams.stateSpaceRage[0][0]==nextPosition[0]:
            x_index=1
        if self.envparams.stateSpaceRage[0][1]==nextPosition[0]:
            x_index=1
        if self.envparams.stateSpaceRage[1][0]==nextPosition[1]:
            y_index=1
        if self.envparams.stateSpaceRage[1][1]==nextPosition[1]:
            y_index=1
        
        #On x Wall
        if x_index==1 and y_index==0:
            if currentPosition[1] > nextPosition[1]:
                currentPosition = nextPosition
                if currentPosition[1]-(self.stepSize-distanceTravelled) < self.envparams.stateSpaceRage[1][0]:
                    nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][0]]
                else: 
                    nextPosition= [currentPosition[0], currentPosition[1]-(self.stepSize-distanceTravelled)]
            elif currentPosition[1] < nextPosition[1]:
                currentPosition = nextPosition
                if currentPosition[1]+(self.stepSize-distanceTravelled) > self.envparams.stateSpaceRage[1][1]:
                    nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][1]]
                else: 
                    nextPosition= [currentPosition[0], currentPosition[1]+(self.stepSize-distanceTravelled)]
            else :
                if random.randint(0,1)==0:
                    currentPosition = nextPosition
                    if currentPosition[1]-(self.stepSize-distanceTravelled) < self.envparams.stateSpaceRage[1][0]:
                        nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][0]]
                    else:
                        nextPosition= [currentPosition[0], currentPosition[1]-(self.stepSize-distanceTravelled)]
                else: 
                    currentPosition = nextPosition
                    if currentPosition[1]+(self.stepSize-distanceTravelled) > self.envparams.stateSpaceRage[1][1]:
                        nextPosition= [currentPosition[0], self.envparams.stateSpaceRage[1][1]]
                    else:
                        nextPosition= [currentPosition[0], currentPosition[1]+(self.stepSize-distanceTravelled)]
        #On y Wall
        elif x_index==0 and y_index==1:
            
            if currentPosition[0] > nextPosition[0]:
                currentPosition = nextPosition
                if currentPosition[0]-(self.stepSize-distanceTravelled) < self.envparams.stateSpaceRage[0][0]:
                    nextPosition= [self.envparams.stateSpaceRage[0][0], currentPosition[1]]
                else:
                    nextPosition= [currentPosition[0]-(self.stepSize-distanceTravelled), currentPosition[1]]
            elif currentPosition[1] < nextPosition[1]:
                currentPosition = nextPosition
                if currentPosition[0]+(self.stepSize-distanceTravelled) > self.envparams.stateSpaceRage[0][1]:
                    nextPosition= [self.envparams.stateSpaceRage[0][1], currentPosition[1]]
                else:
                    nextPosition= [currentPosition[0]+(self.stepSize-distanceTravelled), currentPosition[1]]
            else :
                if random.randint(0,1)==0:
                    currentPosition = nextPosition
                    if currentPosition[0]-(self.stepSize-distanceTravelled) < self.envparams.stateSpaceRage[0][0]:
                        nextPosition= [self.envparams.stateSpaceRage[0][0], currentPosition[1]]
                    else:  
                        nextPosition= [currentPosition[0]-(self.stepSize-distanceTravelled), currentPosition[1]]
                else: 
                    currentPosition = nextPosition
                    if currentPosition[0]+(self.stepSize-distanceTravelled) > self.envparams.stateSpaceRage[0][1]:
                        nextPosition= [self.envparams.stateSpaceRage[0][1], currentPosition[1]]
                    else:
                        nextPosition= [currentPosition[0]+(self.stepSize-distanceTravelled), currentPosition[1]]            
        #Stuck at a corner
        elif x_index==1 and y_index==1:
            if (abs(nextPosition[0]-currentPosition[0]) < abs(nextPosition[1]-currentPosition[1])):
                currentPosition= nextPosition
                if currentPosition[0]==self.envparams.stateSpaceRage[0][0]:
                    nextPosition=[currentPosition[0]+self.stepSize-distanceTravelled, currentPosition[1]]
                if currentPosition[0]==self.envparams.stateSpaceRage[0][1]:
                    nextPosition=[currentPosition[0]-self.stepSize-distanceTravelled, currentPosition[1]]
            if (abs(nextPosition[0]-currentPosition[0]) > abs(nextPosition[1]-currentPosition[1])):
                currentPosition= nextPosition
                if currentPosition[1]==self.envparams.stateSpaceRage[1][0]:
                    nextPosition=[currentPosition[0], currentPosition[1]+self.stepSize-distanceTravelled]
                if currentPosition[1]==self.envparams.stateSpaceRage[1][1]:
                    nextPosition=[currentPosition[0], currentPosition[1]-self.stepSize-distanceTravelled]
            
            if (abs(nextPosition[0]-currentPosition[0]) == abs(nextPosition[1]-currentPosition[1])):
                if random.randint(0,1)==0:
                    currentPosition= nextPosition
                    if currentPosition[0]==self.envparams.stateSpaceRage[0][0]:
                        nextPosition=[currentPosition[0]+self.stepSize-distanceTravelled, currentPosition[1]]
                    if currentPosition[0]==self.envparams.stateSpaceRage[0][1]:
                        nextPosition=[currentPosition[0]-self.stepSize-distanceTravelled, currentPosition[1]]
                else: 
                    currentPosition= nextPosition
                    if currentPosition[1]==self.envparams.stateSpaceRage[1][0]:
                        nextPosition=[currentPosition[0], currentPosition[1]+self.stepSize-distanceTravelled]
                    if currentPosition[1]==self.envparams.stateSpaceRage[1][1]:
                        nextPosition=[currentPosition[0], currentPosition[1]-self.stepSize-distanceTravelled]
        return nextPosition, currentPosition
    
        
    def move(self,currentPosition):
        #print("theta = "+str(self.theta))
        #print("theta_0 = "+str(self.theta_0))
        #print("theta_base = "+str(self.theta_base))
        if self.cornerIndex==1:
            self.cornerIndex=0
            if self.theta_base==90:
                if currentPosition[0]==self.envparams.stateSpaceRage[0][1]:  
                    x=currentPosition[0]-self.stepSize
                    y=currentPosition[1]
                else: 
                    x=currentPosition[0]+self.stepSize
                    y=currentPosition[1]
            elif self.theta_base==270:
                if  currentPosition[0]==self.envparams.stateSpaceRage[0][1]:  
                    x=currentPosition[0]-self.stepSize
                    y=currentPosition[1]
                else:
                    x=currentPosition[0]+self.stepSize
                    y=currentPosition[1]
            elif self.theta_base==0:
                if  currentPosition[1]==self.envparams.stateSpaceRage[1][1]:  
                    x=currentPosition[0]
                    y=currentPosition[1]-self.stepSize
                else:
                    x=currentPosition[0]
                    y=currentPosition[1]+self.stepSize
            elif self.theta_base==180:
                if  currentPosition[1]==self.envparams.stateSpaceRage[1][1]:  
                    x=currentPosition[0]
                    y=currentPosition[1]-self.stepSize
                else:
                    x=currentPosition[0]
                    y=currentPosition[1]+self.stepSize
        else:
            directionalAngle=self.computeDirectionalAngle()
            x= currentPosition[0]+self.stepSize*math.cos(directionalAngle)
            y= currentPosition[1]+self.stepSize*math.sin(directionalAngle)
        xflag=0
        yflag=0
        if not self.xIsInRange(x):
            if not self.yIsInRange(y):
                xflag = 1
                yflag = 1
                #Adjust both x and y based on the minimum deviation of thata with respect to the closes walls
                #and deflect
            else:
                #Adjust x to 10 or 0 and y with respect to the stepSize
                xflag = 1
                yflag = 0                    
        if not self.yIsInRange(y):
            if not self.xIsInRange(x):
                #Adjust both x and y
                xflag = 1
                yflag = 1
            else:
                #Adjust y to 10 or 0 and x with respect to the stepSize
                yflag = 1
                xflag = 0
        
        current_x_index=0
        current_y_index=0

        if self.envparams.stateSpaceRage[0][0]==currentPosition[0]:
            current_x_index=1
        if self.envparams.stateSpaceRage[0][1]==currentPosition[0]:
            current_x_index=1
        if self.envparams.stateSpaceRage[1][0]==currentPosition[1]:
            current_y_index=1
        if self.envparams.stateSpaceRage[1][1]==currentPosition[1]:
            current_y_index=1
        if current_x_index==0 and current_y_index==0:
            nextPosition=self.findWallIntersection(xflag, yflag, currentPosition, [x,y])
            traveledDistanc= round(((nextPosition[1]-currentPosition[1])**2+(nextPosition[0]-currentPosition[0])**2)**(0.5),2)
            traveledDistanc = traveledDistanc.real
            totalTravDist= traveledDistanc
            while(totalTravDist < self.stepSize):
                nextPosition,currentPosition=self.deflect(currentPosition, nextPosition, xflag, yflag, totalTravDist)
                if (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])>0:
                    self.setBaseTheta(90)
                elif (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])<0:
                    self.setBaseTheta(270)
                elif ((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])>0) or((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])<0):
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+180)
                elif (nextPosition[0]-currentPosition[0])>0 and (nextPosition[1]-currentPosition[1])<0:
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+360)
                else:
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0]))))
                    
                traveledDistanc= round(((nextPosition[1]-currentPosition[1])**2+(nextPosition[0]-currentPosition[0])**2)**(0.5),2)
                traveledDistanc = traveledDistanc.real
                totalTravDist+=traveledDistanc  
        else: 
            nextPosition=[x,y]
            x_index=0
            y_index=0
            if self.envparams.stateSpaceRage[0][0]>nextPosition[0]:
                x_index=1
            if self.envparams.stateSpaceRage[0][1]<nextPosition[0]:
                x_index=1
            if self.envparams.stateSpaceRage[1][0]>nextPosition[1]:
                y_index=1
            if self.envparams.stateSpaceRage[1][1]<nextPosition[1]:
                y_index=1 
            if x_index==1 or y_index==1:
                nextPosition,currentPosition=self.OnWallDeflect(currentPosition, nextPosition,current_x_index, current_y_index)
                if (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])>0:
                    self.setBaseTheta(90)
                elif (nextPosition[0]-currentPosition[0])==0 and (nextPosition[1]-currentPosition[1])<0:
                    self.setBaseTheta(270)
                elif ((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])>0) or((nextPosition[0]-currentPosition[0])<0 and (nextPosition[1]-currentPosition[1])<0):
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+180)
                elif (nextPosition[0]-currentPosition[0])>0 and (nextPosition[1]-currentPosition[1])<0:
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0])))+360)
                else:
                    self.setBaseTheta(math.degrees(math.atan((nextPosition[1]-currentPosition[1])/(nextPosition[0]-currentPosition[0]))))
            
            
        return nextPosition