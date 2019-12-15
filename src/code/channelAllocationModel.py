# _*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:42

import numpy as np
from code.config import *
from code.Graph import Graph
from math import inf


def chooseMaxWeighted(wEdgeDegree):
    # 选择权重/degree最大的链路
    idx = np.where(wEdgeDegree == np.max(wEdgeDegree))
    choosen = idx[0][0]
    return choosen


def chooseRandom(wEdgeDegree):
    # 随机选择可分配链路
    nozeros = np.where(wEdgeDegree > 0)[0]
    choosen = 0
    # print(nozeros)
    if len(nozeros) > 0:
        m = np.random.randint(0, len(nozeros))
        choosen = nozeros[m]
    return choosen


def weightK_MWIS(enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, k,t):
    wEdge = np.zeros((numOfL))
    for m in range(numOfL):
        Fe = links[m, 0]
        De = links[m, 1]
        wEdge[m] = -(chCap[m, k] * (dataQ[De, t] - dataQ[Fe, t] - virtualQ[Fe, t]) \
                     + P_R[m, 0] * (batterCapacity - enQ[De, t]) + P_T * (batterCapacity - enQ[Fe, t]))
    return wEdge

def weightMaxBackLog(enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, k,t):
    wEdge = np.zeros((numOfL))
    for m in range(numOfL):
        Fe = links[m, 0]
        De = links[m, 1]
        wEdge[m] = dataQ[Fe, t]
        if (enQ[Fe, t] < P_max or enQ[De, t] < P_max):
            wEdge[m] = 0
    return wEdge

def weightMaxEnergy(enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, k,t):
    # print("max Energy!")
    wEdge = np.zeros((numOfL))
    for m in range(numOfL):
        Fe = links[m, 0]
        De = links[m, 1]
        wEdge[m] = enQ[Fe, t]
        if (enQ[Fe, t] < P_max or enQ[De, t] < P_max):
            wEdge[m] = 0

    return wEdge

def findMWIS(Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max,k,alg,caResults, t):
    # 计算每条链路的权重
    # 原问题为最小化，取相反数后求最大值
    wEdge = np.zeros((numOfL))
    if chState[k][0] != 0:
        # print(weightMethod[alg])
        wEdge = weightMethod[alg](enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max, k, t)
        # 权重小于 0的结点将不被分配信道
        wEdge = np.where(wEdge < 0, 0, wEdge)
        V = np.ones(numOfL, dtype=np.int8)
        # 将已经分配信道的链路权重置零
        hasAllocated = np.where(np.sum(caResults[:, 0:k], 1) == 1)
        V[hasAllocated] = 0
        wEdge[hasAllocated] = 0
        # 为信道 k 初始化带权图
        G = Graph(V.copy(), Edge.copy(), wEdge.copy())
        wEdgeDegree = G.wEdge
        while (np.size(G.V) > 0 and np.sum(wEdgeDegree) > 0):
            linkHasNoConflict = np.where(G.dList == 0)
            linkWithConflict = np.where(G.dList > 0)
            hasDeleted = np.where(G.V == 0)
            # 如果当前结点度为0，不存在冲突，直接为其分配信道 k
            wEdgeDegree[linkHasNoConflict] = inf
            wEdgeDegree[linkWithConflict] = wEdge[linkWithConflict] / (G.dList[linkWithConflict] + 1)
            wEdgeDegree[hasDeleted] = 0
            # 为wEdgeDegree中权重最大的结点分配信道 k
            choosen = chooseMethod[alg](wEdgeDegree)
            if np.max(wEdgeDegree) != 0:
                # 为链路 choosen 分配信道 k
                caResults[choosen, k] = 1
                # 删除结点 choosen 以及与其邻接的所有结点
                G.coloring(choosen)

def channelAllocation(Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max,alg, t):
    caResults = np.zeros((numOfL, numOfCH), dtype=np.int8)
    for k in range(numOfCH):
        if chState[k][0] != 0:
            findMWIS(Edge, enQ, dataQ, virtualQ, links, chCap, batterCapacity, P_R, chState, P_max,k,alg, caResults,t)
        else:
            # print("t:",t,"信道",k,"不可用")
            pass
    return caResults

chooseMethod = {"kmwis": chooseMaxWeighted,  "random": chooseRandom,"delay":chooseMaxWeighted,"greedy":chooseMaxWeighted}
weightMethod = {"kmwis":weightK_MWIS,"random":weightK_MWIS,"delay":weightMaxBackLog,"greedy":weightMaxEnergy}
