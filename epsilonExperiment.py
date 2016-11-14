'''
Created on Nov 14, 2016

@author: Maziar
'''
from ExplorationPolicy import polyExplorer 
from graphics import *
from builtins import range
from numpy import *
from qLearner import QLearner

if __name__ == '__main__':
    numberOfMoves=20000
    numberOfPureExploreMoves=10000 #numberOfEpsilonGreedy would be "numberOfMoves-numberOfPureExploreMoves".
    numberOfPureExploitMoves=5000
    numberOfTestEvents=10
    numberOfRoundsExperiments=10
    stepSize=1
    persistenceLength=200
    randomWalkFlagExploit=0
    epsilonList=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    learningRateList= [0.01, 0.05, 0.1, 0.15 ,0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]
    epsilon_init=1
    k=0
    n=0
    expResults=[]
    for i in range(len(learningRateList)):
        tempResult=[]
        for j in range(len(epsilonList)):
            epsilon=epsilon_init
            polyexp= polyExplorer(numberOfMoves, stepSize, persistenceLength)
            polyexp.setRandomWalkFlag(0)
            actionSamplingDensity=polyexp.envparams.actionFeatureDim
            qAgent = QLearner(learningRateList[i], epsilon_init, actionSamplingDensity, polyexp)
            weightVec= qAgent.weightVector
            initPosition=polyexp.drawInitState()
            tempState=initPosition
            angle=polyexp.theta_0
            goalRegion=qAgent.goalZone()
            for num in range(numberOfMoves):
                if qAgent.isInGoalZone(tempState):
                    initPosition=polyexp.drawInitState()
                    tempState=initPosition
                    angle=polyexp.theta_0
                if num>=numberOfPureExploreMoves:
                    n+=1
                    continue
                if num<numberOfPureExploreMoves:
                    qAgent.setEpsilon(epsilon_init)
                else:
                    epsilon=epsilonList[j]
                    polyexp.setRandomWalkFlag(randomWalkFlagExploit)
                qAgent.setEpsilon(epsilon)
                action=qAgent.getAction(tempState) 
                oldState=tempState
                tempState=polyexp.move(oldState)
                newState=tempState
                if polyexp.deflectFlag==1:
                    action=polyexp.actionTemp
                    polyexp.deflectFlag=0
                reward=qAgent.getReward(newState)
                weightVec=qAgent.update(oldState, action, newState, reward)
                
            epsilon=0
            qAgent.setEpsilon(epsilon)
            totalReward=0
            numberOfSuccessfulEvents=0
            for p in range(numberOfTestEvents):
                initPosition=polyexp.drawInitState()
                polyexp.nextPosition=initPosition
                tempState=initPosition
                angle=polyexp.theta_0
                exploitReward=0
                for q in range(numberOfPureExploitMoves):
                    action=qAgent.getAction(tempState) 
                    oldState=tempState
                    tempState=polyexp.move(oldState)
                    newState=tempState
                    if polyexp.deflectFlag==1:
                        action=polyexp.actionTemp
                        polyexp.deflectFlag=0
                    reward=qAgent.getReward(newState)
                    exploitReward+=reward
                    if reward==polyexp.envparams.goalReward:
                        numberOfSuccessfulEvents+=1
                        break
            totalReward=totalReward+exploitReward
            averageReward=totalReward/numberOfTestEvents
            tempResult.append([averageReward,numberOfSuccessfulEvents/numberOfTestEvents*100, epsilonList[j], learningRateList[i]])
            averageReward=0
            totalReward=0
            numberOfSuccessfulEvents=0
        expResults.append(tempResult)
    print(expResults)