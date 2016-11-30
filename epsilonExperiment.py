'''
Created on Nov 14, 2016

@author: Maziar
'''
from ExplorationPolicy import polyExplorer 
import statistics
import math
from cycler import cycler
from graphics import *
from builtins import range
import numpy as np
from qLearner import QLearner
import matplotlib.pyplot as plt

if __name__ == '__main__':
    numIterations=10
    numberOfMoves=200000
    numberOfPureExploreMoves=100000 #numberOfEpsilonGreedy would be "numberOfMoves-numberOfPureExploreMoves".
    numberOfPureExploitMoves=20000
    numberOfTestEvents=20
#     numberOfRoundsExperiments=10
    stepSize=1
    persistenceLengthList=[10,200,700]
    randomWalkFlagExploit=0
    epsilonList=[0.1,0.4,0.7]
    learningRateList= [0.1,0.3,0.5]
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
    
    #for i in range(len(learningRateList)):
    #    for j in range(len(epsilonList)):
    plt.figure()
#     ax = plt.gca()
#     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
            
    avgReward=[]
    std=[]
    #Plot average reward as a function of learning rate for a certain persistence length 
    for k in range(len(epsilonList)):
        for j in range(len(learningRateList)):
            avgReward.append(expResults[1][j][k][0])
            std.append(expResults[1][j][k][1])
        print(avgReward)
        print(std)
        plt.errorbar(learningRateList, avgReward, yerr=std, fmt='o')   
        avgReward=[]
        std=[]
            
    
    print(expResults)
    
#     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
    
    plt.xlim(0,1)
    plt.ylim(-100,100)
    plt.ylabel('Average Reward')
    plt.xlabel('Learning Rate')
    plt.legend(["epsilon=0.1","epsilon=0.4", "epsilon=0.7" ],loc=0)
    plt.title("Average Reward for P=200")
    plt.savefig('1.png')
    
    plt.figure()
#     ax1 = plt.gca()
#     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
    avgSuccessRatio=[]
    std=[]
    for k in range(len(epsilonList)):
        for j in range(len(learningRateList)):
            avgSuccessRatio.append(expResults[1][j][k][2])
            std.append(expResults[1][j][k][3])
        print(avgSuccessRatio)
        print(std)
        plt.errorbar(learningRateList, avgSuccessRatio, yerr=std, fmt='o')   
        avgSuccessRatio=[]
        std=[]
            
    
    print(expResults)
    
#     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
    
    plt.xlim(0,1)
    plt.ylim(-0.5,1)
    plt.ylabel('Ratio of Successful Events')
    plt.xlabel('Learning Rate')
    plt.legend(["epsilon=0.1","epsilon=0.4", "epsilon=0.7" ],loc=0)
    plt.title("Ratio of Successful Events for P=200")
    plt.savefig('2.png')
    
    plt.figure()
#     ax2 = plt.gca()
#     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
            
    avgReward=[]
    std=[]
    #Plot average reward as a function of learning rate for a certain persistence length 
    for j in range(len(learningRateList)):
        for i in range(len(persistenceLengthList)):
            avgReward.append(expResults[i][j][0][0])
            std.append(expResults[i][j][0][1])
        print(avgReward)
        print(std)
        plt.errorbar(persistenceLengthList, avgReward, yerr=std, fmt='o')   
        avgReward=[]
        std=[]
            
    
    print(expResults)
    
#     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
    
    plt.xlim(0,1000)
    plt.ylim(-100,100)
    plt.ylabel('Average Reward')
    plt.xlabel('Persistence Length')
    plt.legend(["alpha=0.05","alpha=0.1", "alpha=0.2", "alpha=0.3", "alpha=0.4", "alpha=0.5"  ],loc=0)
    plt.title("Average Reward for epsilon=0.1")
    plt.savefig('3.png')
    
    plt.figure()
#     ax3 = plt.gca()
#     plt.set_color_cycle(['b', 'r', 'g', 'c', 'k', 'y', 'm'])
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +cycler('linestyle', ['-', '--', ':', '-.'])))
    avgSuccessRatio=[]
    std=[]
    for j in range(len(learningRateList)):
        for i in range(len(persistenceLengthList)):
            avgSuccessRatio.append(expResults[i][j][0][2])
            std.append(expResults[i][j][0][3])
        print(avgSuccessRatio)
        print(std)
        plt.errorbar(persistenceLengthList, avgSuccessRatio, yerr=std, fmt='o')   
        avgSuccessRatio=[]
        std=[]
            
    
    print(expResults)
    
#     ax.errorbar(learningRateList, avgReward, yerr=std, fmt='o')
    
    plt.xlim(0,1000)
    plt.ylim(-0.5,1)
    plt.ylabel('Ratio of Successful Events')
    plt.xlabel('Persistence Length')
    plt.legend(["alpha=0.05","alpha=0.1", "alpha=0.2", "alpha=0.3", "alpha=0.4", "alpha=0.5"  ],loc=0)
    plt.title("Ratio of Successful Events for epsilon=0.1")
    plt.savefig('4.png')
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
#     mean_V_vs_LSW[j]=abs(numpy.average(temptemp))
#     std_V_vs_LSW[j] = numpy.std(temptemp)
#     V_vs_LSW_bldu[j] = math.log10(abs(mean_V_vs_LSW[j]+std_V_vs_LSW[j]))-math.log10(abs(mean_V_vs_LSW[j]))
#     V_vs_LSW_bldl[j] = -math.log10(abs(mean_V_vs_LSW[j]-std_V_vs_LSW[j]))+math.log10(abs(mean_V_vs_LSW[j]))
#     V_vs_LSW_blm[j] = math.log10(abs(mean_V_vs_LSW[j]))
    