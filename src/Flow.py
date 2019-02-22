import numpy as np


from Points import Point2D

# Added
from Raster import Raster

class FlowNode(Point2D):
    """
    A point2D with attributes to define flow: downnode, upnode, pitflag, 
    and value requires as arguments x, y, and value.
    """
    
    def __init__(self, x, y, value):
        """Initializes FlowNode with _downnode, _upnoddes, _pitflag,
        _value, _rainfall, and _lakedepth."""
        Point2D.__init__(self, x, y)
        self._downnode = None
        self._upnodes = []
        self._pitflag = True
        self._value = value
        self._rainfall = 1
        self._lakedepth = 0
        
    def setDownnode(self, newDownNode):
        """
        Sets flownode's downnode as specified, updating the pit flag and the 
        downnode's upnodes accordingly.
        """
        
        # Not a pit if it has a downnode.
        self._pitflag = (newDownNode == None)
        
        # If there is already a downnode, remove self from upnodes.
        if (self._downnode != None): # change previous
            self._downnode._removedUpnode(self)
        
        # If a newDownNode is passed, add self as an upnode to that node, 
        #and set newDownNode as downnode.
        if (newDownNode != None):
            newDownNode._addUpnode(self)
        self._downnode = newDownNode 
        
    def getDownnode(self):
        """Returns flownode's downnode."""
        return self._downnode 
        
    def getUpnodes(self):
        """Returns flownode's upnodes."""
        return self._upnodes
    
    def _removedUpnode(self, nodeToRemove):
        """Removes specified node from _upnodes."""
        self._upnodes.remove(nodeToRemove)
    
    def _addUpnode(self, nodeToAdd):
        """Adds specified node to _upnodes."""
        self._upnodes.append(nodeToAdd)

    def numUpnodes(self):
        """Returns flownode's number of upnodes."""
        return len(self._upnodes)
        
    def getPitFlag(self):
        """Returns flownode's _pitflag attribute."""
        return self._pitflag 
    
    def getElevation(self):
        """Returns the _value attribute,."""
        return self._value
  
    def __str__(self):
        """
        Returns a string giving flownode's x and y values, using parental
        functions.
        """
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())
    
    def getFlow(self):
        """
        Calculates the flow volume passing through flownode by recursively
        adding flow from upnodes. Added as a part of Task 2.
        """        
        self.flow = self._rainfall # Rainfall defaults to 1mm for Task 2.
        for upnode in self.getUpnodes():
            self.flow += upnode.getFlow()
        return(self.flow)
        
    def getLakeDepth(self):
        """Calculates the depth of lakes. Added as part of Task 4."""
        return self._lakedepth
        
        
