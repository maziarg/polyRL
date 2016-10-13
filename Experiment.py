'''
Created on Sep 15, 2016

@author: qubit
'''
from ExplorationPolicy import polyExplorer 
from graphics import *
from builtins import range
from numpy import *
from operator import truediv

if __name__ == '__main__':
    
    
    numberOfMoves=20000
    stepSize=1
    persistenceLength=1000 
    polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
    #myTurtle= turtle()
    #anchorpoint= Point(polyexp.envparams.stateSpaceRange[0][1]/2,polyexp.envparams.stateSpaceRange[1][1]/2)
    #image= Image(anchorpoint, polyexp.envparams.stateSpaceRange[0][1], polyexp.envparams.stateSpaceRange[1][1])
    
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
    for i in range(numberOfMoves):
        xCoordinate=tempState
        #print("angle #"+str(i)+ " = "+str(angle))
        print("move #"+str(i)+ " = "+str(tempState))
        angle=polyexp.theta_base
        #print("theta_base = "+str(i)+ " = "+str(angle))
        tempState=polyexp.move(tempState)
        yCoordinate=tempState
        line = Line(Point(xCoordinate[0],xCoordinate[1]), Point(yCoordinate[0],yCoordinate[1]))
        line.draw(win)
        
        #sety(tempState)
        #goto(xCoordinate,yCoordinate)
    # saves the current TKinter object in postscript format
    win.postscript(file="image.eps", colormode='color')
    print("theta:",str(polyexp.theta))
    print("Number of segments in each square:",str(polyexp.numberOfSegment))
    x1=numberOfMoves/16
    x2=x1*3
    x3=x1*5
    x4=x1*7
    numberOfSegmentIdeal=[x1, x2, x3, x4]
    Comparison=[]
    for i in range(4):
        Comparison.append(polyexp.numberOfSegment[0][i]/numberOfSegmentIdeal[i])
    #Comparison=[(x)/y for x, y in zip(polyexp.numberOfSegment, numberOfSegmentIdeal)]
    print(numberOfSegmentIdeal)
    print(Comparison)
    print("persistence length = ", str(persistenceLength))