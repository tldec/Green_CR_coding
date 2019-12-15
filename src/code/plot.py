#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/15 0:59
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
    plt.title(plt_dict["title"])
    for w in range(len(diff)):
        lbl = "{0} = {1}".format(plt_dict["para_name"],diff[w])

        plt.plot(range(timeSlots), val[:,w], c=__randomcolor(),label=lbl)
    plt.xlabel(plt_dict["xlabel"])
    plt.ylabel(plt_dict["ylabel"])
    plt.legend()  # 显示图例
    plt.show()

def plotUtilityOverWeights(val,diff,plt_dict):
    if diff == None:
        plt.title(plt_dict['title'])
        plt.plot(weights, val, c=__randomcolor(), linestyle='-', marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
    else:
        for w in range(len(diff)):
            lbl = "{0} = {1}".format(plt['para_name'],diff[w])
            plt.title(plt_dict['title'])
            plt.plot(weights, val, c=__randomcolor(),label=lbl,linestyle='-',marker='s')
        plt.xlabel(plt_dict['xlabel'])
        plt.ylabel(plt_dict['ylabel'])
        plt.legend()  # 显示图例
    plt.show()