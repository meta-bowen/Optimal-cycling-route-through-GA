# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:48:12 2017

@author: hp
"""

#2、GA.py
# -*- coding: utf-8 -*-
  
"""GA.py
  
遗传算法类
"""
  
import random
from Life import Life
  
class GA(object):
  
    def __init__(self, xRate = 0.7, mutationRate = 0.005, lifeCount = 50, geneLength = 1000, judge = lambda lf, av: 1, save = lambda: 1, mkLife = lambda: None, xFunc = None, mFunc = None):
        self.xRate = xRate#交叉率
        self.mutationRate = mutationRate#突变率
        self.mutationCount = 0
        self.generation = 0
        self.lives = []
        self.bounds = 0.0 # 得分总数
        self.best = None
        self.lifeCount = lifeCount
        self.geneLength = geneLength
        self.__judge = judge
        self.save = save
        self.mkLife = mkLife    # 默认的产生生命的函数
        self.xFunc = (xFunc, self.__xFunc)[xFunc == None]   # 自定义交叉函数
        self.mFunc = (mFunc, self.__mFunc)[mFunc == None]   # 自定义变异函数
  
        for i in range(lifeCount):
            self.lives.append(Life(self, self.mkLife()))
  
    def __xFunc(self, p1, p2):
        # 默认交叉函数
        r = random.randint(0, self.geneLength)
        gene = p1.gene[0:r] + p2.gene[r:]
        return gene
  
    def __mFunc(self, gene):
        # 默认突变函数
        r = random.randint(0, self.geneLength - 1)
        gene = gene[:r] + ("0", "1")[gene[r:r] == "1"] + gene[r + 1:]
        return gene
  
    def __bear(self, p1, p2):
        # 根据父母 p1, p2 生成一个后代
        r = random.random()
        if r < self.xRate:
            # 交叉
            gene = self.xFunc(p1, p2)
        else:
            gene = p1.gene
  
        r = random.random()
        if r < self.mutationRate:
            # 突变
            gene = self.mFunc(gene)
            self.mutationCount += 1
  
        return Life(self, gene)
  
    def __getOne(self):
        # 根据得分情况，随机取得一个个体，机率正比于个体的score属性
        r = random.uniform(0, self.bounds)
        for lf in self.lives:
            r -= lf.score
            if r <= 0:
                return lf
  
    def __newChild(self):
        # 产生新的后代
        return self.__bear(self.__getOne(), self.__getOne())
  
    def judge(self, f = lambda lf, av: 1):
        # 根据传入的方法 f ，计算每个个体的得分
        lastAvg = self.bounds / float(self.lifeCount)
        self.bounds = 0.0
        self.best = Life(self)
        self.best.setScore(-1.0)
        for lf in self.lives:
            lf.score = f(lf, lastAvg)
            if lf.score > self.best.score:
                self.best = lf
            self.bounds += lf.score
  
    def next(self, n = 1):
        # 演化至下n代
        while n > 0:
            # self.__getBounds()
            self.judge(self.__judge)
            newLives = []
            newLives.append(Life(self, self.best.gene))  # 将最好的父代加入竞争
            # self.bestHistory.append(self.best)
            while (len(newLives) < self.lifeCount):
                newLives.append(self.__newChild())
            self.lives = newLives
            self.generation += 1
            #print("gen: %d, mutation: %d, best: %f" % (self.generation, self.mutationCount, self.best.score))
            self.save(self.best, self.generation)
  
            n -= 1
