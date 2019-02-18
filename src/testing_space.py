#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:38:44 2019

@author: s1871317
"""
import sys
#sys.path.insert(0,r'/home/s1871317/Documents/Week4')
sys.path.insert(0,r'C:\Users\johnd\OneDrive\EdinburghU\Semester 2\OOSE SA\Work\week-4-workspace-s1871317')

from RasterHandler_jde import readRaster
from matplotlib import pyplot as plt

path = r'C:\Users\johnd\OneDrive\EdinburghU\Semester 2\OOSE SA\Work\week-4-workspace-s1871317'
r = readRaster(path + r'\RasterExample1.txt' )
r = readRaster(path + r'\raster_test2.txt' )
r.getRows()

plt.imshow(r.getData())
plt.imshow(r.smoother(5))

r.sloper()

data = r.getData()
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        y = (i) * self.getCellsize() + self.getOrgs()[0]
        x = (j) * self.getCellsize() + self.getOrgs()[1]
        nodes.append(FlowNode(x, y, data[i,j]))
nodes = []
for i in range(3):
    for j in range(3):
        print(i,j)
        y = (i) * r.getCellsize() + r.getOrgs()[0]
        x = (j) * r.getCellsize() + r.getOrgs()[1]
        nodes.append(FlowNode(x, y, data[i,j]))


# Check relative distribution of flow with constant and variable rainfall
import numpy as np


exfr = flow.FlowRaster(elevationRasterA)       

# before variable rainfall
ffff = []
for i in range(exfr.getRows()):
    for j in range(exfr.getCols()):
        ffff.append(exfr.getData()[i,j].getFlow())
b =  np.arange(min(ffff), max(ffff), (max(ffff) - min(ffff))/50 )
fig = mp.figure(figsize = (9,6))
ax = mp.hist(ffff, bins = list(b))
mp.show()

exfr.addRainfall(rainrasterA.getData())

# after variable rainfall
ffff = []
for i in range(exfr.getRows()):
    for j in range(exfr.getCols()):
        ffff.append(exfr.getData()[i,j].getFlow())
b =  np.arange(min(ffff), max(ffff), (max(ffff) - min(ffff))/50 )
fig = mp.figure(figsize = (9,6))
ax = mp.hist(ffff, bins = list(b), color = 'red')
mp.show()


for i in range(5):
    for j in range(5):
        print(exfr._data[i,j].getPitFlag())