class FlowRaster(Raster):
    """
    A raster whose data is an array of FlowNodes associated with each cell of 
    the original input raster.
    """    
    def __init__(self, araster):
        """
        Initializes FlowRaster with the same origin, cell size, and data
        as the input raster.
        """
        super().__init__(None, araster.getOrgs()[0], araster.getOrgs()[1],
              araster.getCellsize())
        data = araster.getData() # why not include in init?
        nodes = []
        
        # Create a FlowNode for each of input raster's rows and columns.
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y = (i) * self.getCellsize() + self.getOrgs()[0]
                x = (j) * self.getCellsize() + self.getOrgs()[1]

                nodes.append(FlowNode(x, y, data[i,j]))
                
        # Array matching input raster's shape.
        nodearray = np.array(nodes)
        nodearray.shape = data.shape
        self._data = nodearray
        
        # Create indices for eight adjacent points.
        self.__neighbourIterator = np.array([1, -1, 1, 0, 1, 1, 0, -1,
                                             0, 1, -1, -1, -1, 0, -1, 1])
        self.__neighbourIterator.shape = (8,2)
        self.setDownCells()
                    
    def getNeighbours(self, r, c):
        """ Returns a list containing a specified node's neighbours."""
        neighbours = []
        for i in range(8):
            rr = r + self.__neighbourIterator[i,0]
            cc = c + self.__neighbourIterator[i,1]
            if (rr > -1 and 
                rr < self.getRows() and 
                cc > -1 and 
                cc < self.getCols()):
                
                neighbours.append(self._data[rr,cc])
                
        return neighbours
    
    def lowestNeighbour(self, r, c):
        """Returns a specified node's neighbour with lowest elevation."""
        lownode = None
        
        for neighbour in self.getNeighbours(r,c):
            
            if lownode == None or neighbour.getElevation() < lownode.getElevation():
                lownode = neighbour
                       
        return lownode

    def setDownCells(self):
        """
        For each cell in the raster, sets the downnode to the neighbour with
        lowest elevation. If all neighbours are higher, set downnode to None.
        """
        for r in range(self.getRows()):
            for c in range(self.getCols()):
                lowestN = self.lowestNeighbour(r,c)
                if (lowestN.getElevation() < self._data[r,c].getElevation()):
                    self._data[r,c].setDownnode(lowestN)
                else:
                    self._data[r,c].setDownnode(None)

    
    def extractValues(self, extractor):
        """Returns values as required by a specified Extractor class."""
        values = []
        for i in range(self._data.shape[0]):
            for j in range(self._data.shape[1]):
                values.append(extractor.getValue(self._data[i,j]))
        valuesarray = np.array(values)
        valuesarray.shape = self._data.shape
        return valuesarray
    
    def addRainfall(self, raindata):
        """
        Overwrites _rainfall values with values from specified rain data of 
        the same shape. Added as part of Task 3.
        """
        for i in range(self.getRows()):
            for j in range(self.getCols()):
                self._data[i,j]._rainfall = raindata[i,j]
    
    def joinCatchments(self, row, col, con, exc):
        """
        Joins a specified node's catchment to a neighbouring catchment by 
        searching and recursively adding lowest neighbouring nodes until 
        finding one in a different catchment. Also sets each point tried (each 
        flooded node) as a lake by calculating its _lakedepth, based on the 
        difference in elevation between that point and the spillover point. 
        Added as part of Task 4.
        
        Args:
            row: Row of the pit in the catchment to be joined to another 
                catchment.
            col: Column of the pit in the catchment to be joined to another 
                catchment.
            con: List for storing all untried spillover point candidates. Must 
                be initialized outside this method, and should be empty at 
                start.
            exc: List for storing all neighbouring nodes to be excluded from
                consideration as possible spillover points. Must be initialized 
                outside this method, and should be empty at start.
        
        Returns:
            The spillover point.
        """
        # Add current point to the exclude list.
        curnode = self._data[row, col]
        exc.append(curnode)
        
        # Add node's neighbours to consideration and remove duplicates.
        con = list(set(con + self.getNeighbours(row, col)))
    
        # Remove exclude list items from consideration.
        con = [x for x in con if x not in exc]
        
        # Find lowest point under consideration.
        lownode = None
        for node in con:
            if lownode == None or node.getElevation() < lownode.getElevation():
                lownode = node
        
        # Get indices of lownode, accounting for possible resampling.
        lowx = int(lownode.get_x() / self.getCellsize())
        lowy = int(lownode.get_y() / self.getCellsize())
        
        # Assemble list of the upnodes of excluded cells.
        excUpnodes = []
        for e in exc:
            excUpnodes += e.getUpnodes()
        
        # If lownode is an upnode of any nodes in the exclude list, recurse.
        if lownode in excUpnodes:
            lownode = self.joinCatchments(lowy, lowx, con, exc)
            
        # Add update upnodes and downnodes, and set lakedepth if appropriate.
        curnode.setDownnode(lownode)
        if lownode.getElevation() > curnode.getElevation():
            curnode._lakedepth = lownode.getElevation() - curnode.getElevation()
        
        return(lownode)

    def calculateLakes(self):
        """ 
        Calculates lake depths and joins catchments for all pits. Added as 
        part of Task 4.
        """
        for i in range(self.getRows()):
            for j in range(self.getCols()):
                node = self._data[i,j]
                
                # Only pits not along the border of the elevation.
                if (node.getPitFlag() & 
                    (i != 0) & 
                    (i != (self.getRows() - 1)) & 
                    (j != 0) & 
                    (j != (self.getCols() - 1))):
                    
                    # Find spillover node and use to calculate lakedepth.
                    consider = []
                    exclude = []
                    self.joinCatchments(i, j, consider, exclude)
                    
                    
class FlowExtractor():
    def getValue(self, node):
        """Extracts results of FlowNode.getFlow()."""
        return node.getFlow()

class LakeDepthExtractor():
    """Extracts results of FlowNode.getLakeDepth(). Added as part of Task 4."""
    def getValue(self, node):
        return node.getLakeDepth()
    
