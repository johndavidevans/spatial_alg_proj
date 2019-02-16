import numpy as np


from Points import Point2D

# Added
from Raster import Raster

class FlowNode(Point2D):
    """A point2D with attributes that define flow: downnode, upnode, pitflag, 
    and value requires as arguments x, y, and value."""
    
    def __init__(self, x, y, value):
        """Initializes FlowNode with _downnode, _upnoddes, _pitflag,
        and _value. Value represents elevation."""
        # Call initialization from Point2D ***is this necessary? super()?
        Point2D.__init__(self, x, y)
        self._downnode = None
        self._upnodes = []
        self._pitflag = True
        self._value = value
        
    def setDownnode(self, newDownNode):
        """Sets a point's downnode."""
        
        # Changes _pitflag to False if newDownNode is supplied.
        self._pitflag = (newDownNode == None)
        
        # If there is already a downnode, remove from upnodes.
        if (self._downnode != None): # change previous
            self._downnode._removedUpnode(self)
        
        # If a newDownNode is passed, add self as an upnode to that node.
        if (newDownNode != None):
            newDownNode._addUpnode(self)
        
        # Set newDownNode as downnode.
        self._downnode = newDownNode 
        
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
    """"""    
    def __init__(self, araster):
        """Initializes FlowRaster with the same origin, cell size, and data
        as the input raster."""
        super().__init__(None, araster.getOrgs()[0], araster.getOrgs()[1],
              araster.getCellsize())
        data = araster.getData() # why not include in init?
        nodes = []
        
        # Iterate through input raster's rows and columns and create a FlowNode
        # (point) for each.
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y = (i) * self.getCellsize() + self.getOrgs()[0]
                x = (j) * self.getCellsize() + self.getOrgs()[1]
                nodes.append(FlowNode(x, y, data[i,j]))
        
        # Convert to array and reshape to match input raster.
        nodearray = np.array(nodes)
        nodearray.shape = data.shape
        self._data = nodearray
        
        # Create index array for eight adjacent points.
        self.__neighbourIterator = np.array([1, -1, 1, 0, 1, 1, 0, -1,
                                             0, 1, -1, -1, -1, 0, -1, 1])
        self.__neighbourIterator.shape = (8,2)
        self.setDownCells()
                    
    def getNeighbours(self, r, c):
        """ Returns a list of the elevations of a node's eight neighbors."""
        neighbours = []
        for i in range(8):
            rr = r + self.__neighbourIterator[i,0]
            cc = c + self.__neighbourIterator[i,1]
            if (rr > -1 and rr < self.getRows() and cc > -1 and cc < self.getCols()):
                neighbours.append(self._data[rr,cc])
            #*** Change the above to add the FlowNode itself to neighbors,
            #*** Rather than adding the _data of the FlowNode???
                
        return neighbours
    
    def lowestNeighbour(self, r, c):
        """Returns the elevation of the lowest neighbor neighbors"""
        lownode = None
        
        for neighbour in self.getNeighbours(r,c):
            
            if lownode == None or neighbour.getElevation() < lownode.getElevation():
                lownode = neighbour
                #*** neighbors are elevations. Do they have .getElevation()???
                
        return lownode

    def setDownCells(self):
        """For each cell in the raster, set the downnode to the neighbor with
        the lowest elevation, unless all neighbors are higher, in which case
        set downnode to None."""
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                lowestN = self.lowestNeighbour(r,c)
                if (lowestN.getElevation() < self._data[r,c].getElevation()):
                    #*** Again, does the _data[r,c] have an elevation, or is it
                    #*** the elevation?
                    self._data[r,c].setDownnode(lowestN)
                else:
                    self._data[r,c].setDownnode(None)
                        #*** Should we also set pitflag to true?
    
    def extractValues(self, extractor):
        """Returns the values as an array of the same size."""
        values = []
        for i in range(self._data.shape[0]): #*** should we use the .getRows()
            for j in range(self._data.shape[1]): #*** and .getCols()  for consistency?
                values.append(extractor.getValue(self._data[i,j]))
                #*** Could FlowNode.getFlow() not be accessed more directly?
        valuesarray = np.array(values)
        valuesarray.shape = self._data.shape
        return valuesarray
    
class FlowExtractor():
    #*** Obfuscation? Why is this its own class? Add .getValue as a method above?
    def getValue(self, node):
        """Returns the results of FlowNode.getFlow()"""
        return node.getFlow()
