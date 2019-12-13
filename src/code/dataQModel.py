#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:43
import numpy as np
from code.config import *
from math import inf
def computeDataHar(dataQ,enQ,flowQ,batterCapacity,t):
    dataGenVec = np.random.uniform(0, 1, (numOfN, 1)) * dataArrival_max
    dataHarVec = np.zeros((numOfN,1))
    tmp = P_H * (batterCapacity -enQ[:,t]) + dataQ[:,t] - flowQ[:,t]
    # print("computeDataHar()->tmp:\n",tmp)
    stopHarvest = np.where(tmp >= 0)
    harMax = np.where(tmp < 0)
    dataHarVec[stopHarvest] = 0
    dataHarVec[harMax] = dataGenVec[harMax]
    # print("dataHar:\n",dataHarVec)
    return dataHarVec
def computeDataHarWithSingleFlowQ(dataQ,enQ,flowQ,batterCapacity,t):
    dataGenVec = np.random.uniform(0, 1, (numOfN, 1)) * dataArrival_max
    dataHarVec = np.zeros((numOfN,1))
    tmp = P_H * (batterCapacity -enQ[:,t]) + dataQ[:,t] - flowQ[t]
    # print("computeDataHar()->tmp:\n",tmp)
    stopHarvest = np.where(tmp >= 0)
    harMax = np.where(tmp < 0)
    dataHarVec[stopHarvest] = 0
    dataHarVec[harMax] = dataGenVec[harMax]
    # print("dataHar:\n",dataHarVec)
    return dataHarVec

def computeTransRecv(caResults,links,dist,chCapacity,dataQ,t):
    # 对应位置元素相乘，计算链路流量
    # print("CA:",caResults)
    # print("CHCAP:",chCapacity)
    tmp = caResults * chCapacity
    # print("tmp:",tmp)
    chOfLink = np.sum
    dataTransVec  = np.zeros(numOfN)
    dataRecvVec = np.zeros_like(dataTransVec)
    for m in range(numOfL):
        Fe  = links[m,0]
        De = links[m,1]
        if (np.sum(tmp[m,:])) > 0:
            for k in range(numOfCH):
                if (tmp[m,k] > 0):
                    val = 0
                    if (tmp[m,k] >= dataQ[Fe,t]):
                        val = dataQ[Fe,t]
                    else:
                        val = tmp[m,k]
                    if Fe != 0:
                        dataTransVec[Fe] = val
                    if De != 0:
                        dataRecvVec[De] = val
    return dataTransVec,dataRecvVec

def computeDrop(virtualQ,dataQ,dataTransVec,weight,dropMax,t):
    dataDropVec = np.zeros((numOfN,1))
    for n in range(numOfN):
        tmp = weight * beta * maxSlop - virtualQ[n, t] - dataQ[n,t]
        if tmp > 0 :
            dataDropVec[n] = 0
        else:
            if dataQ[n,t] - dataTransVec[n] > dataArrival_max:
                dataDropVec[n] = dataArrival_max
            else:
                dataDropVec[n] = dataQ[n,t] - dataTransVec[n]
    return dataDropVec

def updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t):
    dataHarVec = dataHarVec.reshape(dataQ[:, t].shape)
    dataTransVec = dataTransVec.reshape(dataQ[:, t].shape)
    dataDropVec = dataDropVec.reshape(dataQ[:, t].shape)
    dataRecvVec = dataRecvVec.reshape(dataQ[:, t].shape)
    dataQ[:,t+1] = dataQ[:,t] - dataTransVec - dataDropVec + dataRecvVec + dataHarVec
    dataQ[0,t+1] = 0



