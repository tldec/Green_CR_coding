#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/6 20:31
from code.config import *
from math import inf
from code.Graph import Graph
from code.init import *
from code.energyQModel import *
from code.dataQModel import *
from code.virtualQModel import *
from code.channelAllocationModel import *
# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((numOfN, timeSlots))
# 平均网络效益-权重
aveUtility = np.zeros((len(weights)))
# 记录每个时隙结点发送的数据
dataTransM = np.zeros((numOfN, timeSlots))
# 记录每个时隙结点接收的数据
dataRecvM = np.zeros_like(dataTransM)
# 记录每个结点收集的数据
dataHarM = np.zeros_like(dataTransM)
# 记录每个结点丢弃的数据
dataDropM = np.zeros_like(dataTransM)
# 记录每个结点采集的能量
enHarM = np.zeros_like(dataTransM)
# 记录每个结点消耗的能量
enConM = np.zeros_like(dataTransM)
# 记录信道分配结果
caResultM = np.zeros((numOfL,numOfCH,timeSlots))
# 能量队列上界
enQ_max = np.zeros(len(weights))
# 数据队列上界
dataQ_max = np.zeros_like(enQ_max)
# 虚拟队列上界
virtualQ_max = np.zeros_like(enQ_max)
# 数据丢弃上限
dropMax = np.zeros(len(epsilons))

# 信道可接入概率
# 主用户信道状态集 0 表示不可用 1 表示可用
access = [0, 1]
# 主用户可接入概率
p = [0.4, 0.6]
P_R = para/distOfLink
def main():
    chMax = np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise)
    dataQ_max = weights * maxSlop + dataArrival_max + chMax
    virtualQ_max = weights * maxSlop * beta + epsilons
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        dropMax[e] = max(epsilon,(dataArrival_max + chMax))
    W_1 = (chMax/P_T)*(weights * beta * maxSlop + epsilons + weights * maxSlop + chMax+dataArrival_max)
    W_2 = (1/ P_H) * (weights  * maxSlop + dataArrival_max+chMax)
    enQ_max = np.where(W_1 > W_2, W_1, W_2)

    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        for w in range((len(weights))):
            weight = weights[w]
            for t in range(timeSlots-1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity =weights* np.log2(1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                                                ((distOfLink ** 2) * noise)) * chState.T
                # print(channelCapacity)
                enHarVec = computeEnHar(enQ, enQ_max, t)
                enHarM[:, t] = enHarVec.T
                dataHarVec = computeDataHar(dataQ,enQ,enQ_max[w],t)
                print("Edge:",Edge)
                caResults = channelAllocation(Edge,enQ,dataQ,virtualQ,link,channelCapacity,enQ_max[w],P_R,t)
                dataTransVec,dataRecvVec = computeTransRecv(caResults,link,dist,channelCapacity)
                dataDropVec = computeDrop(virtualQ,dataQ,weight,dropMax,t)
                enConVec = computeEnConsumption(caResults,link,distOfLink,dataHarVec)
                updateEnQ(enQ,enHarVec,enConVec,enQ_max[w],t)
                updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t)
                updateVirtualQ(virtualQ,dataQ,epsilon,dataTransVec,dataDropVec,chMax,t)
                utility[t] = np.log(1+np.sum(dataHarVec[1:])-np.sum(dataDropVec[1:]))
                aveUtility[w] = np.sum(utility)/timeSlots
if '__main__' == __name__:
    main()





