#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/10 22:19
from code.config import *
from math import inf

def computeFlowInput(weight,flowQ,t):
    flowInVec = np.zeros((numOfN, 1))
    for n in range(numOfN):
        if flowQ[n,t] == 0:
            flowInVec[n] = dataArrival_max
        elif flowQ[n,t] >0:
            tmp = weight/flowQ[n,t] -1
            if tmp < 0:
                flowQ[n,t] = 0
            elif tmp < dataArrival_max:
                flowQ[n,t] = tmp
            else:
                flowQ[n, t] = dataArrival_max
    return flowInVec
def computeFlowInputWithSingleFlowQ(weight,flowQ,t):
    flowGenVec = np.random.uniform(0, 1, (numOfN, 1)) * dataArrival_max
    flowHarVec = np.zeros((numOfN, 1))
    if flowQ[t] == 0:
        tmpF = inf
    else:
        tmpF = weight / flowQ[t] - 1
    for i in range(numOfN):
        if tmpF < 0:
            flowHarVec[i] = 0
        elif tmpF >= flowGenVec[i]:
            flowHarVec[i] = flowGenVec[i]
        else:
            flowHarVec[i] = tmpF
    flowHarVec[0] = 0
    return np.sum(flowHarVec)

def updateFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max,t):
    # print("flowInVec:",flowInVec)
    # print("dataHarVec:",dataHarVec)
    flowQ[:,t+1] = flowQ[:,t] - dataHarVec.T+ flowInVec.T
    flowQ[:, t + 1] = np.where(flowQ[:, t + 1]<0,0,flowQ[:, t + 1])
    flowQ[0,t+1] = flowQ_max
def updateFlowQWithSigleFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max,t):
    totalIn = flowInVec
    totalOut = np.sum(dataHarVec[1:])
    flowQ[t+1] = flowQ[t] - totalOut + totalIn
    if flowQ[t+1] < 0:
        flowQ[t+1] = 0




