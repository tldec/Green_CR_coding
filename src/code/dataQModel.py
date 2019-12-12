#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:43
import numpy as np
from code.config import *
from math import inf
def computeDataHar(dataQ,enQ,flowQ,batterCapacity,t):
    dataHarVec = np.zeros((numOfN,1))
    tmp = P_H * (batterCapacity -enQ[:,t]) + dataQ[:,t] - flowQ[:,t]
    # print("computeDataHar()->tmp:\n",tmp)
    stopHarvest = np.where(tmp > 0)
    harMax = np.where(tmp <= 0)
    dataHarVec[stopHarvest] = 0
    dataHarVec[harMax] = dataArrival_max
    # for n in range(numOfN):
    #     if (n!=0):
    #         tmp = -dataQ[n,t]+(batterCapacity-enQ[n,t])*P_H
    #         harVal = weight/tmp -1
    #         print("harVal =", harVal+1)
    #             # dataHarVec[n] = inf
    #         # print("harVal:",harVal)
    #         if harVal < 0:
    #             dataHarVec[n] = 0
    #         elif harVal < dataArrival_max:
    #             dataHarVec[n] = harVal
    #         else:
    #             dataHarVec[n] = dataArrival_max
    return dataHarVec

def computeTransRecv(caResults,links,dist,chCapacity,dataQ,t):
    # 对应位置元素相乘，计算链路流量
    print("CA:",caResults)
    print("CHCAP:",chCapacity)
    
    tmp = caResults * chCapacity
    print("tmp:",tmp)
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

def computeDrop(virtualQ,dataQ,weight,dropMax,t):
    dataDropVec = np.zeros((numOfN,1))
    tmp = weight * beta * maxSlop - virtualQ[:, t] + dataQ[:,t]

    stopDrop = np.where(tmp > 0)
    drop = np.where(tmp <= 0)
    dataDropVec[stopDrop] = 0
    dataDropVec[drop] = dropMax
    dropAll = np.where(dataQ[:,t]<dropMax)
    dataDropVec[dropAll] = dataQ[:,t].reshape(numOfN,1)[dropAll]
    # for n in range(numOfN):
    #     if (n!=0):
    #         if weight * beta * maxSlop > virtualQ[n, t] + dataQ[n, t]:
    #             dataDropVec[n] = 0
    #         else:
    #             dataDropVec[n] = dropMax
    print("computeDrop()->dataDropVec:\n", dataDropVec)
    return dataDropVec

def updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t):
    dataQ[:,t+1] = dataQ[:,t] - dataTransVec.T - dataDropVec.T + dataRecvVec.T + dataHarVec.T
    dataQ[0,t+1] = 0



