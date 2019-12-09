#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:43
import numpy as np
from code.config import *
from math import inf
def computeDataHar(dataQ,enQ,batterCapacity,t):
    dataHarVec = np.zeros((numOfN,1))
    for n in range(numOfN):
        if (n!=0):
            tmp = (dataQ[n,t]-(batterCapacity))*P_H
            if tmp == 0:
                dataHarVec[n] = 0

            elif (tmp-1)>dataArrival_max:
                dataHarVec[n] = dataArrival_max
            else:
                dataHarVec[n] = tmp -1
    return dataHarVec

def computeTransRecv(caResults,links,dist,chCapacity):
    # 对应位置元素相乘，计算链路流量
    tmp = caResults * chCapacity
    dataTransVec  = np.zeros(numOfN)
    dataRecvVec = np.zeros_like(dataTransVec)
    for m in range(numOfL):
        Fe  = links[m,0]
        De = links[m,1]
        if (np.sum(tmp[m,:])) > 0:
            for k in range(numOfCH):
                if (tmp[m,k] > 0):
                    if Fe != 0:
                        dataTransVec[Fe] = tmp[m,k]
                    if De != 0:
                        dataRecvVec[De] = tmp[m,k]
    return dataTransVec,dataRecvVec

def computeDrop(virtualQ,dataQ,weight,dropMax,t):
    dataDropVec = np.zeros(numOfN)
    for n in range(numOfN):
        if (n!=0):
            if weight * beta * maxSlop > virtualQ[n, t] + dataQ[n, t]:
                dataDropVec[n] = 0
            else:
                dataDropVec[n] = dropMax
    return dataDropVec

def updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t):
    dataQ[:,t+1] = dataQ[:,t] - dataTransVec.T - dataDropVec.T + dataRecvVec.T + dataHarVec.T
    dataQ[0,t+1] = 0



