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




def findExit(flowraster, row, col, con, exc):
    
    # Add current point to the exclude list.
    exc.append(flowraster._data[row, col])
    
    # Add node's neighbors to consideration and remove duplicates.
    con = list(set(con + flowraster.getNeighbours(row, col)))
    
    # Remove exclude list items from consideration.
    con = [x for x in con if x not in exc]
    
    # Find lowest point under consideration.
    lownode = None
    for node in con:           
        if lownode == None or node.getElevation() < lownode.getElevation():
            lownode = node
    
    # Assemble list of the upnodes of excluded cells.
    excUpnodes = []
    for e in exc:
        excUpnodes += e.getUpnodes()
    
    # Check if lownode is an upnode of any nodes in the exclude list.
    if lownode not in excUpnodes:
        flowraster._data[row, col].setDownnode(lownode)
        flowraster._data[row, col]._lakedepth = (lownode.getElevation() - flowraster._data[row, col].getElevation())
    
    else:
        findExit(flowraster, int(lownode.get_x), int(lownode.get_y), con, exc)
    
    return(lownode)



consider = []
exclude = []

exfr = flow.FlowRaster(elevationRasterA)       
l = findExit(exfr, 0, 1, consider, exclude)

exclUpnodes = []
for i in e:
    exclUpnodes += i.getUpnodes()

for i in exclUpnodes:
    print(i.getElevation())
