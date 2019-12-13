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
enQRA = np.zeros((numOfN,timeSlots,len(epsilons)))
dataQRA = np.zeros_like(enQRA)
virtualQRA = np.zeros((numOfN,timeSlots,len(epsilons)))
flowQ = np.zeros((timeSlots))
# flowQ = np.zeros_like((enQ))
flowQRA = np.zeros((timeSlots))
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
aveUtility = np.zeros((len(weights),2))
# 记录每个时隙结点发送的数据
dataTransM = np.zeros((numOfN, timeSlots))
# 记录每个时隙结点接收的数据
dataRecvM = np.zeros_like(dataTransM)
# 记录每个结点收集的数据
dataHarM = np.zeros_like(dataTransM)
# 记录每个结点丢弃的数据
dataDropM = np.zeros_like(dataTransM)
dataHarMRA = np.zeros_like(dataTransM)
# 记录每个结点丢弃的数据
dataDropMRA = np.zeros_like(dataTransM)
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
    chMax = bandWidth*np.log2(1 + P_T * 1.5) / ((minDist ** 2) * noise)/1000
    print("chMax",chMax)
    colorList = []
    for e in range(len(epsilons)):
        colorList.append(randomcolor())
    flowQ_max = weights * maxSlop  + dataArrival_max
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
            for n in range(numOfN):
                enQ[n, 0] = enQ_max[w]*initCapacityRate
                enQRA[n,0] = enQ_max[w]*initCapacityRate
            for t in range(timeSlots-1):
                chState = np.random.choice(access, (numOfCH, 1), p)
                channelCapacity =bandWidth*(weight/1000)* np.log2(1 + P_T * (np.random.rand(numOfL, numOfCH) + 0.5) / \
                                                ((distOfLink ** 2) * noise)) * chState.T
                enHarVec = computeEnHar(enQ, enQ_max[w], t)
                enHarVecRA = computeEnHar(enQRA, enQ_max[w], t)
                enHarM[:, t] = enHarVec.T

                dataHarVec = computeDataHarWithSingleFlowQ(dataQ,enQ,flowQ,enQ_max[w],t)
                dataHarVecRA = computeDataHarWithSingleFlowQ(dataQRA,enQRA,flowQRA,enQ_max[w],t)
                dataHarM[:,t] = dataHarVec.T
                dataHarMRA[:,t] = dataHarVecRA.T

                caResults = channelAllocation(Edge,enQ,dataQ,virtualQ,link,channelCapacity,enQ_max[w],P_R,chState,t)
                caResultsRA = channelAllocationRandom(Edge,enQRA,dataQRA,virtualQRA,link,channelCapacity,enQ_max[w],P_R,chState,t)

                dataTransVec,dataRecvVec = computeTransRecv(caResults,link,dist,channelCapacity,dataQ,t)
                dataTransVecRA, dataRecvVecRA = computeTransRecv(caResultsRA, link, dist, channelCapacity, dataQRA, t)

                dataDropVec = computeDrop(virtualQ,dataQ,dataTransVec,weight,dropMax[e],t)
                dataDropVecRA = computeDrop(virtualQRA,dataQRA,dataTransVecRA,weight,dropMax[e],t)
                dataDropM[:,t] = dataDropVec.T
                dataDropMRA[:,t] = dataDropVecRA.T

                enConVec = computeEnConsumption(caResults,link,distOfLink,dataHarVec)
                enConVecRA = computeEnConsumption(caResultsRA,link,distOfLink,dataHarVecRA)

                flowInVec = computeFlowInputWithSingleFlowQ(weight, flowQ, t)
                flowInVecRA = computeFlowInputWithSingleFlowQ(weight, flowQRA, t)

                updateFlowQWithSigleFlowQ(flowQ,flowInVec,dataHarVec,flowQ_max[w],t)
                updateFlowQWithSigleFlowQ(flowQRA,flowInVecRA,dataHarVecRA,flowQ_max[w],t)
                # print("dataHarRA:",dataHarVecRA)
                # print("dataHar:", dataHarVec)
                updateEnQ(enQ,enHarVec,enConVec,enQ_max[w],t)
                updateEnQ(enQRA,enHarVecRA,enConVecRA,enQ_max[w],t)
                updateDataQ(dataQ,dataHarVec,dataTransVec,dataRecvVec,dataDropVec,t)
                updateDataQ(dataQRA,dataHarVecRA,dataTransVecRA,dataRecvVecRA,dataDropVecRA,t)
                updateVirtualQ(virtualQ,dataQ,epsilon,dataTransVec,dataDropVec,chMax,t)
                updateVirtualQ(virtualQRA,dataQRA,epsilon,dataTransVecRA,dataDropVecRA,chMax,t)
            aveHar = np.average(dataHarM[1:,:],axis=1)
            aveHarRA = np.average(dataHarMRA[1:,:],axis=1)
            aveDrop = np.average(dataDropM[1:, :], axis=1)
            aveDropRA = np.average(dataDropMRA[1:, :], axis=1)
            # print("aveHar",aveHar)
            # print("aveDrop", aveDrop)
            aveUtility[w,0] = np.sum(np.log(1+aveHar - aveDrop))
            aveUtility[w,1] = np.sum(np.log(1+aveHarRA - aveDropRA))
            # enQw[:,:,e] = enQ
            # dataQe[:,:,e] = dataQ
            # 只使用一个流队列
            # flowQw[:,w] = flowQ.reshape((flowQw[:,w].shape))
            # virtualQe[:,:,e] = virtualQ
            # print("aveHarRA",aveHarRA,"aveDropRA", aveDropRA)
            # print("aveDrop", aveDropRA)
            print("CA w = ",weights[w],"aveUtility =",aveUtility[w][0],"RA w = ",weights[w],"aveUtility =",aveUtility[w][1])
    np.savetxt('E:\\utilityCompare.csv', aveUtility, delimiter=',')


    # # 数据队列与epsilon
    # for e in range(len(epsilons)):
    #     plt.title('Data Queue')
    #     s = "{0} {1}".format("e = ", epsilons[e])
    #     plt.plot(range(timeSlots), dataQRA[10,:,e], c=colorList[e], label=s)
    #     plt.legend()  # 显示图例
    # plt.show()
    # # 虚拟队列与epsilon
    # for e in range(len(epsilons)):
    #     plt.title('Virtual Queue')
    #     s = "{0} {1}".format("e = ", epsilons[e])
    #     # s = "V = %d." % (weights[w])
    #     plt.plot(range(timeSlots), virtualQRA[10,:,e], c=colorList[e], label=s)
    #     plt.legend()  # 显示图例
    # plt.show()
    # # 共用一个流队列
    # for w in range(len(weights)):
    #     plt.title('Flow Queue')
    #     s = "{0} {1}".format("V = ", weights[w])
    #     plt.plot(range(timeSlots), flowQRA[:,w], c=randomcolor(), label=s)
    #     plt.legend()  # 显示图例
    # plt.show()
    s = "Utility-V compare "
    plt.title(s)
    # print(aveUtility)
    plt.xlabel("Value of Weights")
    plt.ylabel("Value of Utility")
    plt.plot(weights, aveUtility[:,0], c=randomcolor(),linestyle = '-', marker = 's',label="K-MWIS")
    plt.plot(weights, aveUtility[:, 1], c=randomcolor(), linestyle='-', marker='o', label="Random Algrithm")
    plt.legend()
    plt.show()
def plotUtility(utilityVal):
    bar_width = 0.3
    x1 = np.array(range(len(weights)))
    x2 = np.array(range(len(weights))) + bar_width
    plt.bar(x=x1, height=utilityVal[:, 0], label='K-MWIS',
            color='blue', alpha=0.8, width=bar_width)
    plt.bar(x=x2 , height=utilityVal[:, 1], label='Random Algrithm',
            color='red', alpha=0.8, width=bar_width)
    plt.title("Utility Comparation Under Different Algrithm")

    # 将X轴数据改为使用np.arange(len(x_data))+bar_width,
    # 就是bar_width、1+bar_width、2+bar_width...这样就和第一个柱状图并列了

    # 为两条坐标轴设置名称
    plt.xlabel("Value of Weights")
    plt.ylabel("Value of Utility")
    # 显示图例
    plt.legend()
    plt.show()
if '__main__' == __name__:
    # main()
    U = np.loadtxt('E:\\utilityCompare.csv',delimiter=',')
    plotUtility(U)






