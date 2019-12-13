# _*_coding:utf-8_*_
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
enQMaxBklog = np.zeros((numOfN, timeSlots))
enQRA = np.zeros((numOfN, timeSlots, len(epsilons)))
enQw = np.zeros((numOfN, timeSlots,len(weights)))
# 初始化结点数据队列
dataQ = np.zeros_like(enQ)
dataQRA = np.zeros_like(enQRA)
dataQMaxBklog = np.zeros_like(enQRA)
dataQw = np.zeros_like(enQw)
# 初始化结点虚拟队列
virtualQ = np.zeros_like(enQ)
virtualQRA = np.zeros((numOfN, timeSlots, len(epsilons)))
virtualQMaxBklog = np.zeros((numOfN, timeSlots, len(epsilons)))
virtualQw = np.zeros_like(enQw)
# 结点流队列
flowQ = np.zeros((timeSlots))
flowQRA = np.zeros((timeSlots))
flowQMaxBklog = np.zeros((timeSlots))
# flowQMaxBklog = np.zeros((timeSlots))
flowQw = np.zeros((timeSlots,len(weights)))

# 初始化每个结点的网络效益
# sum_{n:N} f(h_n - d_n)
utility = np.zeros((numOfN, timeSlots))
# 平均网络效益-权重
aveUtility = np.zeros((len(weights), 3))
# 记录每个时隙结点发送的数据
dataTransM = np.zeros((numOfN, timeSlots))
# 记录每个时隙结点接收的数据
dataRecvM = np.zeros_like(dataTransM)
# 记录每个结点收集的数据
dataHarM = np.zeros_like(dataTransM)
dataHarMRA = np.zeros_like(dataTransM)
dataHarMMaxBklog = np.zeros_like(dataTransM)

# 记录每个结点丢弃的数据
dataDropM = np.zeros_like(dataTransM)
dataDropMRA = np.zeros_like(dataTransM)
dataDropMMaxBklog = np.zeros_like(dataTransM)

# 记录每个结点采集的能量
enHarM = np.zeros_like(dataTransM)
# 记录每个结点消耗的能量
enConM = np.zeros_like(dataTransM)
# 记录信道分配结果
caResultM = np.zeros((numOfL, numOfCH, timeSlots))
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
P_R = para / distOfLink


def saveRandomUtility(utilityRandom):
    np.savetxt('E:\\utilityRandom.csv', utilityRandom, delimiter=',')


def saveRandomCA(saveRandomUtility):
    np.savetxt('E:\\utilityRandom.csv', saveRandomUtility, delimiter=',')


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


