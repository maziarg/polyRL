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
    
    
    numberOfMoves=100000
    numberOfPureExploreMoves=100000 #numberOfEpsilonGreedy would be "numberOfMoves-numberOfPureExploreMoves".
    numberOfPureExploitMoves=20000
    numberOfTestEvents=50
    stepSize=1
    persistenceLength=150
    learningRate=0.2
    epsilonGreedy=0.3
    epsilonIncrement=0.1
     
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
#     goalPoint=qAgent.goalBorders()
    goalPoint=[Point(polyexp.envparams.goalPoint[0][0],polyexp.envparams.goalPoint[0][1]),Point(polyexp.envparams.goalPoint[1][0],polyexp.envparams.goalPoint[1][1])]
    rect = Rectangle(goalPoint[0],goalPoint[1])
#     rect.setOutline('red')
    rect.setFill('aquamarine')
    rect.draw(win1)
    #line = Line(Point(polyexp.envparams.goalZone[0][0],polyexp.envparams.goalZone[1][0]), Point(polyexp.envparams.goalZone[0][1],polyexp.envparams.goalZone[1][1]))
    #line.draw(win1)
#     cirG = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[0][1]), polyexp.envparams.goalZoneRin)
#     cirG.draw(win1)
#     cirG.setOutline('red')
#     cirG = Circle(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[0][1]), polyexp.envparams.goalZoneRout)
#     cirG.setOutline('red')
#     cirG.draw(win1)
    k=0
    for i in range(numberOfMoves):
        if i<numberOfPureExploreMoves:
            qAgent.setEpsilon(epsilon_init)
        else:
#             epsilon=(epsilon_init/(numberOfPureExploreMoves-(numberOfMoves-numberOfPureExploitMoves)))*(i-(numberOfMoves-numberOfPureExploitMoves))
#             epsilon=epsilonGreedy
            if (i-numberOfPureExploreMoves)==k*(numberOfMoves-numberOfPureExploreMoves)/10:
                k+=1
                epsilon=epsilon_init-k*epsilonIncrement
        qAgent.setEpsilon(epsilon)
        print("epsilon="+str(epsilon))
        action=qAgent.getAction(tempState) 
        print("action= "+str(action))
#         print("goalRegion="+str(goalRegion))
#         polyexp.setBaseTheta(action)
        oldState=tempState
        print("move #"+str(i)+ " = "+str(oldState))
        tempState=polyexp.move(oldState)
        newState=tempState
        if polyexp.deflectFlag==1:
            action=polyexp.actionTemp
            polyexp.deflectFlag=0
        reward=qAgent.getReward(newState)
        weightVec=qAgent.update(oldState, action, newState, reward)
        line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
        if qAgent.exploitFlag==1:
            line.setOutline('red')
        line.draw(win1)
        #sety(tempState)
        #goto(oldState,newState)
    # saves the current TKinter object in postscript format
    win1.postscript(file="image.eps", colormode='color')
    epsilon=0
    qAgent.setEpsilon(epsilon)
    totalReward=0
    numberOfSuccessfulEvents=0
    for i in range(numberOfTestEvents):
        initPosition=polyexp.drawInitState()
        polyexp.nextPosition=initPosition
        tempState=initPosition
        angle=polyexp.theta_0
        exploitReward=0
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
        goalPoint=[Point(polyexp.envparams.goalPoint[0][0],polyexp.envparams.goalPoint[0][1]),Point(polyexp.envparams.goalPoint[1][0],polyexp.envparams.goalPoint[1][1])]
#         goalPoint=qAgent.goalBorders()
        rect = Rectangle(goalPoint[0],goalPoint[1])
    #     rect.setOutline('red')
        rect.setFill('aquamarine')
        rect.draw(win2)
        for j in range(numberOfPureExploitMoves):
            action=qAgent.getAction(tempState) 
            print("action= "+str(action))
#             print("goalRegion="+str(goalRegion))
            print("test# "+str(i+1))
            oldState=tempState
            print("move #"+str(j)+ " = "+str(oldState))
            tempState=polyexp.move(oldState)
            newState=tempState
            if polyexp.deflectFlag==1:
                action=polyexp.actionTemp
                polyexp.deflectFlag=0
            reward=qAgent.getReward(newState)
            line = Line(Point(oldState[0],oldState[1]), Point(newState[0],newState[1]))
            line.setOutline('red')
            line.draw(win2)
            exploitReward+=reward
            if reward==polyexp.envparams.goalReward:
                print("Accumulative Reward="+str(exploitReward))
                numberOfSuccessfulEvents+=1
                break
            if j==numberOfPureExploitMoves-1:
                print("Accumulative Reward="+str(exploitReward))
                print("Didn't reach goal")
        totalReward=totalReward+exploitReward
        win2.getMouse() # pause for click in window
#         input("Press Enter to continue...")
        win2.postscript(file="Exploit.eps",colormode='color')
        win2.close()
    averageReward=totalReward/numberOfTestEvents
    #print("theta:",str(polyexp.theta))
    #print("Number of segments in each square:",str(polyexp.numberOfSegment))
    print("action matrix: "+str(qAgent.actionMatrix))
    print("average reward over "+str(numberOfTestEvents)+" tests= "+str(averageReward))
    print("number of successful events in "+str(numberOfTestEvents)+" experiments= "+str(numberOfSuccessfulEvents)+" ("+str(numberOfSuccessfulEvents/numberOfTestEvents*100)+"%)")
    