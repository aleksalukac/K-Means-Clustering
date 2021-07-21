# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 00:41:01 2020

@author: Aleksa
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from copy import deepcopy
from random import randrange
from random import choice
import imageio
from kneed import KneeLocator

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
         return ("(x: "+ str(self.x) + ", y: " + str(self.y) + ")")

    def __repr__(self):
         return ("(x: "+ str(self.x) + ", y: " + str(self.y) + ")")

    def distance(self, a):
        return (self.x - a.x)**2 + (self.y - a.y)**2

def drawPoint(point, c, center):
    plt.scatter(point.x, point.y, color = c)
    x_values = [point.x, center.x]
    y_values = [point.y, center.y]
    plt.plot(x_values, y_values, color = c)

def kMeansClustering(points, clustersCount, createPlots = False, saveToFile = False):
    directory = 'C:/gif/'
    pointsCount = len(points)
    colors = cm.rainbow(np.linspace(0, 1, clustersCount))
    image_count = 0
    sum_of_squared_distances = 0
    squared_sums = []

    if(createPlots):
        for point in points:
            plt.scatter(point.x, point.y)

        plt.savefig(directory + 'plt' + str(image_count) + '.png', bbox_inches='tight')
        image_count += 1
        plt.show()

    centers = []

    for i in range(0, clustersCount):
        rand_points_count = 10
        x = 0
        y = 0
        for _ in range(rand_points_count):
            p = choice(points)
            x += p.x
            y += p.y
        x /= rand_points_count
        y /= rand_points_count
        centers.append(Point(x,y))

    cond = True
    while cond:
        sum_of_squared_distances = 0
        clusters = [ [] for i in range(0, clustersCount)]
        oldCenters = deepcopy(centers)

        for point in points:
            cluster = 0
            dist = point.distance(centers[0])
            for i in range(1, clustersCount):
                if(dist > point.distance(centers[i])):
                    cluster = i
                    dist = point.distance(centers[i])
            clusters[cluster].append(point)

        cond = False
        for i in range(0, clustersCount):
            x = 0
            y = 0
            for point in clusters[i]:
                x += point.x
                y += point.y
                sum_of_squared_distances += ((point.x - centers[i].x)**2 + (point.y - centers[i].y)**2)

            if(len(clusters[i]) != 0):
                centers[i].x = x / len(clusters[i])
                centers[i].y = y / len(clusters[i])

            if(centers[i].distance(oldCenters[i]) != 0):
                cond = True

        squared_sums.append(sum_of_squared_distances)

        if(createPlots):
            i = 0

            for cluster in clusters:
                for point in cluster:
                    drawPoint(point, colors[i], centers[i])

                i += 1

            plt.savefig(directory + 'plt' + str(image_count) + '.png', bbox_inches='tight')
            image_count += 1
            plt.show()

    if(createPlots and saveToFile):
        images = []
        for i in range(0, image_count):
            images.append(imageio.imread(directory + '/plt' + str(i) + '.png'))
        imageio.mimsave(directory + '/movie.gif', images)

    return centers, squared_sums[-1]

def getCenters(points):
    squared_sums = []
    centers = []
    for clustersCount in range(1, len(points)):
        cntrs, sq_sms = kMeansClustering(points, clustersCount)
        centers.append(cntrs)
        squared_sums.append(sq_sms)

    x = range(1, len(squared_sums)+1)
    kn = KneeLocator(x, squared_sums, curve='convex', direction='decreasing')

    elbow_point = kn.knee + 1

    j = 0
    for a in squared_sums:
        j += 1
        plt.scatter(j, a)
        if(j > 1):
            p1 = Point(j, a)
            p2 = Point(j - 1, squared_sums[j - 2])
            drawPoint(p1, 'b', p2)
    plt.show()

    return centers[elbow_point - 1]

def clusterDeeply(points):
    centers = getCenters(points)
    print(centers)

    clusters_count = len(centers)
    centers = []
    errors = []
    for _ in range(3):
        c, error = kMeansClustering(points, clusters_count, True)
        centers.append(c)
        errors.append(error)

    return centers[errors.index(min(errors))], errors.index(min(errors))

randomCount = 40
maxRange = 100
points = []
random_parts_x = [0, 300, 0, 300]
random_parts_y = [0, 0, 300, 300]

for i in range(0, randomCount):
    x = randrange(maxRange) + random_parts_x[i % 4]
    y = randrange(maxRange) + random_parts_y[i % 4]
    points.append(Point(x,y))
print(clusterDeeply())