def main():
    chMax = bandWidth * np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise) / 1000
    print("chMax", chMax)
    colorList = []
    for e in range(len(epsilons)):
        colorList.append(randomcolor())
    flowQ_max = weights * maxSlop + dataArrival_max
    # for e in range(len(epsilons)):
    #     epsilon = epsilons[e]
    #     dropMax[e] = max(epsilon,(dataArrival_max + chMax))
    # W_1 = (chMax/P_T)*(weights * beta * maxSlop + epsilons + weights * maxSlop + chMax+2*dataArrival_max)
    # W_2 = (1/ P_H) * (weights  * maxSlop + dataArrival_max+chMax)
    # enQ_max = np.where(W_1 > W_2, W_1, W_2)

    for e in range(len(epsilons)):
        epsilon = epsilons[e]
        dropMax[e] = max(epsilon, (dataArrival_max + chMax))
        W_1 = (chMax / P_T) * (weights * beta * maxSlop + epsilons[e] + weights * maxSlop + chMax + 2 * dataArrival_max)
        W_2 = (1 / P_H) * (weights * maxSlop + dataArrival_max + chMax)
        enQ_max = np.where(W_1 > W_2, W_1, W_2)
        for w in range((len(weights))):
            weight = weights[w]
            dataQ_max = weight * maxSlop + 2* dataArrival_max + chMax
            for n in range(numOfN):
                enQ[n, 0] = enQ_max[w] * initCapacityRate
                enQRA[n, 0] = enQ_max[w] * initCapacityRate
                enQMaxBklog[n, 0] = enQ_max[w] * initCapacityRate
            for t in range(timeSlots - 1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity = bandWidth * (weight / 1000) * np.log2(
                    1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                    ((distOfLink ** 2) * noise)) * chState.T
                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarVecRA = computeEnHar(enQRA, enQ_max[w], t)
                enHarVecMaxBklog = computeEnHar(enQRA, enQ_max[w], t)
                enHarM[:, t] = enHarVecMaxBklog.T
                dataHarVec = computeDataHarWithSingleFlowQ(dataQ, enQ, flowQ, enQ_max[w], t)
                dataHarVecRA = computeDataHarWithSingleFlowQ(dataQRA, enQRA, flowQRA, enQ_max[w], t)
                dataHarVecMaxBklog = computeDataHarWithSingleFlowQ(dataQMaxBklog, enQMaxBklog, flowQMaxBklog, enQ_max[w], t)
                dataHarM[:, t] = dataHarVec.T
                dataHarMRA[:, t] = dataHarVecRA.T
                dataHarMMaxBklog[:, t] = dataHarVecMaxBklog.T

                caResults = channelAllocation(Edge, enQ, dataQ, virtualQ, link, channelCapacity, enQ_max[w], P_R,
                                                   chState,"KMWIS", t)
                caResultsRA = channelAllocation(Edge, enQRA, dataQRA, virtualQRA, link, channelCapacity,
                                                      enQ_max[w], P_R, chState,"random", t)
                caResultsMaxBklog = channelAllocation(Edge, enQMaxBklog, dataQMaxBklog, virtualQMaxBklog, link, channelCapacity,
                                                      enQ_max[w], P_R, chState,"greedy", t)

                dataTransVec, dataRecvVec = computeTransRecv(caResults, link, dist, channelCapacity, dataQ, t)
                dataTransVecRA, dataRecvVecRA = computeTransRecv(caResultsRA, link, dist, channelCapacity, dataQRA, t)
                dataTransVecMaxBklog, dataRecvVecMaxBklog = computeTransRecv(caResultsMaxBklog, link, dist, channelCapacity, dataQMaxBklog, t)
                dataDropVec = computeDrop(virtualQ, dataQ, dataTransVec, weight, dropMax[e], t)
                dataDropVecRA = computeDrop(virtualQRA, dataQRA, dataTransVecRA, weight, dropMax[e], t)
                dataDropVecMaxBklog = computeDropRandom(virtualQMaxBklog, dataQMaxBklog, dataTransVecMaxBklog, weight, dropMax[e], t)
                dataDropM[:, t] = dataDropVec.T
                dataDropMRA[:, t] = dataDropVecRA.T
                dataDropMMaxBklog[:, t] = dataDropVecMaxBklog.T

                enConVec = computeEnConsumption(caResults, link, distOfLink, dataHarVec)
                enConVecRA = computeEnConsumption(caResultsRA, link, distOfLink, dataHarVecRA)
                enConVecMaxBklog = computeEnConsumption(caResultsMaxBklog, link, distOfLink, dataHarVecMaxBklog)

                flowInVec = computeFlowInputWithSingleFlowQ(weight, flowQ, t)
                flowInVecRA = computeFlowInputWithSingleFlowQ(weight, flowQRA, t)
                flowInVecMaxBklog = computeFlowInputWithSingleFlowQ(weight, flowQMaxBklog, t)

                updateFlowQWithSigleFlowQ(flowQ, flowInVec, dataHarVec, flowQ_max[w], t)
                updateFlowQWithSigleFlowQ(flowQRA, flowInVecRA, dataHarVecRA, flowQ_max[w], t)
                updateFlowQWithSigleFlowQ(flowQMaxBklog, flowInVecMaxBklog, dataHarVecMaxBklog, flowQ_max[w], t)
                # print("dataHarRA:",dataHarVecRA)
                # print("dataHar:", dataHarVec)
                updateEnQ(enQ, enHarVec, enConVec, enQ_max[w], t)
                updateEnQ(enQRA, enHarVecRA, enConVecRA, enQ_max[w], t)
                updateEnQ(enQMaxBklog, enHarVecMaxBklog, enConVecMaxBklog, enQ_max[w], t)
                updateDataQ(dataQ, dataHarVec, dataTransVec, dataRecvVec, dataDropVec, t)
                updateDataQ(dataQRA, dataHarVecRA, dataTransVecRA, dataRecvVecRA, dataDropVecRA, t)
                updateDataQ(dataQMaxBklog, dataHarVecMaxBklog, dataTransVecMaxBklog, dataRecvVecMaxBklog, dataDropVecMaxBklog, t)
                updateVirtualQ(virtualQ, dataQ, epsilon, dataTransVec, dataDropVec, chMax, t)
                updateVirtualQ(virtualQRA, dataQRA, epsilon, dataTransVecRA, dataDropVecRA, chMax, t)
                updateVirtualQ(virtualQMaxBklog, dataQMaxBklog, epsilon, dataTransVecMaxBklog, dataDropVecMaxBklog, chMax, t)
            aveHar = np.average(dataHarM[1:, :], axis=1)
            aveHarRA = np.average(dataHarMRA[1:, :], axis=1)
            aveHarMaxBklog = np.average(dataHarMMaxBklog[1:, :], axis=1)
            aveDrop = np.average(dataDropM[1:, :], axis=1)
            aveDropRA = np.average(dataDropMRA[1:, :], axis=1)
            aveDropMaxBklog = np.average(dataDropMMaxBklog[1:, :], axis=1)
            # print("aveHar",aveHar)
            # print("aveDrop", aveDrop)
            aveUtility[w, 0] = np.sum(np.log(1 + aveHar - aveDrop))
            aveUtility[w, 1] = np.sum(np.log(1 + aveHarRA - aveDropRA))
            aveUtility[w, 2] = np.sum(np.log(1 + aveHarMaxBklog - aveDropMaxBklog))
            enQw[:,:,w] = enQ
            dataQw[:,:,w] = dataQ
            # 只使用一个流队列
            virtualQw[:,:,w] = virtualQ
            flowQw[:,w] = flowQ.reshape((flowQw[:,w].shape))
            # print("aveHarRA",aveHarRA,"aveDropRA", aveDropRA)
            # print("aveDrop", aveDropRA)
            print("w = ", weights[w], "CA :", aveUtility[w][0], "RA :",aveUtility[w][1],"MaxBklog :",aveUtility[w][2])
    np.savetxt('E:\\utilityCompare.csv', aveUtility, delimiter=',')
    plotPoleUtility(aveUtility)
    plotQ()

def plotLineUtility(utilityVal):
    s = "Utility-V compare "
    plt.title(s)
    # print(aveUtility)
    plt.xlabel("Value of Weights")
    plt.ylabel("Value of Utility")
    plt.plot(weights, aveUtility[:, 0], c=randomcolor(), linestyle='-', marker='s', label="K-MWIS")
    plt.plot(weights, aveUtility[:, 1], c=randomcolor(), linestyle='-', marker='o', label="Random Algrithm")
    plt.legend()
    plt.show()

def plotPoleUtility(utilityVal):
    bar_width = 12
    # X 轴 变量
    # x1 = np.array(range(len(weights)))
    x1 = weights -13
    plt.bar(x=x1, height=utilityVal[:, 0], label='K-MWIS',
            color='blue', alpha=0.8, width=bar_width)
    x2 = x1  +13
    plt.bar(x=x2, height=utilityVal[:, 1], label='Random Algrithm',
            color='red', alpha=0.8, width=bar_width)
    x3 = x2 + 13
    plt.bar(x=x3, height=utilityVal[:, 2], label='Delay-Sensitive',
            color='gray', alpha=0.8, width=bar_width)
    plt.title("Utility Comparation Under Different Algrithm")
    plt.xlim(10,480)
    plt.xlabel("Value of Weights")
    plt.ylabel("Value of Utility")
    # 显示图例
    plt.legend()
    plt.show()

def plotQ():
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
if '__main__' == __name__:
    U = np.loadtxt('E:\\utilityCompare.csv',delimiter=',')
    plotPoleUtility(U)
    # main()

