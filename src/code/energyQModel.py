#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:41
import numpy as np
from code.config import *
def computeEnHar(enQ,batterCapacity,t):
    enGenVec = np.random.uniform(0, 1, (numOfN, 1)) * EH_max * tau
    enHarVec = enGenVec.copy()
    for n in range(numOfN):
        restCapacity = batterCapacity - enQ[n,t]
        # print(restCapacity)
        if restCapacity < 0:
            enHarVec[n] = 0
        else:
            enHarVec[n] = min(restCapacity,enGenVec[n])

    # print("enGenVec\n",enGenVec)
    return enHarVec

def updateEnQ(enQ,enHarVec,enConVec,batterCapacity,t):
    enHarVec = enHarVec.reshape(enQ[:,t].shape)
    enConVec = enConVec.reshape(enQ[:,t].shape)
    enQ[:,t+1] = enQ[:,t] -enConVec + enHarVec
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



