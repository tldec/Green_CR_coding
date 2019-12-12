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
from code.flowQModel import *
import matplotlib.pyplot as plt

# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
# 结点流队列
flowQ = np.zeros_like(enQ)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((timeSlots))
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
flowQ_max = np.zeros_like(enQ_max)
# 数据丢弃上限
dropMax = np.zeros(len(epsilons))

# 信道可接入概率
# 主用户信道状态集 0 表示不可用 1 表示可用
access = [0, 1]
# 主用户可接入概率
p = [0.4, 0.6]
P_R = para/distOfLink
def main():
    chMax = np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise)/1000
    dataQ_max = weights * maxSlop + 2*dataArrival_max + chMax
    virtualQ_max = weights * maxSlop * beta + epsilons
    flowQ_max = weights * maxSlop  + dataArrival_max
    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        dropMax[e] = max(epsilon,(dataArrival_max + chMax))
    W_1 = (chMax/P_T)*(weights * beta * maxSlop + epsilons + weights * maxSlop + chMax+2*dataArrival_max)
    W_2 = (1/ P_H) * (weights  * maxSlop + dataArrival_max+chMax)
    enQ_max = np.where(W_1 > W_2, W_1, W_2)

    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        for w in range((len(weights))):
            weight = weights[w]
            for n in range(numOfN):
                enQ[n, 0] = enQ_max[w]*0.75
            for t in range(timeSlots-1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity =(weight/1000)* np.log2(1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                                                ((distOfLink ** 2) * noise)) * chState.T
                # print(channelCapacity)

                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T
                # computeDataHar(dataQ, enQ, flowQ, batterCapacity, t):
                dataHarVec = computeDataHar(dataQ,enQ,flowQ,enQ_max[w],t)
                # print("dataHarVec:\n",dataHarVec)
                # print("Edge:",Edge)
                caResults = channelAllocation(Edge,enQ,dataQ,virtualQ,link,channelCapacity,enQ_max[w],P_R,chState,t)
                # if (np.sum(caResults) >0):
                #     print("t",t,"caResult:\n",caResults)
                # else:
                #     print("t", t)
                # print("chCap:",channelCapacity)
                # print("CA:",caResults)
                dataTransVec,dataRecvVec = computeTransRecv(caResults,link,dist,channelCapacity,dataQ,t)
                # print("dataTransVec:",dataTransVec)
                # print("dataRecvVec:",dataRecvVec)
                dataDropVec = computeDrop(virtualQ,dataQ,dataTransVec,weight,dropMax[e],t)
                enConVec = computeEnConsumption(caResults,link,distOfLink,dataHarVec)
                flowInVec = computeFlowInput(weight,flowQ,t)
                updateFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max[w],t)
                updateEnQ(enQ,enHarVec,enConVec,enQ_max[w],t)
                updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t)
                updateVirtualQ(virtualQ,dataQ,epsilon,dataTransVec,dataDropVec,chMax,t)
                # print("np.sum(dataHarVec[1:]:",np.sum(dataHarVec[1:]))
                utility[t] = np.log(1+np.sum(dataHarVec[1:]))-weight*beta*maxSlop*np.sum(dataDropVec[1:])
                aveUtility[w] = np.sum(utility)/timeSlots
                print("e",epsilon,"w",weight,"t",t)
                # print()
    # print("enQ_max",enQ_max)
    plt.plot(range(timeSlots),enQ[2],color='red')
    plt.legend(title="Ent")
    plt.show()
    plt.plot(range(timeSlots), dataQ[2], color='blue')
    plt.legend(title="Dnt")
    plt.show()
    plt.plot(range(timeSlots), virtualQ[2], color='blue')
    plt.legend(title="VQnt")
    plt.show()
    plt.plot(weights, aveUtility, color='green')
    plt.legend(title="utility")
    plt.show()
    # plt.plot(range(timeSlots), flowQ[2], color='blue')
    # plt.legend(title="FQnt")
    # plt.show()
if '__main__' == __name__:
    main()






