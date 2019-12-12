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
    # flowInVec = np.ones((numOfN,1)) * dataArrival_max
    # fZeros = np.where(flowQ[:,t]== 0)
    # flowInVec[fZeros] = inf
    # noZeros = np.where((flowQ[:,t] != 0))
    # flowInVec = np.zeros((numOfN,1))
    # print("flowQ[noZeros]:",flowQ[noZeros])
    # if (len(noZeros) != 0):
    #     flowInVec[noZeros] = weight/flowQ[noZeros] -1
    # flowInVec = np.where(flowInVec > dataArrival_max,dataArrival_max,flowInVec)
    # print("flowInVec:",flowInVec)
    return flowInVec

def updateFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max,t):
    # print("flowInVec:",flowInVec)
    # print("dataHarVec:",dataHarVec)
    flowQ[:,t+1] = flowQ[:,t] - dataHarVec.T + flowInVec.T
    flowQ[0,t+1] = flowQ_max



