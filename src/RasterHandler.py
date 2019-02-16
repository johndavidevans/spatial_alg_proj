# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 01:00:00 2013

@author: nrjh
"""
import numpy as np
from Raster import Raster
import random
import math

def readRaster(fileName):
    """ Generates a raster object from a ARC-INFO ascii format file."""
    
    myFile = open(fileName, 'r')
        
    end_header = False
    xll = 0.
    yll = 0.
    nodata =- 999.999
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
    
    ##***commented these out to test redundancy
    ##***delete later if everything works
    #items = line.split() #***redundant?
        
    # Assemble data as a list of lists.
    datarows = []
    #***items = line.split()
    #***row = []
    #***for item in items:
    #***    row.append(float(item))
 
    #***datarows.append(row)
    
    #lines = [] #***Moved from top for clarity`    
    for line in myFile.readlines():
        #***lines.append(line)
        row = [float(x) for x in line.split()]
        #***items = line.split()
    
        #***row = []
        #***for item in items:
        #    row.append(float(item))
   
        datarows.append(row)
    ##***end commented these out to test redundancy

    data = np.array(datarows)
    
    # Returns a raster.
    return Raster(data, xll, yll, cellsize, nodata)
    

    
#def createRanRaster(rows=25,cols-25,cellsize=1,xorg=0,yorg=0,nodata=-999.999,levels=1,datahi=0.,datalo=0.:
# modify cell size
def createRanRaster(rows=20, cols=30, cellsize=2, xorg=0, yorg=0,
                    nodata=-999.999, levels=5, datahi=100., datalo=0.):
 
   #print (rows,cols,levels)
   
   #levels = min(levels, rows)
   
   # Set data sizes
   levels = min(levels, cols)
   data = np.zeros([levels, rows, cols])  
   dataout = np.zeros([rows, cols]) 
   
   # Assign uniformly distributed random data.
   for x in np.nditer(data, op_flags=['readwrite']):
       x[...] = random.uniform(datalo, datahi) 
   #print data
   #np.nditer()

   #*** Begin random magic. Explore as time permits.
   for i in range(levels):
       lin = ((i) * 2) + 1
       lin2 = lin * lin
       
       #print (lin,lin2)
       iterator = np.zeros([lin2,2], dtype=int)
       for itx in range(lin):
           for ity in range(lin):
               iterator[itx * lin + ity, 0] = (itx - i)
               iterator[itx * lin + ity, 1] = (ity - i)
       #print iterator
       
       part = data[i]
       
       
       new = np.zeros([rows,cols])
       for j in range(rows):
           for k in range(cols):
                for it in range(lin2):
                        r = (j + iterator[it, 0]) % rows
                        c = (k + iterator[it, 1]) % cols
                        #print (i,j,k,r,c)
                        new[j,k] = new[j,k] + part[r,c]
        
       minval = np.min(new)
       maxval = np.max(new)
       ran = maxval - minval
       data[i] = ((new - minval) / ran) * (2 ** i)
       #print data[i]
       
       dataout = dataout + data[i]
       
   minval = np.min(dataout)
   maxval = np.max(dataout)
   ran = maxval - minval
   datarange = datahi - datalo
   dataout = (((dataout - minval) / ran) * (datarange)) + datalo
   #*** End random magic. Explore as time permits.
   
   return Raster(dataout, xorg, yorg, cellsize, nodata)


   
# Increase cell size to improve plotting appearance.
def createRanRasterSlope(rows=20, cols=30, cellsize=10, xorg=0, yorg=0,
                         nodata=-999.999, levels=5, datahi=100., datalo=0.,
                         focusx=None, focusy=None, ranpart=0.5):
    
    # Set default focal function values.
    if (focusx == None):
        focusx = cols / 2
    if (focusy == None):
        focusy = rows / 2
    
    # Create a random raster.    
    rast = createRanRaster(rows, cols, cellsize, xorg, yorg,
                           nodata, levels, 1., 0.)

    # Create an empty array of the same size as raster for slope ddata.
    slope_data = np.zeros([rows,cols])
    maxdist = math.sqrt(rows * rows + cols * cols) # Diagonal of whole raster.
    
    for i in range(rows):
        for j in range(cols):
            xd = focusx - j
            yd = focusy - i
            dist = maxdist - math.sqrt((xd * xd) + (yd * yd))
            slope_data[i,j] = dist / maxdist
    
    #***version 1        
    minval = np.min(slope_data) #*** not returned
    maxval = np.max(slope_data)
    ran = maxval - minval
    #***
    
    slope_data = ((slope_data - minval) / ran)
    
    ran_data = rast.getData()
    
    data_out = slope_data * (1. - ranpart) + ran_data * (ranpart)
    
    #*** reuse variable names. is this necessary?
    minval = np.min(data_out)
    maxval = np.max(data_out)
    ran = maxval - minval
    #***
    datarange = datahi - datalo
    data_out = (((data_out - minval) / ran) * datarange) + datalo
        
    return Raster(data_out, xorg, yorg, cellsize)
    