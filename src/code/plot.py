#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/14 19:56
from matplotlib import pyplot as plt
import random
from code.config import *
def __randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color
def plotOverSlot(val,diff,plt_dict):
    # print(plt_dict["title"])
    plt.title(plt_dict["title"])
    for w in range(len(diff)):
        lbl = "{0} = {1}".format(plt_dict["para_name"],diff[w])
        plt.plot(range(timeSlots), val[:,w], c=__randomcolor(),label=lbl)
    plt.xlabel(plt_dict["xlabel"])
    plt.ylabel(plt_dict["ylabel"])
    plt.legend(loc="best")  # 显示图例
    plt.show()

def plotUtilityOverWeights(val,diff,plt_dict):
    if diff == None:
        plt.title(plt_dict['title'])
        plt.plot(weights, val, c=__randomcolor(), linestyle='-', marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
        plt.show()
    else:
        plt.title(plt_dict['title'])
        for w in range(len(diff)):
            # print(val[:,w])
            lbl = "{0}".format(diff[w])
            plt.plot(weights, val[:,w], c=__randomcolor(),label=lbl,linestyle='-',marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
        plt.legend()  # 显示图例
        plt.show()

#
# def plotPoleUtility(utilityVal):
#     utilityVal = np.where(utilityVal < 0, -utilityVal, utilityVal)
#     bar_width = int((weights[len(weights) - 1]) / (len(weights)) / 4)
#     # print(int(bar_width))
#     # X 轴 变量
#     # x1 = np.array(range(len(weights)))
#     x1 = weights - bar_width
#     plt.bar(x=x1, height=utilityVal[:, 0], label='K-MWIS',
#             color='blue', alpha=0.8, width=bar_width)
#     x2 = x1 + bar_width
#     plt.bar(x=x2, height=utilityVal[:, 1], label='Random Algrithm',
#             color='red', alpha=0.8, width=bar_width)
#     x3 = x2 + bar_width
#     plt.bar(x=x3, height=utilityVal[:, 2], label='Delay-Sensitive',
#             color='gray', alpha=0.8, width=bar_width)
#     x4 = x3 + bar_width
#     plt.bar(x=x4, height=utilityVal[:, 3], label='greedy',
#             color='green', alpha=0.8, width=bar_width)
#     plt.title("Utility Comparation Under Different Algrithm")
#     plt.xlim(weights[0] - bar_width, weights[len(weights) - 1] + bar_width)
#     plt.xlabel("Value of Weights")
#     plt.ylabel("Value of Utility")
#     # 显示图例
#     plt.legend()
#     plt.show()

# algList = ["K-MWIS", "Random Allocation", "Delay-Sensitive", "Greedy"]
# def randomcolor():
#     colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
#     color = ""
#     for i in range(6):
#         color += colorArr[random.randint(0, 14)]
#     return "#" + color
#
#
# def plotSunOfTraffic():
#     traffic = np.zeros((timeSlots, len(weights), 4))
#     traffic[:, :, 0] = np.loadtxt('E:\\trafficOverSlot_0.csv', delimiter=',')
#     traffic[:, :, 1] = np.loadtxt('E:\\trafficOverSlot_1.csv', delimiter=',')
#     traffic[:, :, 2] = np.loadtxt('E:\\trafficOverSlot_2.csv', delimiter=',')
#     # traffic[:, :, 3] = np.loadtxt('E:\\trafficOverSlot_3.csv', delimiter=',')
#     # plt.title("Sum of Traffics Under different Alorithm")
#     bar_width = int((weights[len(weights) - 1]) / (len(weights)) / 4)
#     # print(int(bar_width))
#     # X 轴 变量
#     # x1 = np.array(range(len(weights)))
#     totalTraffic = np.zeros((len(weights), 4))
#     for w in range(len(weights)):
#         totalTraffic[w, 0] = np.sum(traffic[:, w, 0])
#         totalTraffic[w, 1] = np.sum(traffic[:, w, 1])
#         totalTraffic[w, 2] = np.sum(traffic[:, w, 2])
#         # totalTraffic[w, 3] = np.sum(traffic[:, w, 3])
#     totalTraffic = totalTraffic
#     x1 = weights - bar_width
#     plt.bar(x=x1, height=totalTraffic[:, 0], label='K-MWIS',
#             color='blue', alpha=0.8, width=bar_width)
#     x2 = x1 + bar_width
#     plt.bar(x=x2, height=totalTraffic[:, 1], label='Random Algrithm',
#             color='red', alpha=0.8, width=bar_width)
#     x3 = x2 + bar_width
#     plt.bar(x=x3, height=totalTraffic[:, 2], label='Delay-Sensitive',
#             color='gray', alpha=0.8, width=bar_width)
#     x4 = x3 + bar_width
#     plt.bar(x=x4, height=totalTraffic[:, 3], label='greedy',
#             color='green', alpha=0.8, width=bar_width)
#     plt.title("Sum of Traffics Under Different Algrithm")
#     plt.xlim(weights[0] - bar_width, weights[len(weights) - 1] + bar_width)
#     plt.xlabel("Value of Weights")
#     plt.ylabel("Sum of Traffics")
#
#     plt.legend()
#     plt.show()
#
#
# def plotNumOfCA(alg):
#     numCA = np.zeros((timeSlots, len(weights), 4))
#     numCA[:, :, 0] = np.loadtxt('E:\\numOfCA_0.csv', delimiter=',')
#     numCA[:, :, 1] = np.loadtxt('E:\\numOfCA_1.csv', delimiter=',')
#     numCA[:, :, 2] = np.loadtxt('E:\\numOfCA_2.csv', delimiter=',')
#     # numCA[:, :, 3] = np.loadtxt('E:\\numOfCA_3.csv', delimiter=',')
#     for w in range(len(weights)):
#         plt.title("{0} {1}".format("Number of Link with Channel Allccated over slots uder", algList[alg]))
#         lab = "{0} {1}".format("V = ", weights[w])
#         plt.plot(range(timeSlots), numCA[:, w, alg], c=randomcolor(), linestyle='-', marker='o', label=lab)
#     plt.legend()
#     plt.show()
#
#
# def plotAveNumOfCA():
#     numCA = np.zeros((timeSlots, len(weights), 4))
#     numCA[:, :, 0] = np.loadtxt('E:\\numOfCA_0.csv', delimiter=',')
#     numCA[:, :, 1] = np.loadtxt('E:\\numOfCA_1.csv', delimiter=',')
#     numCA[:, :, 2] = np.loadtxt('E:\\numOfCA_2.csv', delimiter=',')
#     # numCA[:, :, 3] = np.loadtxt('E:\\numOfCA_3.csv', delimiter=',')
#     aveNumOfCA = np.zeros((len(weights), 4))
#     for w in range(len(weights)):
#         aveNumOfCA[w, 0] = np.average(numCA[:, w, 0])
#         aveNumOfCA[w, 1] = np.average(numCA[:, w, 1])
#         aveNumOfCA[w, 2] = np.average(numCA[:, w, 2])
#         # aveNumOfCA[w, 3] = np.average(numCA[:, w, 3])
#     bar_width = int((weights[len(weights) - 1]) / (len(weights)) / 4)
#     # print(int(bar_width))
#     # X 轴 变量
#     # x1 = np.array(range(len(weights)))
#     x1 = weights - bar_width
#     plt.bar(x=x1, height=aveNumOfCA[:, 0], label='K-MWIS',
#             color='blue', alpha=0.8, width=bar_width)
#     x2 = x1 + bar_width
#     plt.bar(x=x2, height=aveNumOfCA[:, 1], label='Random Algrithm',
#             color='red', alpha=0.8, width=bar_width)
#     x3 = x2 + bar_width
#     plt.bar(x=x3, height=aveNumOfCA[:, 2], label='Delay-Sensitive',
#             color='gray', alpha=0.8, width=bar_width)
#     x4 = x3 + bar_width
#     plt.bar(x=x4, height=aveNumOfCA[:, 3], label='greedy',
#             color='green', alpha=0.8, width=bar_width)
#     plt.title("AveNumber of Link with Channel Allccated Under Different Algrithm")
#     plt.xlim(weights[0] - bar_width, weights[len(weights) - 1] + bar_width)
#     plt.xlabel("Value of Weights")
#     plt.ylabel("Number of Link with Channel Allccated ")
#
#     plt.legend()
#     plt.show()
#
#
# def plotSunOfDrop():
#     drop = np.zeros((timeSlots, len(weights), 4))
#     drop[:, :, 0] = np.loadtxt('E:\\dataDrop_0.csv', delimiter=',')
#     drop[:, :, 1] = np.loadtxt('E:\\dataDrop_1.csv', delimiter=',')
#     drop[:, :, 2] = np.loadtxt('E:\\dataDrop_2.csv', delimiter=',')
#     # drop[:, :, 3] = np.loadtxt('E:\\dataDrop_3.csv', delimiter=',')
#
#     # print("drop_02:",drop[:, :, 2])
#     totalDrop = np.zeros((len(weights), 4))/timeSlots
#     for w in range(len(weights)):
#         totalDrop[w, 0] = np.sum(drop[:, w, 0])
#         totalDrop[w, 1] = np.sum(drop[:, w, 1])
#         totalDrop[w, 2] = np.sum(drop[:, w, 2])
#         totalDrop[w, 3] = np.sum(drop[:, w, 3])
#     # plt.title("Sum of Traffics Under different Alorithm")
#     bar_width = int((weights[len(weights) - 1]) / (len(weights)) / 4)
#     # print(int(bar_width))
#     # X 轴 变量
#     # x1 = np.array(range(len(weights)))
#     x1 = weights - bar_width
#     plt.bar(x=x1, height=totalDrop[:, 0], label='K-MWIS',
#             color='blue', alpha=0.8, width=bar_width)
#     x2 = x1 + bar_width
#     plt.bar(x=x2, height=totalDrop[:, 1], label='Random Algrithm',
#             color='red', alpha=0.8, width=bar_width)
#     x3 = x2 + bar_width
#     plt.bar(x=x3, height=totalDrop[:, 2], label='Delay-Sensitive',
#             color='gray', alpha=0.8, width=bar_width)
#     x4 = x3 + bar_width
#     plt.bar(x=x4, height=totalDrop[:, 3], label='greedy',
#             color='green', alpha=0.8, width=bar_width)
#     plt.title("Sum of Data Drops Under Different Algrithm")
#     plt.xlim(weights[0] - bar_width, weights[len(weights) - 1] + bar_width)
#     plt.xlabel("Value of Weights")
#     plt.ylabel("Sum of Traffics")
#
#     plt.legend()
#     plt.show()


# def plotDrop(alg):
#     drop = np.zeros((timeSlots, len(weights), 4))
#     drop[:, :, 0] = np.loadtxt('E:\\dataDrop_0.csv', delimiter=',')
#     drop[:, :, 1] = np.loadtxt('E:\\dataDrop_1.csv', delimiter=',')
#     drop[:, :, 2] = np.loadtxt('E:\\dataDrop_2.csv', delimiter=',')
#     # drop[:, :, 3] = np.loadtxt('E:\\dataDrop_3.csv', delimiter=',')
#     for w in range(len(weights)):
#         plt.title("{0} {1}".format("Data Drops over slots uder", algList[alg]))
#         lab = "{0} {1}".format("V = ", weights[w])
#         plt.plot(range(timeSlots), drop[:, w, alg], c=randomcolor(), linestyle='-', marker='o', label=lab)
#     plt.legend()
#     plt.show()

#
# def plotTraffic(alg):
#     traffic = loadValueTriaxis('E:\\trafficOverSlot',3,)
#     traffic[:, :, 0] = np.loadtxt('E:\\trafficOverSlot_0.csv', delimiter=',')
#     traffic[:, :, 1] = np.loadtxt('E:\\trafficOverSlot_1.csv', delimiter=',')
#     traffic[:, :, 2] = np.loadtxt('E:\\trafficOverSlot_2.csv', delimiter=',')
#     # traffic[:, :, 3] = np.loadtxt('E:\\trafficOverSlot_3.csv', delimiter=',')
#     for w in range(len(weights)):
#         plt.title("{0} {1}".format("Traffics over slots uder", algList[alg]))
#         lab = "{0} {1}".format("V = ", weights[w])
#         plt.plot(range(timeSlots), traffic[:, w, alg], c=randomcolor(), linestyle='-', marker='o', label=lab)
#     plt.legend()
#     plt.show()
# def plotOverSlots(figTitle,xlabel,ylabel,V,algList):
#     plt.title(figTitle)
#     # print(aveUtility)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     for n in range(len(algList)):
#         plt.plot(timeSlots, V[:, n], c=randomcolor(), linestyle='-', marker='s', label=algList[n])
#     plt.legend()
#     plt.show()
# def loadValueTriaxis(fname,numOfF,rows,cols):
#     val = np.zeros((rows,cols,numOfF))
#     for n in range(numOfF):
#         name = "{0}_{1}.csv".format(fname,n)
#         val[:,:,n] = np.loadtxt(name,delimiter=',').reshape(val[:,:,n].shape)
#     return val
#
# def plotCompareUnderWeight(figTitle,xlabel,ylabel,V,algList):
#     plt.title(figTitle)
#     for n in range(len(algList)):
#         if len( V.shape )== 3 :
#             plt.plot(weights, V[:,0, n], c=randomcolor(), linestyle='-', marker='s', label=algList[n])
#         else:
#             plt.plot(weights, V[:, n], c=randomcolor(), linestyle='-', marker='s', label=algList[n])
#     plt.legend()
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.show()
#
#
# def plotQueueUnderWeight(figTitle,Q):
#     for w in range(len(weights)):
#         plt.title(figTitle)
#         s = "{0} {1}".format("V = ", weights[w])
#         plt.plot(range(timeSlots), Q[:, w], c=randomcolor(), label=s)
#         plt.legend()  # 显示图例
#     plt.show()
#
# def plotQw(enQw,flowQw,dataQw,virtualQw):
#     plotQueueUnderWeight("Energy Queue",enQw[12,:,:])
#     plotQueueUnderWeight("Data Queue",dataQw[10,:,:])
#     plotQueueUnderWeight("Virtual Queue",virtualQw[10,:,:])
#     plotQueueUnderWeight("Flow Queue",flowQw)
