# -*- coding: utf-8 -*-
"""

"""
import numpy as np

class Raster(object):
    """A class to represent 2-D Rasters."""

    def __init__(self, data, xorg, yorg, cellsize, nodata=-999.999):
        """Initializes raster, with private attributes for data, origin,
        cell size, and nodata indicator value."""
        self._data = np.array(data)
        self._orgs = (xorg, yorg)
        self._cellsize = cellsize
        self._nodata = nodata
        
    def getData(self):
        """Returns raster's data."""
        return self._data
        
    def getShape(self):
        """Returns raster's shape."""
        return self._data.shape    
    
    def getRows(self):
        """Returns raster's row count."""
        return self._data.shape[0]
        
    def getCols(self):
        """Returns raster's column count."""
        return self._data.shape[1]
        
    def getOrgs(self):
        """Returns raster's origin."""
        return self._orgs
        
    def getCellsize(self):
        """Returns raster's cell size."""
        return self._cellsize
    
    def getNoData(self):
        """Returns raster's nodata indicator value."""
        return self._nodata
        
    def createWithIncreasedCellsize(self, factor):
       """
       Returns a new Raster with cell size larger by a 
       factor (which must be an integer).
       """
       if factor == 1:
           return self
       else:
            newRowNum = self.getRows() // factor
            newColNum = self.getCols() // factor
            newData = np.zeros([newRowNum, newColNum])
            
            for i in range(newRowNum):
               for j in range(newColNum):
                   sumCellValue = 0.0
            
                   for k in range(factor):
                       for l in range(factor):
                           sumCellValue += self._data[i * factor + k, j * factor + l]
                   
                   newData[i,j] = sumCellValue / factor ** 2
                   #newData[i,j]._x = newData[i,j]._x / factor
                   #newData[i,j]._y = newData[i,j]._y / factor
                    
       return Raster(newData, self._orgs[0], self._orgs[1], factor)#self._cellsize * factor)
           
           
           