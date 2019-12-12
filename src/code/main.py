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
import random

# 初始化结点能量队列
enQ = np.zeros((numOfN, timeSlots))
enQw = np.zeros((numOfN,timeSlots,len(weights)))
dataQw = np.zeros_like(enQw)
virtualQw = np.zeros((numOfN,timeSlots,len(weights)))
flowQ = np.zeros((timeSlots))
# flowQ = np.zeros_like((enQ))
flowQw = np.zeros((timeSlots,len(weights)))
# flowW = np.zeros_like(flowQw)
# flowQw = np.zeros((numOfN,timeSlots,len(weights)))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
# 结点流队列
# flowQ = np.zeros_like(enQ)
# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((numOfN,timeSlots))
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

def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color
def main():
    chMax = bandWidth*np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise)/1000
    print("chMax",chMax)
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
                enQ[n, 0] = enQ_max[w]*initCapacityRate
            for t in range(timeSlots-1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity =bandWidth*(weight/1000)* np.log2(1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                                                ((distOfLink ** 2) * noise)) * chState.T
                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T

                dataHarVec = computeDataHarWithSingleFlowQ(dataQ,enQ,flowQ,enQ_max[w],t)
                dataHarM[:,t] = dataHarVec.T
                caResults = channelAllocation(Edge,enQ,dataQ,virtualQ,link,channelCapacity,enQ_max[w],P_R,chState,t)
                dataTransVec,dataRecvVec = computeTransRecv(caResults,link,dist,channelCapacity,dataQ,t)

                dataDropVec = computeDrop(virtualQ,dataQ,dataTransVec,weight,dropMax[e],t)
                dataDropM[:,t] = dataDropVec.T
                enConVec = computeEnConsumption(caResults,link,distOfLink,dataHarVec)
                flowInVec = computeFlowInputWithSingleFlowQ(weight, flowQ, t)
                updateFlowQWithSigleFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max[w],t)
                # print("flowQ:",flowQ)
                updateEnQ(enQ,enHarVec,enConVec,enQ_max[w],t)
                updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t)
                updateVirtualQ(virtualQ,dataQ,epsilon,dataTransVec,dataDropVec,chMax,t)
            aveHar = np.average(dataHarM[1:,:],axis=1)
            aveDrop = np.average(dataDropM[1:, :], axis=1)
            # print("aveHar",aveHar)
            # print("aveDrop", aveDrop)
            aveUtility[w] = np.sum(np.log(epsilon+aveHar - aveDrop))
            enQw[:,:,w] = enQ
            dataQw[:,:,w] = dataQ
            # 只使用一个流队列
            flowQw[:,w] = flowQ.reshape((flowQw[:,w].shape))
            virtualQw[:,:,w] = virtualQ
            print("w =",weight,"aveUtility =",aveUtility[w])
    np.savetxt('E:\\utility.csv', aveUtility, delimiter=',')



    for w in range(len(weights)):
        plt.title('Energy Queue')
        s = "{0} {1}".format("V = ", weights[w])
        plt.plot(range(timeSlots), enQw[10,:,w], c=randomcolor(), label=s)
        plt.legend()  # 显示图例
    plt.show()
    for w in range(len(weights)):
        plt.title('Data Queue')
        s = "{0} {1}".format("V = ", weights[w])
        plt.plot(range(timeSlots), dataQw[10,:,w], c=randomcolor(), label=s)
        plt.legend()  # 显示图例
    plt.show()
    for w in range(len(weights)):
        plt.title('Virtual Queue')
        s = "{0} {1}".format("V = ", weights[w])
        # s = "V = %d." % (weights[w])
        plt.plot(range(timeSlots), virtualQw[10,:,w], c=randomcolor(), label=s)
        plt.legend()  # 显示图例
    plt.show()
    # 共用一个流队列
    for w in range(len(weights)):
        plt.title('Flow Queue')
        s = "{0} {1}".format("V = ", weights[w])
        plt.plot(range(timeSlots), flowQw[:,w], c=randomcolor(), label=s)
        plt.legend()  # 显示图例
    plt.show()
    plt.plot(weights, aveUtility, color='green',linestyle = '-', marker = 's')
    plt.legend(title="utility")
    plt.show()

if '__main__' == __name__:
    main()






