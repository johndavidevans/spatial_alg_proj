# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:07:23 2019

@author: johnd
"""
from matplotlib import pyplot as plt

path = r'C:\Users\johnd\OneDrive\EdinburghU\Semester 2\OOSE SA\Coursework\myrepo\data'
file = '\DEM.txt'

from RasterHandler import readRaster
from Raster import Raster
from Flow import FlowRaster

r = readRaster((path + file))

xs = range(r.getCols())
ys = range(r.getRows())

import CourseWork1