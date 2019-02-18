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



def rrr(fileName):
    """ Generates a raster object from a ARC-INFO ascii format file."""
    
    myFile = open(fileName, 'r')
        
    end_header = False
    xll = 0.
    yll = 0.
    nodata =-999.999
    cellsize = 1.0
    
    while (not end_header):
        # Search through lines for raster keywords and their values.
        line = myFile.readline()      
        items = line.split()
        keyword = items[0].lower()
        value = items[1]
        if (keyword == 'ncols'):
            ncols = int(value)
        elif (keyword == 'nrows'):
            nrows = int(value)
        elif (keyword == 'xllcorner'):
            xll = float(value)
        elif (keyword == 'yllcorner'):
            yll = float(value)  
        elif (keyword == 'nodata_value'):
            nodata = float(value)
        elif (keyword == 'cellsize'):
            cellsize = float(value)  
        else:
            end_header = True
    
    # If no rows or no columns, not a valid raster.
    if (nrows == None or ncols == None):
        print ("Row or Column size not specified for Raster file read")
        return None

    datarows = []
    for line in myFile.readlines():
        row = [float(x) for x in line.split()]

        datarows.append(row)
    data = np.array(datarows)
    data = np.vstack([data[0,:], data])
    
    #return(datarows)
    return Raster(data, xll, yll, cellsize, nodata)

path = r'C:\Users\johnd\OneDrive\EdinburghU\Semester 2\OOSE SA\Coursework\myrepo\data'
demfile = r'\DEM.txt'
rainfile = r'\Rainfall.txt'

r = rrr((path + demfile))
r._data.shape


factor = 10
newRowNum = r.getRows() // factor
newColNum = r.getCols() // factor
newData = np.zeros([newRowNum, newColNum])

for i in range(newRowNum):
   for j in range(newColNum):
       sumCellValue = 0.0

       for k in range(factor):
           for l in range(factor):
               sumCellValue += r._data[i * factor + k, j * factor + l]
       newData[i,j] = sumCellValue / factor**2

r2 = Raster(newData, r._orgs[0], r._orgs[1], r._cellsize * factor)
mp.imshow(r2.getData())

mp.imshow(r.getData())
r.getData().shape
