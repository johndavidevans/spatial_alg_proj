from RasterHandler import createRanRasterSlope
from RasterHandler import readRaster
import matplotlib.pyplot as mp
import Flow as flow
import numpy as np
import argparse

def getCmdArgs():
    """
    Get commndline arguments.
    """
    # Create an argparse object.
    p = argparse.ArgumentParser(description = ('For passing Coursework args.'))
    
    # Define arguments.
    p.add_argument('--DEM', 
                   dest='DEM', 
                   type=bool, 
                   default=False, 
                   help=("Run for DEM file. Default is False."))
    p.add_argument('--path',
                   dest='path',
                   type=str, 
                   default = "../data", 
                   help = ("Path to DEM and rain data. Default is ../data."))
    p.add_argument('--df', 
                   dest='demfile', 
                   type=str, 
                   default="\DEM.txt", 
                   help=("DEM file name. Default is \DEM.txt."))
    p.add_argument('--rf',
                   dest='rainfile',
                   type=str, 
                   default="\Rainfall.txt", 
                   help=("Path to DEM and rain data. Default is \Rainfall.txt.")) 
    
    cmdargs = p.parse_args()
    
    # Returns commandline arguments as an object.
    return cmdargs


def plotstreams(flownode, colour):
    """Plots streams by recursing up until reaching a node with no upnodes."""
    for node in flownode.getUpnodes():
        # Gets coords of node passed, and recursively plot line to
        # each of its upnodes.
        x1 = flownode.get_x()
        y1 = flownode.get_y()
        x2 = node.get_x()
        y2 = node.get_y()
        mp.plot([x1, x2], [y1, y2], color = colour)
        if (node.numUpnodes() > 0):
            plotstreams(node, colour)  # The recursion.
    
def plotFlowNetwork(originalRaster, flowRaster, title="", plotLakes=True):
    """Overlays a FlowRaster onto its associated elevation raster."""
    print ("\n\n{}".format(title))
    
    # Added to improve viewability.
    mp.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    mp.title(label = ("\n\n{}".format(title)),
             fontdict = {'fontsize':24})
    
    # Plot.    
    mp.imshow(originalRaster._data)
    mp.colorbar()
    
    #  Set parameters for plotting streams
    colouri = -1
    colours = ["black", "red", "magenta", "yellow", "green", "cyan", "white", 
               "orange", "grey", "brown"]
    
    # Plot pits, associated streams, and if specified and populated, lakes.
    for i in range(flowRaster.getRows()):   
        for j in range(flowRaster.getCols()):
            node = flowRaster._data[i,j]
            
            if (node.getPitFlag()): # dealing with a pit
                mp.scatter(node.get_x(), node.get_y(), color="red")
                colouri += 1
                plotstreams(node, colours[colouri % len(colours)])
            if (plotLakes and node.getLakeDepth() > 0):
                mp.scatter(node.get_x(), node.get_y(), color="deepskyblue")

    mp.show()

def plotExtractedData(flowRaster, extractor, title=""):
    """ Plots data extracted from input FlowRaster."""
    print ("\n\n{}".format(title))
    mp.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    mp.imshow(flowRaster.extractValues(extractor))  
    mp.colorbar()
    mp.title(label = ("\n\n{}".format(title)),
             fontdict = {'fontsize':24})
    mp.show()

def plotRaster(araster, title=""):
    """Plots a raster."""
    print ("\n\n{}, shape is  {}".format(title, araster.shape))
    
    # Added improve viewability.
    mp.figure(num=None, figsize=(15, 10), dpi=80, facecolor='w', edgecolor='k')
    mp.imshow(araster)
    mp.colorbar()
    mp.title(label = ("\n\n{}, shape is  {}".format(title, araster.shape)),
             fontdict = {'fontsize':24})
    mp.show()


def calculateFlowsAndPlot(elevation, rain, resampleF, tasks = ['1','2','3','4','5']):
    """
    The main function to execute the project. Processes elevation and rain
    data, producing a series of plots of elevations, flow networks, and lake
    depths.
    """
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

    ############# Answer questions for step 5 #############################
    values = fr.extractValues(flow.FlowExtractor())

    # Max
    maxflow = np.max(values)
    
    # Row
    rowMax = np.where(values == maxflow)[0][0]
    # Col
    colMax = np.where(values == maxflow)[1][0]
    
    # Print message
    print("Maximum flow of\n\n{} found in node [{},{}]".format(maxflow, rowMax, colMax))
    

############# Command Line Functionality ###################
if __name__ == '__main__':

    # read the command line
    cmdargs = getCmdArgs()

    if cmdargs.DEM:
        path = cmdargs.path
        demfile = cmdargs.demfile
        rainfile = cmdargs.rainfile
        calculateFlowsAndPlot(readRaster(path + demfile), 
                              readRaster(path + rainfile), 
                              10)

    else:
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
                          #tasks = cmdargs.tasks)

  #l = rand_gen(bottom = cmdargs.minimum, top = cmdargs.maximum, length = cmdargs.list_length)
  #print(l)
  
