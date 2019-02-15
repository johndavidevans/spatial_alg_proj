import numpy as np


from Points import Point2D

# Added
from Raster import Raster

class FlowNode(Point2D):

# is a point 2D
# requires as arguments x, y, and value
    
    def __init__(self,x,y, value):
        """
        Initializes instantiation of FlowNode.
        """
        # Call initialization from Point2D **is this necessary? super()?
        Point2D.__init__(self,x,y)
        self._downnode=None
        self._upnodes=[]
        self._pitflag=True
        self._value=value
        
    def setDownnode(self, newDownNode):
        """Sets a point's downnode."""
        
        # Changes _pitflag to False if newDownNode is supplied.
        self._pitflag=(newDownNode==None)
        
        # If there is already a downnode, remove from upnodes.
        if (self._downnode!=None): # change previous
            self._downnode._removedUpnode(self)
        
        # If a newDownNode is passed, add self as a downnode to that node.
        if (newDownNode!=None):
            newDownNode._addUpnode(self)
        
        # Set newDownNode as _downnode.
        self._downnode=newDownNode 
        
    def getDownnode(self):
        """Returns downnode."""
        return self._downnode 
        
    def getUpnodes(self):
        """Returns upnodes."""
        return self._upnodes
    
    def _removedUpnode(self, nodeToRemove):
        """Removes node from _upnodes."""
        self._upnodes.remove(nodeToRemove)
    
    def _addUpnode(self, nodeToAdd):
        """Adds node to _upnodes."""
        self._upnodes.append(nodeToAdd)

    def numUpnodes(self):
        """Returns the number of upnodes."""
        return len(self._upnodes)
        
    def getPitFlag(self):
        """Returns the _pitflag attribute."""
        return self._pitflag 
    
    def getElevation(self):
        """Returns the _value attribute,."""
        return self._value
  
    def __str__(self):
        """Returns a string giving x and y, using parental functions."""
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())
    
class FlowRaster(Raster):

    def __init__(self,araster):
        super().__init__(None,araster.getOrgs()[0],araster.getOrgs()[1],araster.getCellsize())
        data = araster.getData()
        nodes=[]
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y=(i)*self.getCellsize()+self.getOrgs()[0]
                x=(j)*self.getCellsize()+self.getOrgs()[1]
                nodes.append(FlowNode(x,y, data[i,j]))
            
        nodearray=np.array(nodes)
        nodearray.shape=data.shape
        self._data = nodearray

        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
        self.setDownCells()
        
              
    def getNeighbours(self, r, c):
        neighbours=[]
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])
                
        return neighbours
    
    def lowestNeighbour(self,r,c):
        lownode=None
        
        for neighbour in self.getNeighbours(r,c):
            if lownode==None or neighbour.getElevation() < lownode.getElevation():
                lownode=neighbour
        
        return lownode

    def setDownCells(self):
       for r in range(self.getRows()):
           for c in range(self.getCols()):
               lowestN = self.lowestNeighbour(r,c)
               if (lowestN.getElevation() < self._data[r,c].getElevation()):
                   self._data[r,c].setDownnode(lowestN)
               else:
                   self._data[r,c].setDownnode(None)
    
    def extractValues(self, extractor):
        values=[]
        for i in range(self._data.shape[0]):
            for j in range(self._data.shape[1]):
                values.append(extractor.getValue(self._data[i,j]))
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        return valuesarray
    
class FlowExtractor():
    def getValue(self, node):
        return node.getFlow()
