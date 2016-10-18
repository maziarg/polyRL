'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from graphics import *
from builtins import range
from numpy import *
from qLearner import QLearner

if __name__ == '__main__':
    
    
    numberOfMoves=20000
    numberOfPureExpMoves=1000
    stepSize=1
    persistenceLength=200
    learningRate=0.1
    epsilon=0.99
    epsilon_init=1 
    actionSampleingDensity=10
    
    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
    #myTurtle= turtle()
    #anchorpoint= Point(polyexp.envparams.stateSpaceRange[0][1]/2,polyexp.envparams.stateSpaceRange[1][1]/2)
    #image= Image(anchorpoint, polyexp.envparams.stateSpaceRange[0][1], polyexp.envparams.stateSpaceRange[1][1])
    qAgent = QLearner(learningRate, epsilon, actionSampleingDensity, polyexp)
    weightVec= qAgent.weightVector
    initPosition=polyexp.drawInitState()
    tempState=initPosition
    angle=polyexp.theta_0
    #positionArray=zeros((numberOfMoves,2))
    win = GraphWin("GRID",  1000,1000)
    line1 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]))
    line1.draw(win)
    line2 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]))
    line2.draw(win)
    line3 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]))
    line3.draw(win)
    line4 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]))
    line4.draw(win)
    cir1 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), 5)
    cir1.draw(win)
    cir2 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), 5)
    cir2.draw(win)
    cir3 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), 5)
    cir3.draw(win)
    cir4 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), 5)
    cir4.draw(win)
    line = Line(Point(polyexp.envparams.goalZone[0][0],polyexp.envparams.goalZone[1][0]), Point(polyexp.envparams.goalZone[0][1],polyexp.envparams.goalZone[1][1]))
    line.draw(win)
    for i in range(numberOfMoves):
        if i<numberOfPureExpMoves:
            qAgent.setEpsilon(epsilon_init)
        else:
            qAgent.setEpsilon(epsilon)
        action=qAgent.getAction(tempState)
        print("action= "+str(action))
        polyexp.setBaseTheta(action)
        oldState=tempState
        print("move #"+str(i)+ " = "+str(oldState))
        tempState=polyexp.move(oldState)
        newState=tempState
        reward=qAgent.getReward(newState)
        weightVec=qAgent.update(oldState, action, newState, reward)
        line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
        line.draw(win)
        
        #sety(tempState)
        #goto(oldState,newState)
    # saves the current TKinter object in postscript format
    win.postscript(file="image.eps", colormode='color')
    print("theta:",str(polyexp.theta))
    print("Number of segments in each square:",str(polyexp.numberOfSegment))
    print("weight vector: "+ str(weightVec))
    