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
        self._rainfall = 1
        self._lakedepth = 0
        
    def setDownnode(self, newDownNode):
        """Sets a point's downnode."""
        
        # Changes _pitflag to False if newDownNode is supplied.
        self._pitflag = (newDownNode == None)
        
        # If there is already a downnode, remove self from upnodes.
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
    
    def getFlow(self):
        """
        Calculates the flow volume passing through a particular node by 
        recursively moving upstream. Added as a part of Task 2.
        """
        self.flow = self._rainfall
        for upnode in self.getUpnodes():
            self.flow += upnode.getFlow()
        return(self.flow)
        
    def getLakeDepth(self):
        """Calculates the depth of lakes."""
        return self._lakedepth
        
        
class FlowRaster(Raster):
    """
    A raster whose data is an array of FlowNodes associated with each cell of 
    the original input raster.
    """    
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
        """ Returns a list containing a node's neighbors."""
        neighbours = []
        for i in range(8):
            rr = r + self.__neighbourIterator[i,0]
            cc = c + self.__neighbourIterator[i,1]
            if (rr > -1 and rr < self.getRows() and cc > -1 and cc < self.getCols()):
                neighbours.append(self._data[rr,cc])
                
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
                    self._data[r,c].setDownnode(lowestN)
                else:
                    self._data[r,c].setDownnode(None)

    
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
    
    def addRainfall(self, raindata):
        """Add rainfall..."""
        for i in range(self.getRows()):
            for j in range(self.getCols()):
                self._data[i,j]._rainfall = raindata[i,j]
    
    def joinCatchments(self, row, col, con, exc):
        """"""
        # Define current node
        curnode = self._data[row, col]
        # Add current point to the exclude list.
        exc.append(curnode)
        
        # Add node's neighbors to consideration and remove duplicates.
        con = list(set(con + self.getNeighbours(row, col)))
    
        # Remove exclude list items from consideration.
        con = [x for x in con if x not in exc]
        
        # Find lowest point under consideration.
        lownode = None
        for node in con:
            if lownode == None or node.getElevation() < lownode.getElevation():
                lownode = node
        
        # Get indices of lownode.
        lowx = int(lownode.get_x() / self.getCellsize())
        lowy = int(lownode.get_y() / self.getCellsize())
        
        # Assemble list of the upnodes of excluded cells.
        excUpnodes = []
        for e in exc:
            excUpnodes += e.getUpnodes()
        
        # If lownode is an upnode of any nodes in the exclude list, recurse.
        if lownode in excUpnodes:
            lownode = self.joinCatchments(lowy, lowx, con, exc)
            
        curnode.setDownnode(lownode)
        
        if lownode.getElevation() > curnode.getElevation():
            curnode._lakedepth = lownode.getElevation() - curnode.getElevation()
        return(lownode)

    def traceBack(self, area, pit, tracenode):
        
        # Get coords of current tracenode.
        cs = self.getCellsize()
        tnx = int(tracenode.get_x() / cs)
        tny = int(tracenode.get_y() / cs)
        
        # List neighbors of current traceback node that are in the area of consideration.
        lowneighbours = [x for x in self.getNeighbours(tnx, tny) if x in area]
        
        # If the original pit is among them, set traceback as downnode. We're done.
        if pit in lowneighbours:
            pit.setDownnode(tracenode)
        
        #If not, set the traceback as a downnode of the lowest neighbour.
        
        elif len([x.getElevation() for x in lowneighbours]) > 0:
            # Find the lowNeighbour with the lowest elevation.
            # COULD USE ABOVE METHODS
            
            elevs = [x.getElevation() for x in lowneighbours]
            if len(elevs) > 0:
                #newtraceindex = np.argmin([0,elevs])  
                newtraceindex = elevs.index(min(elevs))
                newtrace = lowneighbours[newtraceindex]
                
                # Set low as downnode of newlow.
                newtrace.setDownnode(tracenode)
                 
                FlowRaster.traceBack(self, area, pit, newtrace)
                
            
                return newtrace
        
    
    def calculateLakes(self):
        """ Calculates lake depths and """
        for i in range(self.getRows()):
            for j in range(self.getCols()):
                node = self._data[i,j]
                
                # Only pits not along the border of the elevation.
                if node.getPitFlag() & (i != 0) & (i != (self.getRows() - 1)) & (j != 0) & (j != (self.getCols() - 1)):
                    pit = self._data[i,j]
                    consider = []
                    exclude = []
                    
                    # Find spillover node and use to calculate lakedepth.
                    lownode = self.joinCatchments(i, j, consider, exclude)
                    #pit._lakedepth = (lownode.getElevation() - pit.getElevation())
                    
                    # Fix where Cellsize adjustment takes place!
                    
                    # NEW ATTEMPT
                    # Adjust upnode/downnode relationships to reflect flow from pit to spillover point.
                    
                    # Get xs and ys from excluded list so bounding box can be set.
                    #cs = self.getCellsize()
                    #xs = [int(n.get_x() / cs) for n in exclude]
                    #ys = [int(n.get_y() / cs) for n in exclude]

                    # Area bounded by exclude (of which pit is the first member).
                    
                    #traceArea = self.getData()[min(xs):max(xs) + 1, min(ys):max(ys) + 1]
                    
                    # Recursive traceback.
                    #FlowRaster.traceBack(self, traceArea, pit, lownode)

                    
class FlowExtractor():
    #*** Obfuscation? Why is this its own class? Add .getValue as a method above?
    def getValue(self, node):
        """Returns the results of FlowNode.getFlow()"""
        return node.getFlow()

class LakeDepthExtractor():
    def getValue(self, node):
        return node.getLakeDepth()
    
    
                        # New idea
                    # Create a bounding box of coordinates using lownode and pitnode
                    # starting at the lownode, find the box neighbor with the next lowest elevation
                    # set self as downnode of that neighbor
                    # new lownode = the neighbor just joined to
                    # recurse until the neighbor is the pitnode
                    
                    # Alternatively "Add a method to trace all upnodes"
                    
                    # Find neighbors of lownode
                    # Find which of these is in exclude
                    # Find which is the closest to lownode
                    # Set lownode as the downnode of the closest
                    
                    # Another possible approach:
                    # Check all neighbors of pit
                        # If lowest
    

            
                    #minoverlap.setDownnode(lownode)                  
                    #    if overlap[i].getElevation() < minoverlap.getElevation():
                    #        minoverlap = overlap[i]
                    #minoverlap.setDownnode(lownode)
                    # If lownode IS an upnode of any nodes in the exclude list
                                        # Overlap:
                    #overlap = [x for x in self.getNeighbours(lowy, lowx) if x in exc]
                    #minoverlap = overlap[0]
                    #for i in range(1, len(overlap)):
                    #    if np.sqrt((lownode.get_x() - minoverlap.get_x())**2 + (lownode.get_y() - minoverlap.get_y())**2) > np.sqrt((lownode.get_x() - overlap[i].get_x())**2 + (lownode.get_y() - overlap[i].get_y())**2):
                    #        minoverlap = overlap[i]
                    #minoverlap.setDownnode(lownode)
                