"# oosa-final-assignment-s1871317"
Exam No B131587
_____________________________________________
These modules estimate rainfall-adjusted waterflow rates across a given topography,
presenting the results in a seris of charts and some printed messages. Much of the
code was developed prior to this assignment, but much has also been added and amended.
Comments and docstrings outline the functions used and what they do.
_____________________________________________
The files contained are:
ProjectReport_B131587.docx - the requested report

src\Points.py - defines the Point2d object.

src\Raster.py - defines the Raster objects.

src\RasterHandler.py - functions to create raster, including random slopes.

src\Flow.py - defines the FlowNode and FlowRaster objects, through which most analysis is performed, as well as a couple of helper classes.

src\CourseWork1.py - the driver originally provided with comments and some minor modifications to improve chart viewability. To execute successfully, the path, demfile, and rainfile variables may require updating.

src\CourseWork1_argparse.py - a modified version of CourseWork1.py, with basic command line parsing
enabled. This file also calculates and prints the answers to the questions in Task 5.

Four arguments have been enabled:
--DEM if True causes the calculateFlowsAndPlot() function to be called on a specified DEM and rain file. Defaults to false, and randome slopes are generated and processed.
--path allows definition of the location of the files to be processed with DEM enabled. Defaults to ../data.
--df allows the DEM file name to be specified. Defaults to \DEM.txt.
--rf allows the rain file name to be specified. Defaults to \Rainfall.txt.

Example:
>python CourseWork1_argparse.py --DEM True --path C:\files --df \newDEM.txt --rf \newRainfall.txt

would process the DEM and rain data in C:\files\newDem.txt and c:\newRainfall.txt and print the results to screen.
