import time
from datetime import date

randomWalkFlag=1
randomWalkFlagExploit=0
goalPoint=[[165,5],[205,85]]


expResults=[[1, 4, 7 ,0.1],[3 ,5, 1.5, 11]]
finalResult=open('test','w')
expResultsSTR=str(expResults)
finalResult.write('The order from the largest to the smallest list:\n')
finalResult.write('Persistence Length --> Learning0 Rate --> Epsilon --> [Average Reward, Reward STD, Average Success Ratio, Success Ratio STD, Epsilon, Learning Rate, Persistence Length]\n')
finalResult.write(expResultsSTR)


finalResult=open('test','r')
x=finalResult.read()
print(float(x))

information=open('information','w')
information.write('Date:'+str(date.today())+'\n\n\n')
if randomWalkFlag==0:
    information.write('Pure Explore: Persistence Length\n')
else:
    information.write('Pure Explore: Random Walk\n')
if randomWalkFlagExploit==0:
    information.write('Epsilon Greedy Explore: Persistence Length\n')
else:
    information.write('Epsilon Greedy Explore: Random Walk\n')
information.write('Region Corner Coordinates:'+str(goalPoint))