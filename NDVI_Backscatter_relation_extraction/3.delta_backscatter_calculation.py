# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:53:06 2021

@author: Shahla
"""
import gdal 
import numpy as np
import os
import glob

#%%
directory = os.getcwd()
dataset_paths = glob.glob(os.path.join(directory, '*.tif'))
dataset= gdal.Open(dataset_paths[0])
ysize = dataset.RasterYSize
xsize = dataset.RasterXSize
mapinfo = dataset.GetGeoTransform()
proj = dataset.GetProjection()
driver = gdal.GetDriverByName("GTiff")

min_raster = gdal.Open("E:\Thesis\datasets\StudyArea\minimum_backscatter_signal_2020.tif")
min_backscatter = min_raster.GetRasterBand(1).ReadAsArray(0,0,xsize,ysize).astype(np.float)

for file in dataset_paths:
    outname = 'deltaSignal'+file.split('dB_')[1]
    f = gdal.Open(file)
    backscatter = f.GetRasterBand(1).ReadAsArray(0,0,xsize,ysize).astype(np.float)
    delta_backscatter = backscatter - min_backscatter
    dsOut = driver.Create(outname, xsize, ysize, 1,gdal.GDT_Float32, ['TFW=YES', 'NUM_THREADS=1'])
    dsOut.SetGeoTransform(mapinfo)
    dsOut.SetProjection(proj)
    dsOut.GetRasterBand(1).WriteArray(delta_backscatter)
    print("Done this one")
    dsOut = None