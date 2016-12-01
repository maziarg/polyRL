'''
Created on Nov 14, 2016

@author: Maziar
'''
from ExplorationPolicy import polyExplorer 
import statistics
import math
from builtins import range
import numpy as np
from qLearner import QLearner
import time
from datetime import date
# import matplotlib.pyplot as plt

if __name__ == '__main__':
    numIterations=2
    numberOfMoves=200000
    numberOfPureExploreMoves=100000 #numberOfEpsilonGreedy would be "numberOfMoves-numberOfPureExploreMoves".
    numberOfPureExploitMoves=20000
    numberOfTestEvents=20
#     numberOfRoundsExperiments=10
    stepSize=1
    persistenceLengthList=[200]
    randomWalkFlagExploit=0
    epsilonList=[0.1]
    learningRateList= [0.1]
    epsilon_init=1
#     k=0
#     n=0
    expResults=[]
    
    for per in range(len(persistenceLengthList)):
        persistenceLength=persistenceLengthList[per]
        prsistanatTempResult=[]
        for i in range(len(learningRateList)):
            tempResult=[]
            for j in range(len(epsilonList)):
                iterationAvgRewList=[]
                successRatioAvgList=[]
                iterationSTD=0
                iterationAVG=0
                successAVG=0
                successSTD=0
                for iteration in range(numIterations):
                    averageReward=0
                    totalReward=0
                    numberOfSuccessfulEvents=0
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
                        print(str(per+1)+":"+str(len(persistenceLengthList))+"--"+str(i+1)+":"+str(len(learningRateList))+"--"+str(j+1)+":"+str(len(epsilonList))+"--"+str(iteration+1)+":"+str(numIterations)+"--"+str(num+1)+"/"+str(numberOfMoves))
                        if qAgent.isInGoalZone(tempState):
                            initPosition=polyexp.drawInitState()
                            tempState=initPosition
                            angle=polyexp.theta_0
    #                         if num>=numberOfPureExploreMoves:
    #                             n+=1
    #                             continue
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
                    for p in range(numberOfTestEvents):
                        initPosition=polyexp.drawInitState()
                        polyexp.nextPosition=initPosition
                        tempState=initPosition
                        angle=polyexp.theta_0
                        exploitReward=0
                        for q in range(numberOfPureExploitMoves):
                            print(str(per+1)+":"+str(len(persistenceLengthList))+"--"+str(i+1)+":"+str(len(learningRateList))+"--"+str(j+1)+":"+str(len(epsilonList))+"--"+str(iteration+1)+":"+str(numIterations)+"--"+str(num+1)+"/"+str(numberOfMoves)+"("+str(p+1)+":"+str(numberOfTestEvents)+"--"+str(q+1)+":"+str(numberOfPureExploitMoves)+")")
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
                    iterationAvgRewList.append(averageReward)
                    successRatio=numberOfSuccessfulEvents/numberOfTestEvents
                    successRatioAvgList.append(successRatio)
                    
                iterationSTD=statistics.stdev(iterationAvgRewList)/math.sqrt(len(iterationAvgRewList))
                iterationAVG=statistics.mean(iterationAvgRewList)
                successAVG=statistics.mean(successRatioAvgList)
                successSTD=statistics.stdev(successRatioAvgList)/math.sqrt(len(successRatioAvgList))
                bldu = iterationAVG+iterationSTD
                bldl = iterationAVG-iterationSTD
                tempResult.append([iterationAVG, iterationSTD, successAVG, successSTD, epsilonList[j], learningRateList[i], persistenceLength])
            prsistanatTempResult.append(tempResult)
        expResults.append(prsistanatTempResult)
    
    
    finalResult=open('Final Result','w')
    finalResult.write(str(expResults))
    
    information=open('information','w')
    information.write('Date: '+str(date.today())+'\n\n\n')
    if polyexp.randomWalkFlag==0:
        information.write('Pure Explore: Persistence Length\n')
    else:
        information.write('Pure Explore: Random Walk\n')
    if randomWalkFlagExploit==0:
        information.write('Epsilon Greedy Explore: Persistence Length\n')
    else:
        information.write('Epsilon Greedy Explore: Random Walk\n')
    information.write('Region Corner Coordinates: '+str(polyexp.envparams.goalPoint)+'\n\n\n')
    
    information.write('#Pure Explore: '+str(numberOfPureExploreMoves)+'\n')
    information.write('#Epsilon Greedy: '+str(numberOfMoves-numberOfPureExploreMoves)+'\n')
    information.write('#Pure Exploit: '+str(numberOfPureExploitMoves)+'\n')
    
    if polyexp.randomWalkFlag==0 or randomWalkFlagExploit==0:
        information.write('Persistence Length: '+str(persistenceLengthList)+'\n')
    else:
        information.write('Persistence Length: N/A\n')
    information.write('Learning Rate: '+str(learningRateList)+'\n')
    information.write('Epsilon: '+str(epsilonList)+'\n')
    information.write('Discount Factor: '+str(polyexp.envparams.discountFactor)+'\n')
    information.write('Theta STD: '+str(polyexp.STD)+'\n')
    information.write('#Space Regions: '+str(polyexp.envparams.stateFeatureDim)+' (X: '+str(polyexp.envparams.stateFeatureDimX)+', Y: '+str(polyexp.envparams.stateFeatureDimY)+')\n')
    information.write('Environment Corner Coordinates: '+str(polyexp.envparams.stateSpaceRange)+'\n')
    information.write('Angle Range: '+str(polyexp.envparams.angleRange)+'\n')
    information.write('#Action Regions: '+str(polyexp.envparams.actionFeatureDim)+'\n')
    information.write('Action STD: '+str(polyexp.envparams.actionSTD)+'\n\n\n')
    information.write('Regular Reward: '+str(polyexp.envparams.regularReward)+'\n')
    information.write('Wall Reward: '+str(polyexp.envparams.wallReward)+'\n')
    information.write('Goal Reward: '+str(polyexp.envparams.goalReward)+'\n')
    information.write('#Test Events: '+str(numberOfTestEvents)+'\n')
    information.write('#Iterations on Whole Experiment: '+str(numIterations))
    
