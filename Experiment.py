'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from builtins import range
from numpy import zeros

if __name__ == '__main__':
    numberOfMoves=10000
    stepSize=20
    persistenceLength=200
    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
    
    initPosition=polyexp.drawInitState()
    tempState=initPosition
    angle=polyexp.theta_0
    positionArray=zeros((numberOfMoves,2))
    for i in range(numberOfMoves):
        
        #print("angle #"+str(i)+ " = "+str(angle))
        print("move #"+str(i)+ " = "+str(tempState))
        positionArray[i,:]=tempState
        angle=polyexp.theta_base
        #print("theta_base = "+str(i)+ " = "+str(angle))
        tempState=polyexp.move(tempState)
    positionArray[numberOfMoves-1,:]=tempState
    numOfStatesVisited=polyexp.countNumStatesVisited(positionArray)
    numStates=polyexp.envparams.gridXscale*polyexp.envparams.gridYscale
    fractionVisited=numOfStatesVisited/numStates
    print("Total number of states:"+str(numStates))
    print("Number of visited states:"+str(numOfStatesVisited))
    print("Fraction of states visited:"+str(fractionVisited))