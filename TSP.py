
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:29:43 2017

@author: hp
"""

#1、TSP.py
# -*- coding: utf-8 -*-
 
"""TSP.py
 
TSP问题
"""
 
import sys
import random
from math import *
import tkinter
from functools import reduce 
import threading
 
from GA import GA
 
class MyTSP(object):
    "TSP"
 
    def __init__(self, root, width=1200, height=900, n = 20):   #传入参数
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.canvas = tkinter.Canvas(
                root,
                width =self.width,
                height =self.height,
                bg = "#ffffff",   #背景窗口颜色
                xscrollincrement = 1,
                yscrollincrement = 1
            )         #打开窗口
        self.canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
        self.title("三亚自然景观最优路径")
        self.__r = 5
        self.__t = None
        self.__lock = threading.RLock()
 
        self.__bindEvents()
        self.new()
 
    def __bindEvents(self):
        self.root.bind("q", self.quite)
        self.root.bind("n", self.new)
        self.root.bind("e", self.evolve)
        self.root.bind("s", self.stop)
 
    def title(self, s):
        self.root.title(s)
 
    def new(self, evt = None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
 
        self.clear()
        self.nodes = [] # 节点坐标
        self.nodes2 = [] # 节点图片对象
        self.nodes3=[]#节点对应字符
        self.nodes4=[]#保存经纬度，纬度为90-y
        file=open("三亚自然景观经纬坐标.txt","r")
        list_row=file.readlines()
        list_source=[]
        n=0
        for list_line in list_row:
            list_line=list(list_line.strip().split(","))
            s=[]
            for i in list_line:
                s.append(i)
            list_source.append(s)
            n=n+1
        for i in range(n):
            a=(list_source[i][0])
#以经纬度（0,90N）为坐标原点，注意坐标原点是屏幕的左上角
            y=(eval(list_source[i][1]))#纬度
            x=(eval(list_source[i][2]))#经度
            x1=(x-109)*1500
            y1=(18.5-y)*1500
            self.nodes.append((x1,y1))
            node = self.canvas.create_oval(x1 - self.__r,
                    y1 - self.__r,x1 + self.__r,y1+ self.__r,
                    fill = "#fff000",
                    outline = "#000000",
                    tags = "node",
                    #tags=a,
                )
            self.nodes2.append(node)
            str= self.canvas.create_text((x1,y1+15),
                                         text = a,
                                         fill="#ff0000",
                                         
               )
            self.nodes3.append(str)
            self.nodes4.append((x,90-y))
 
        self.ga = GA(
                lifeCount = 50,
                mutationRate = 0.05,
                judge = self.judge(),
                mkLife = self.mkLife(),
                xFunc = self.xFunc(),
                mFunc = self.mFunc(),
                save = self.save()
            )
        self.order = range(self.n)
        self.line(self.order)

    
    def distance(self, order):
        "得到当前顺序下连线总长度"
        distance = 0
        R=0.6371004    #单位1000千米
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1,p2 = self.nodes4[i1], self.nodes4[i2]   #分别代表两个节点，p[0]代表经度，p[1]代表纬度
            #distance += math.sqrt((p1[0] - p2[0])** 2 + (p1[1] - p2[1]) ** 2)
            C = sin(p1[1])*sin(p2[1])*cos(p1[0]-p2[0]) + cos(p1[1])*cos(p2[1])

            distance += R*acos(C)*pi/180
          
        return distance
        
    
    def mkLife(self):
        def f():
            lst = list(range(self.n))
            random.shuffle(lst)
            return lst
        return f
 
    def judge(self):
        "评估函数"
        return lambda lf, av = 100: 1.0 / self.distance(lf.gene)
 
    def xFunc(self):
        "交叉函数"
        def f(lf1, lf2):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(self.n - 1, self.n)
            g1 = lf2.gene[p1:p2] + lf1.gene
            # g2 = lf1.gene[p1:p2] + lf2.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11
        return f
 
    def mFunc(self):
        "变异函数"
        def f(gene):
            p1 = random.randint(0, self.n - 2)#取整
            p2 = random.randint(self.n - 2, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            return gene
        return f
 
    def save(self):
        def f(lf, gen):
            pass
        return f
 
    def evolve(self, evt = None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()
 
        while self.__running:
            self.ga.next()
            self.line(self.ga.best.gene)
            self.title("迭代次数: %d" % self.ga.generation)
            self.canvas.create_text((80,40),
                                         text = "数据来源:谷歌地图",
                                         fill="#000000")
            
            self.canvas.update()
 
        self.__t = None
 
    def line(self, order):
        "将节点按 order 顺序连线"
        self.canvas.delete("line")
        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill = "#000000", tags = "line")
            return i2
 
        reduce(line2, order, order[-1])
 
    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)
 
    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        sys.exit()
 
    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
#        self.canvas.create_text((250,50),
#                        text = self. distance,
#                        fill="#f00000")
        self.__lock.release()
 
    def mainloop(self):
        self.root.mainloop()
 
if __name__ == "__main__":
    MyTSP(tkinter.Tk()).mainloop()

"""
    def distance(self,list_source):
        distance=0
        R=0.6371004
        for i in range(self.n):
            a=(90-eval(list_source[i][1]))
            b=(eval(list_source[i][2]))
            if(i==self.n-1):
                a1=(90-eval(list_source[0][1]))
                b1=(eval(list_source[0][2]))
            a1=(90-eval(list_source[i+1][1]))
            b1=(eval(list_source[i+1][2]))
            C=sin(a)*sin(a1)*cos(b-b1)+cos(a)*cos(a1)
            distance+=R*acos(C)*pi/180
            
        return distance
"""
