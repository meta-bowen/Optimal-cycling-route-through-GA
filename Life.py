# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:48:58 2017

@author: hp
"""

#3、Life.py
# -*- coding: utf-8 -*-
  
"""Life.py
  
生命类
"""
  
import random
  
class Life(object):
  
    def __init__(self, env, gene = None):
        self.env = env
  
        if gene == None:
            self.__rndGene()
        elif type(gene) == type([]):
            self.gene = []
            for k in gene:
                self.gene.append(k)
        else:
            self.gene = gene
  
    def __rndGene(self):
        self.gene = ""
        for i in range(self.env.geneLength):
            self.gene += str(random.randint(0, 1))
  
    def setScore(self, v):
        self.score = v
  
    def addScore(self, v):
        self.score += v

"""
运行TSP.py，即可开始程序。几个快捷键说明如下：
n: 开始新的计算（随机产生32个新的城市）
e: 开始进化
s: 停止
q: 退出

程序没有设置终止进化条件，进化一旦开始，如果不手动停止，会一直计算下去。
"""
