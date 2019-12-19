#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/14 19:56
from matplotlib import pyplot as plt
import random
def __randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

def plotOverSlot(timeSlots,val,diff,plt_dict):
    # print(plt_dict["title"])
    plt.title(plt_dict["title"])
    for w in range(len(diff)):
        lbl = "{0} = {1}".format(plt_dict["para_name"],diff[w])
        plt.plot(range(timeSlots), val[:,w], c=__randomcolor(),label=lbl)
    plt.xlabel(plt_dict["xlabel"])
    plt.ylabel(plt_dict["ylabel"])
    plt.legend(loc="best")  # 显示图例
    # plt.savefig(plt_dict["fname"])
    plt.show()

def plotUtilityOverWeights(weights,val,diff,plt_dict):
    # print("val:",val)
    if diff is None:
        plt.title(plt_dict['title'])
        plt.plot(weights, val, c=__randomcolor(), linestyle='-', marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
        # plt.savefig(plt_dict["fname"])
        plt.show()
    else:
        plt.title(plt_dict['title'])
        for w in range(len(diff)):
            # print(val)
            lbl = "{0}".format(diff[w])
            # print("val[:,w]",val[:,w])
            plt.plot(weights, val[:,w], c=__randomcolor(),label=lbl,linestyle='-',marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
        plt.legend()  # 显示图例
        # plt.savefig(plt_dict["fname"])
        plt.show()
