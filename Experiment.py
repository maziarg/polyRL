'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from graphics import *
from builtins import range
from numpy import zeros

if __name__ == '__main__':
    numberOfMoves=1000
    stepSize=2
    persistenceLength=100
    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
    #myTurtle= turtle()
    initPosition=polyexp.drawInitState()
    tempState=initPosition
    angle=polyexp.theta_0
    positionArray=zeros((numberOfMoves,2))
    win = GraphWin("GRID",  1000,1000)
    line = Line(Point(polyexp.envparams.stateSpaceRange[0][0],polyexp.envparams.stateSpaceRange[0][1]), Point(polyexp.envparams.stateSpaceRange[1][0],polyexp.envparams.stateSpaceRange[1][1]))
    line.draw(win)
    for i in range(numberOfMoves):
        xCoordinate=tempState
        #print("angle #"+str(i)+ " = "+str(angle))
        print("move #"+str(i)+ " = "+str(tempState))
        positionArray[i,:]=tempState
        angle=polyexp.theta_base
        #print("theta_base = "+str(i)+ " = "+str(angle))
        tempState=polyexp.move(tempState)
        yCoordinate=tempState
        line = Line(Point(xCoordinate[0],xCoordinate[1]), Point(yCoordinate[0],yCoordinate[1]))
        line.draw(win)
        #sety(tempState)
        #goto(xCoordinate,yCoordinate)
    positionArray[numberOfMoves-1,:]=tempState
    numOfStatesVisited=polyexp.countNumStatesVisited(positionArray)
    numStates=polyexp.envparams.gridXscale*polyexp.envparams.gridYscale
    fractionVisited=numOfStatesVisited/numStates
    print("Total number of states:"+str(numStates))
    print("Number of visited states:"+str(numOfStatesVisited))
    print("Fraction of states visited:"+str(fractionVisited))