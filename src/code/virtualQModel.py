#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:43
import numpy as np
from code.config import *
def updateVirtualQ(virtualQ,dataQ,epsilon,dataTransVec,dataDropVec,chMax,t):
    for n in range(numOfN):
        if (n != 0):
            if (dataQ[n,t] >0):
                virtualQ[n,t+1] = max(virtualQ[n,t] + epsilon - dataTransVec[n] - dataDropVec[n],0)
            else:
                virtualQ[n, t + 1] = max(virtualQ[n, t] - dataDropVec[n] - chMax, 0)
        else:
            virtualQ[n,t+1] = 0


