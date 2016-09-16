'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from builtins import range

if __name__ == '__main__':
    numberOfMoves=1000
    stepSize=2
    persistanceLenghth=1000
    polyexp= polyExplorer(numberOfMoves, stepSize, persistanceLenghth)
    
    initPosition=polyexp.drawInitState()
    tempState=initPosition
    angle=polyexp.theta_0
    for i in range(numberOfMoves):
        
        #print("angle #"+str(i)+ " = "+str(angle))
        print("move #"+str(i)+ " = "+str(tempState))
        angle=polyexp.theta_base
        #print("theta_base = "+str(i)+ " = "+str(angle))
        tempState=polyexp.move(tempState)
        