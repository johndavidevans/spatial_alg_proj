from RasterHandler import createRanRasterSlope
from RasterHandler import readRaster
import matplotlib.pyplot as mp
import Flow as flow

def plotstreams(flownode,colour):
    """
    Plots streams by recursing up until reaching a node with no upnodes.
    """
    for node in flownode.getUpnodes():
        # Gets coords of node passed, and (iteratively) plot line to
        # each of its upnodes.
        x1 = flownode.get_x() #*** Would be more efficient for these to be outside loop.
        y1 = flownode.get_y() #*** Would be more efficient for these to be outside loop.
        x2 = node.get_x()
        y2 = node.get_y()
        mp.plot([x1, x2], [y1, y2], color = colour)
        if (node.numUpnodes() > 0):
            plotstreams(node, colour)  # The recursion.
    

def plotFlowNetwork(originalRaster, flowRaster, title="", plotLakes=True):
    """
    Overlays a FlowRaster onto its associated elevation raster.
    """
    print ("\n\n{}".format(title))
    
    # Added to make the plot more viewable.
    mp.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
    
    # Plot.
    ###fig, ax = mp.subplots(figsize = (36, 24)) # Diagnostic
    
    mp.imshow(originalRaster._data)
    mp.colorbar()
    
    #  Set parameters for plotting streams
    colouri=-1
    colours=["black","red","magenta","yellow","green","cyan","white","orange","grey","brown"]
    
    ###counter = 0 # tempt for finding locations
    # Iterate over all cells.
    for i in range(flowRaster.getRows()):   
        for j in range(flowRaster.getCols()):
            node = flowRaster._data[i,j]

            ###ax.text(j, i, '%.1f'%node.getElevation(),  # Diagnostic
            ###               ha="center", va="center", color="k") # Diagnostic
            
            # Plot pits, associated streams, and if specified and populated, lakes.            
            if (node.getPitFlag()): # dealing with a pit
                mp.scatter(node.get_x(), node.get_y(), color="red")
                ###if counter == 0: # tempt for finding locations
                ###    mp.scatter(node.get_x(), node.get_y(), color = "orange", s = 200) # tempt for finding locations
                ###    counter += 1 # tempt for finding locations
                colouri += 1
                plotstreams(node, colours[colouri % len(colours)])
            if (plotLakes and node.getLakeDepth() > 0): # getLakeDepth() needs to be defined.
                mp.scatter(node.get_x(), node.get_y(), color="blue")
                
                ###ax.text(j, i, '%.1f'%node.getLakeDepth(),  # Diagnostic
                ###           ha="center", va="center", color="orange") # Diagnostic

    mp.show()

def plotExtractedData(flowRaster, extractor, title=""):
    """ Plots data extracted from input FlowRaster."""
    print ("\n\n{}".format(title))
    mp.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
    mp.imshow(flowRaster.extractValues(extractor))  
    mp.colorbar()
    mp.show()

def plotRaster(araster, title=""):
    """Plots a raster."""
    print ("\n\n{}, shape is  {}".format(title, araster.shape))
    
    #*** Added to make plot more viewable.
    mp.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
    mp.imshow(araster)
    mp.colorbar()
    mp.show()


def calculateFlowsAndPlot(elevation, rain, resampleF):
    # plot input rasters
    plotRaster(elevation.getData(), "Original elevation (m)")
    plotRaster(rain.getData(), "Rainfall")
    resampledElevations = elevation.createWithIncreasedCellsize(resampleF)
    
    ################# step 1 find and plot the intial network #######
    fr = flow.FlowRaster(resampledElevations)
        
    plotFlowNetwork(elevation, fr, "Network structure - before lakes", plotLakes=False)
    
    ################Step 2 ######################################
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - constant rain")
    
    ################# step 3 #######################################
    #handle variable rainfall
    fr.addRainfall(rain.getData())
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")
    
    ############# step 4 and step 5 #######################################
    # handle lakes
    fr.calculateLakes()
    plotFlowNetwork(elevation, fr, "Network structure (i.e. watersheds) - with lakes")
    plotExtractedData(fr, flow.LakeDepthExtractor(), "Lake depth")
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")


############# step 1 to 4 #######################################
# Create Random Raster
import numpy as np 
np.random.seed(1)
# Random raster parameters.
rows = 40
cols = 60
xorg = 0.
yorg = 0.
xp = 5
yp = 5
nodata = -999.999
cellsize = 1.
levels = 4
datahi = 100.
datalow = 0
randpercent = 0.2    
resampleFactorA = 1

# Creates random elevation raster.
elevationRasterA = createRanRasterSlope(rows, cols, cellsize, xorg, yorg,
                                        nodata, levels, datahi, datalow,
                                        xp, yp, randpercent)   
# Creates a random slope raster.
rainrasterA = createRanRasterSlope(rows // resampleFactorA,
                                   cols // resampleFactorA,
                                   cellsize * resampleFactorA,
                                   xorg, yorg, nodata, levels,
                                   4000, 1, 36, 4, .1)   

calculateFlowsAndPlot(elevationRasterA, rainrasterA, resampleFactorA)
    
############# step 5 #######################################
# Test with DEM.txt.
path = r'C:\Users\johnd\OneDrive\EdinburghU\Semester 2\OOSE SA\Coursework\myrepo\data'
demfile = r'\DEM.txt'
rainfile = r'\Rainfall.txt'

calculateFlowsAndPlot(readRaster(path + demfile), readRaster(path + rainfile), 10)
#calculateFlowsAndPlot(readRaster('ascifiles/dem_hack.txt'), readRaster('ascifiles/rain_small_hack.txt'), 10)



