# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 00:41:01 2020

@author: Aleksa
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from random import randrange

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def distance(self, a):
        return (self.x - a.x)**2 + (self.y - a.y)**2

def drawPoint(point, c, center):
    plt.scatter(point.x, point.y, color = c)
    
    x_values = [point.x, center.x]
    
    y_values = [point.y, center.y]
    
    plt.plot(x_values, y_values, color = c)

randomCount = 30
clusterCount = 3
colors = cm.rainbow(np.linspace(0, 1, clusterCount))
points = []

for _ in range(0, randomCount):
    x = randrange(100)
    y = randrange(100)
    points.append(Point(x,y))
    plt.scatter(x, y)
    
plt.show()
centers = []

for i in range(0,clusterCount):
    x = randrange(100)
    y = randrange(100)
    centers.append(Point(x,y))
    
cond = True
while cond:
    clusters = [ [] for i in range(0,clusterCount)]   
    oldCenters = centers.copy()
    
    for point in points:
        cluster = 0
        dist = point.distance(centers[0])
        for i in range(1,clusterCount):
            if(dist > point.distance(centers[i])):
                cluster = i
                dist = point.distance(centers[i])
        clusters[cluster].append(point)
    
    cond = False
    for i in range(0, clusterCount):
        x = 0
        y = 0
        for point in clusters[i]:
            x += point.x
            y += point.y
        
        print(len(clusters[i]))
        centers[i].x = x / len(clusters[i])
        centers[i].y = y / len(clusters[i])
        
        if(centers[i].distance(oldCenters[i]) != 0):
            cond = True
            break

i = 0
for cluster in clusters:
    for point in cluster:
        drawPoint(point, colors[i], centers[i])
        
    i += 1
        

"""
point1 = [1, 2]
point2 = [3, 4]

x_values = [point1[0], point2[0]]

y_values = [point1[1], point2[1]]

plt.plot(x_values, y_values)"""
plt.show()