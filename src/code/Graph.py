#_*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/7 16:52
import  numpy as np
class Graph:
    def __init__(self, V, E,W):
        # print("E:",E)
        self.V = np.array(V)
        self.Edge = np.array(E)
        # print("self.E:",self.Edge)
        self.wEdge = np.array(W)
        self.dList = np.zeros(len(self.V),dtype=np.int32)
        self.degree = 0
        self.init()
    def updateDegree(self):
        self.degree = np.max(self.dList)
    def updateDList(self):
        for v in range(len(self.V)):
            self.dList[v] = np.sum(self.Edge[v,:])
    def init(self):
        self.updateDList()
        self.updateDegree()
    def removeNode(self,n):
        # print("删除邻居:",n)
        # self.V = np.delete(self.V,np.where(self.V == n))
        self.V[n] = 0
        self.Edge[n,:] = np.zeros(self.Edge.shape[1])
        self.Edge[:,n] = np.zeros(self.Edge.shape[0])
        self.wEdge = self.V * self.wEdge
    def coloring(self,n):
        # print("删除结点",n)
        # print("删除前 V:", self.V)
        # print("删除前 dList:", self.dList)
        # print("删除前 wEdge:",self.wEdge)
        # print("E:",self.Edge)
        tmpV = self.V.copy()
        tmpE = self.Edge.copy()
        for i in range(len(tmpV)):
            # print("Edge[n][i]:",tmpE[n][i])
            if tmpE[n][i] == 1:
                # print("删除邻居",i)
                self.removeNode(i)

        # print("删除后 wEdge:", self.wEdge)
        self.updateDList()
        self.updateDegree()
        # print("删除后 V:", self.V)
        # print("删除后 dList:", self.dList)



