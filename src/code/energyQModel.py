#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:41
import numpy as np
from code.config import *
def computeEnHar(enQ,batterCapacity,t):
    enGenVec = np.random.uniform(0, 1, (numOfN, 1)) * EH_max * tau
    enHarVec = np.zeros_like(enGenVec)
    tmp = (batterCapacity - enQ[:,t]).reshape(numOfN,1) - enGenVec
    harMax = np.where(tmp <0)
    harRest = np.where(tmp >=0)
    enHarVec[harMax] = enGenVec[harMax]
    enHarVec[harRest] = tmp[harRest]
    # for i in range(numOfN):
    #     # 从环境中获取的能量 超过剩余电池空间
    #     if enGenVec[i] + enQ[i, t] > batterCapacity:
    #         enHarVec[i] = max(batterCapacity - enQ[i, t], 0)
    #     else:
    #         enHarVec[i] = enGenVec[i]
    return enHarVec

def updateEnQ(enQ,enHarVec,enConVec,batterCapacity,t):
    enQ[:,t+1] = enQ[:,t].T -enConVec.T + enHarVec.T
    enQ[0,t+1] = batterCapacity

def computeEnConsumption(caResult,links,dist,dataHarVec):
    enConsVec = np.zeros((numOfN,1))
    for m in range(numOfL):
        Fe = links[m, 0]
        De = links[m, 1]
        if (np.sum(caResult[m,:])) == 1:
            for k in range(numOfCH):
                if (caResult[m,k] == 1):
                    enConsVec[Fe] = P_T + P_H * dataHarVec[m]
                    enConsVec[De] = para/dist[m] + P_H* dataHarVec[m]
                else:
                    enConsVec[Fe] =  P_H * dataHarVec[m]
                    enConsVec[De] =  P_H * dataHarVec[m]
    return enConsVec



