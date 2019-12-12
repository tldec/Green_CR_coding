#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:42

import numpy as np
from code.config import *
from code.Graph import Graph
from math import inf

def channelAllocation(Edge,enQ,dataQ,virtualQ,links,chCap,batterCapacity,P_R,chState,t):
    caResults = np.zeros((numOfL,numOfCH),dtype=np.int8)
    # 为每个颜色寻找最大带权独立集
    print("t:",t,"信道容量",chCap)

    for k in range(numOfCH):
        # 计算每条链路的权重
        # 原问题为最小化，取相反数后求最大值
        # print("P_R*(batterCapacity - enQ[De]):",P_R*(batterCapacity - enQ[De]))
        wEdge = np.zeros((numOfL))
        # print("信道",k,"状态：",chState[k][0])
        if chState[k][0] != 0 :
            for m in range(numOfL):
                Fe = links[m,0]
                De = links[m,1]
                # print("P_R:",P_R)
                print("t:",t,"tmp_1:",chCap[m,k] * (dataQ[De,t] - dataQ[Fe,t] - virtualQ[Fe,t]))
                print("t:", t, "tmp_2:", P_R[m,0]*(batterCapacity - enQ[De,t]) + P_T*(batterCapacity - enQ[Fe,t]))
                wEdge[m] = -(chCap[m,k] * (dataQ[De,t] - dataQ[Fe,t] - virtualQ[Fe,t]) \
                           +P_R[m,0]*(batterCapacity - enQ[De,t]) + P_T*(batterCapacity - enQ[Fe,t]))

        print("wEdge:\n",-wEdge)
        # 权重小于 0的结点将不被分配信道
        wEdge = np.where(wEdge < 0, 0, wEdge)
        V = np.ones(numOfL,dtype=np.int8)
        # 将已经分配信道的链路权重置零
        hasAllocated = np.where(np.sum(caResults[:,0:k],1)==1)
        print("已分配信道的链路:\n",hasAllocated[0])
        print("before V=\n",V)
        V[hasAllocated] = 0
        print("after V=\n", V)
        wEdge[hasAllocated] = 0
        # 为信道 k 初始化带权图
        G = Graph(V.copy(), Edge.copy(),wEdge.copy())
        # 每次选择 wEdgeDegree中值最大的结点，为其分配信道k
        wEdgeDegree = G.wEdge
        # 构造初始图
        # print("edge:",G.Edge)
        while(np.size(G.V) > 0 and np.sum(wEdgeDegree) > 0):
            linkHasNoConflict = np.where(G.dList == 0)
            linkWithConflict = np.where(G.dList > 0)
            hasDeleted = np.where(G.V == 0)
            # 如果当前结点度为0，不存在冲突，直接为其分配信道 k
            wEdgeDegree[linkHasNoConflict] = inf
            wEdgeDegree[linkWithConflict] = wEdge[linkWithConflict]/(G.dList[linkWithConflict]+1)
            wEdgeDegree[hasDeleted] = 0
            # 为wEdgeDegree中权重最大的结点分配信道 k
            idx = np.where(wEdgeDegree == np.max(wEdgeDegree))
            choosen = idx[0][0]
            if np.max(wEdgeDegree) != 0:
                print("为链路",choosen,"分配信道",k)
                caResults[choosen,k] = 1
                # 删除结点 choosen 以及与其邻接的所有结点
                # print("更新前:",wEdgeDegree)
                G.coloring(choosen)
                # print("更新后\n", wEdgeDegree)
        else:
            print("t:",t,"信道",k,"不可用")
    return caResults



