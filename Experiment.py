'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from graphics import *
from builtins import range
from numpy import *
from qLearner import QLearner
import numpy as np

if __name__ == '__main__':
    
    
    numberOfMoves=30000
    numberOfPureExploreMoves=20000
    numberOfPureExploitMoves=5000
    stepSize=1
    persistenceLength=150
    learningRate=0.5
     
    epsilon_init=1 
    epsilon=epsilon_init
    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
    actionSamplingDensity=polyexp.envparams.actionFeatureDim
    #myTurtle= turtle()
    #anchorpoint= Point(polyexp.envparams.stateSpaceRange[0][1]/2,polyexp.envparams.stateSpaceRange[1][1]/2)
    #image= Image(anchorpoint, polyexp.envparams.stateSpaceRange[0][1], polyexp.envparams.stateSpaceRange[1][1])
    qAgent = QLearner(learningRate, epsilon_init, actionSamplingDensity, polyexp)
    weightVec= qAgent.weightVector
    initPosition=polyexp.drawInitState()
    tempState=initPosition
    angle=polyexp.theta_0
    goalRegion=qAgent.goalZone()
    exploitReward=0
    numberOfExploitExperiment=100
    #positionArray=zeros((numberOfMoves,2))
    win1 = GraphWin("GRID",  polyexp.envparams.stateSpaceRange[0][1]+10-polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]+10-polyexp.envparams.stateSpaceRange[1][0])
    line1 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]))
    line1.draw(win1)
    line2 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]))
    line2.draw(win1)
    line3 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]))
    line3.draw(win1)
    line4 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]))
    line4.draw(win1)
    cir1 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), 5)
    cir1.draw(win1)
    cir2 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), 5)
    cir2.draw(win1)
    cir3 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), 5)
    cir3.draw(win1)
    cir4 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), 5)
    cir4.draw(win1)
    goalPoint=qAgent.goalBorders()
    rect = Rectangle(goalPoint[0],goalPoint[1])
#     rect.setOutline('red')
    rect.setFill('aquamarine')
    rect.draw(win1)
    k=0
    #line = Line(Point(polyexp.envparams.goalZone[0][0],polyexp.envparams.goalZone[1][0]), Point(polyexp.envparams.goalZone[0][1],polyexp.envparams.goalZone[1][1]))
    #line.draw(win1)
#     cirG = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[0][1]), polyexp.envparams.goalZoneRin)
#     cirG.draw(win1)
#     cirG.setOutline('red')
#     cirG = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[0][1]), polyexp.envparams.goalZoneRout)
#     cirG.setOutline('red')
#     cirG.draw(win1)
    
    for i in range(numberOfMoves):
        if i<numberOfPureExploreMoves:
            qAgent.setEpsilon(epsilon_init)
        elif i<numberOfMoves-numberOfPureExploitMoves:
            epsilon=(epsilon_init/(numberOfPureExploreMoves-(numberOfMoves-numberOfPureExploitMoves)))*(i-(numberOfMoves-numberOfPureExploitMoves))
        elif i==numberOfMoves-numberOfPureExploitMoves:
            initPosition=polyexp.drawInitState()
            tempState=initPosition
            angle=polyexp.theta_0
            epsilon=0
        else:
            epsilon=0
        qAgent.setEpsilon(epsilon)
        print("epsilon="+str(epsilon))
        action=qAgent.getAction(tempState)
        print("action= "+str(action))
        print("goalRegion="+str(goalRegion))
#         polyexp.setBaseTheta(action)
        oldState=tempState
        print("move #"+str(i)+ " = "+str(oldState))
        tempState=polyexp.move(oldState)
        newState=tempState
        reward=qAgent.getReward(newState)
        weightVec=qAgent.update(oldState, action, newState, reward)
        if i>numberOfMoves-numberOfPureExploitMoves:
            exploitReward+=reward
            if reward==polyexp.envparams.goalReward:
                print("Accumulative Reward="+str(exploitReward))
                break
            if i==numberOfMoves-1:
                print("Didn't reach goal")
        if i!=numberOfMoves-numberOfPureExploitMoves:
            line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
            if qAgent.exploitFlag==1:
                line.setOutline('red')
            line.draw(win1)
        if i>numberOfMoves-numberOfPureExploitMoves:
            if k==0:
                win2 = GraphWin("GRID",  polyexp.envparams.stateSpaceRange[0][1]+10-polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]+10-polyexp.envparams.stateSpaceRange[1][0])
                line1 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]))
                line1.draw(win2)
                line2 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]))
                line2.draw(win2)
                line3 = Line(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]))
                line3.draw(win2)
                line4 = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]))
                line4.draw(win2)
                cir1 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][0]), 5)
                cir1.draw(win2)
                cir2 = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[1][1]), 5)
                cir2.draw(win2)
                cir3 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][0]), 5)
                cir3.draw(win2)
                cir4 = Circle(Point(polyexp.envparams.stateSpaceRange[0][1],polyexp.envparams.stateSpaceRange[1][1]), 5)
                cir4.draw(win2)
                goalPoint=qAgent.goalBorders()
                rect = Rectangle(goalPoint[0],goalPoint[1])
            #     rect.setOutline('red')
                rect.setFill('aquamarine')
                rect.draw(win2)
                k=1
            line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
            line.setOutline('red')
            line.draw(win2)
        #sety(tempState)
        #goto(oldState,newState)
    # saves the current TKinter object in postscript format
    win1.postscript(file="image.eps", colormode='color')
    win2.postscript(file="Exploit.eps",colormode='color')
    #print("theta:",str(polyexp.theta))
    #print("Number of segments in each square:",str(polyexp.numberOfSegment))
    print("weight vector: "+ str(weightVec))
    