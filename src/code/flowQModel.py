#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/10 22:19
from code.config import *
from math import inf

def computeFlowInput(weight,flowQ,t):
    fZeros = np.where(flowQ[:,t]== 0)
    noZeros = np.where((flowQ[:,t] != 0))
    flowInVec = np.zeros((numOfN,1))
    flowInVec[noZeros] = weight/flowQ[noZeros] -1
    flowInVec[fZeros] = inf
    flowInVec = np.where(flowInVec > dataArrival_max,dataArrival_max,flowInVec)
    return flowInVec

def updateFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max,t):
    flowQ[:,t+1] = flowQ[:,t] - dataHarVec.T + flowInVec.T
    flowQ[0,t+1] = flowQ_max



