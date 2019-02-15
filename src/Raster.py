# -*- coding: utf-8 -*-
"""

"""
import numpy as np

class Raster(object):
    
    '''A class to represent 2-D Rasters'''

# Basic constuctor method
    def __init__(self,data,xorg,yorg,cellsize,nodata=-999.999):
        self._data=np.array(data)
        self._orgs=(xorg,yorg)
        self._cellsize=cellsize
        self._nodata=nodata
        
    def getData(self):
        return self._data
        
#return the shape of the data array      
    def getShape(self):
        return self._data.shape    
    
    def getRows(self):
        return self._data.shape[0]
        
    def getCols(self):
        return self._data.shape[1]
        
    def getOrgs(self):
        return self._orgs
        
    def getCellsize(self):
        return self._cellsize
    
    def getNoData(self):
        return self._nodata
        
    # returns a new Raster with cell size larger by a factor (which must be an integer)
    def createWithIncreasedCellsize(self, factor):
       if factor== 1:
           return self
       else:
           raise ValueError("createWithIncreasedCellsize: not fully implemented so only works for scaling by factor 1!")

    