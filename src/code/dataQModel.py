#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:43
import numpy as np
from code.config import *
from math import inf
import numpy as np
from code.config import *
from math import inf
def computeDataHar(dataQ,enQ,batterCapacity,w,t):
    dataGenVec = np.random.uniform(0, 1, (numOfN, 1)) * dataArrival_max
    dataHarVec = np.zeros((numOfN,1))
    for n in range(numOfN):
        tmp = P_H * (batterCapacity - enQ[n,t]) + dataQ[n,t]
        if tmp == 0:
            dataHarVec[n] = dataGenVec[n]
        else:
            har = weights[w]/tmp -1
            if har < 0:
                dataHarVec[n] = 0
            else:
                dataHarVec[n] = min(har,dataArrival_max)
    # print("dataHar:\n",dataHarVec)
    return dataHarVec

def computeTransRecv(caResults,links,dist,chCapacity,dataQ,t):
    # 对应位置元素相乘，计算链路流量
    # print("CA:",caResults)
    # print("CHCAP:",chCapacity)
    tmp = caResults * chCapacity
    # print("tmp:",tmp)
    dataTransVec  = np.zeros(numOfN)
    dataRecvVec = np.zeros_like(dataTransVec)
    for m in range(numOfL):
        Fe  = links[m,0]
        De = links[m,1]
        # 若链路 m 被分配信道
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
            dataDropVec[n] = min(dataQ[n,t] - dataTransVec[n],dropMax)
    return dataDropVec

def updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t):
    dataQ[:,t+1] = dataQ[:,t] - dataTransVec.reshape(dataQ[:,t].shape) - dataDropVec.reshape(dataQ[:,t].shape) \
                   + dataRecvVec.reshape(dataQ[:,t].shape) + dataHarVec.reshape(dataQ[:,t].shape)
    dataQ[0,t+1] = 0
