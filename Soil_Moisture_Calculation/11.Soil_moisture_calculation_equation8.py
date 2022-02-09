#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 13:18:45 2021

@author: vsc10412
"""

import os
import glob
import numpy as np
import gdal
from osgeo import osr
#%%


def CreateGeoTiff(Name, Array, driver, NDV, xsize, ysize, GeoT, Projection):
    """Function creates a geotiff file from a Numpy Array.
    Name: output file
    Array: numpy array to save
    """
    datatypes = {"uint8": 1, "int8": 1, "uint16": 2, "int16": 3, "Int16": 3, "uint32": 4,
    "int32": 5, "float32": 6, "float64": 7, "complex64": 10, "complex128": 11,
    "Int32": 5, "Float32": 6, "Float64": 7, "Complex64": 10, "Complex128": 11,}
    DataSet = driver.Create(Name,xsize,ysize,1,datatypes[Array.dtype.name])
    if NDV is None:
        NDV = -9999
    Array[np.isnan(Array)] = NDV
    DataSet.GetRasterBand(1).SetNoDataValue(NDV)
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection(Projection.ExportToWkt())
    DataSet.GetRasterBand(1).WriteArray(Array)
    DataSet = None
    
def GetGeoInfo(filename, Subdataset = 0):
    """Gives geo-information derived from a georeferenced map
    
    filename: file to be scrutinized
    subdataset: layer to be used in case of HDF4 format
    """
    SourceDS = gdal.Open(filename, gdal.GA_ReadOnly)
    Type = SourceDS.GetDriver().ShortName
    if Type == 'HDF4' or Type == 'netCDF':
        SourceDS = gdal.Open(SourceDS.GetSubDatasets()[Subdataset][0])
    NDV = SourceDS.GetRasterBand(1).GetNoDataValue()
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    #DataType = SourceDS.GetRasterBand(1).DataType
    #DataType = gdal.GetDataTypeName(DataType)
    driver = gdal.GetDriverByName(Type)
    return driver, NDV, xsize, ysize, GeoT, Projection#, DataType
driver, NDV, xsize, ysize, GeoT, Projection = GetGeoInfo(ndvi_directory[0])

#%%
os.chdir("/theia/scratch/brussel/104/vsc10412/results_mvmin0025/")

ndvi_path = "/theia/scratch/brussel/104/vsc10412/NDVI/"
backscatter_path = "/theia/scratch/brussel/104/vsc10412/delta_backscattered_sentinel1/"

ndvi_directory= glob.glob(os.path.join(ndvi_path, '*.tif'))
backscatter_directory = glob.glob(os.path.join(backscatter_path, '*.tif'))

ndvi_dates=[x[63:71] for x in ndvi_directory]
backscatter_dates = [x[95:103] for x in backscatter_directory]

common_dates_indices={}

common_dates_indices[18]=[22,34]
common_dates_indices[20]=[39,3]
common_dates_indices[1]=[27,33]
common_dates_indices[11]=[54,18,50,17]
common_dates_indices[15]=[36,38]
common_dates_indices[19]=[23,29]
common_dates_indices[4]=[14,26]
common_dates_indices[2]=[25,45]
common_dates_indices[21]=[28,10]
common_dates_indices[0]=[31]     
common_dates_indices[8]=[13,24]
common_dates_indices[16]=[44,20]
common_dates_indices[9]=[19,12]
common_dates_indices[7]=[51]
common_dates_indices[6]=[43,35]
common_dates_indices[5]=[0,9]
common_dates_indices[14]=[57,7]
common_dates_indices[17]=[52,2]  
m=-26.572
b=45.914
mv_min = 0.025879696

mv_max = 0.5
mv_diff = mv_max-mv_min

for i in common_dates_indices.keys():
    ds = gdal.Open(ndvi_directory[i])
    ndvi = np.array(ds.GetRasterBand(1).ReadAsArray())
    f = common_dates_indices[i]
    for j in f:
        ts = gdal.Open(backscatter_directory[j])
        backscatter = np.array(ts.GetRasterBand(1).ReadAsArray())
        f_ndvi = m*ndvi+b
        mv = mv_diff*np.divide(backscatter,f_ndvi)+mv_min
        CreateGeoTiff('Mositure_'+backscatter_dates[j]+'.tif',mv, driver, NDV, xsize, ysize, GeoT, Projection)
    
