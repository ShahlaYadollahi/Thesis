# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 08:33:26 2021

@author: Shahla

module load  Spyder/4.1.5-foss-2020a-Python-3.8.2
module load netcdf4-python/1.5.3-foss-2020a-Python-3.8.2
module load Cartopy/0.18.0-foss-2020a-Python-3.8.2
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import csv

#%%
os.chdir("/theia/scratch/brussel/104/vsc10412/DA_TC_MIR_CL_31/")
smos_directory= glob.glob(os.path.join(os.getcwd(), '*.nc'))
ascending={}
descending={}

for ncfile in smos_directory:
    nc_fid = Dataset(ncfile, 'r')
    # Extract data from NetCDF file
    time = ncfile[75:83]
    soil_moisture = nc_fid.variables['Soil_Moisture'][:][2,5]
    if ncfile[73]=="A":
        ascending[time]=soil_moisture
    if ncfile[73]=="D":
        descending[time]=soil_moisture
        
with open('ascending_smos.csv', 'w') as csvfile:
    for key in ascending.keys():
        csvfile.write("%s,%s\n"%(key,ascending[key]))


with open('descending_smos.csv', 'w') as csvfile:
    for key in descending.keys():
        csvfile.write("%s,%s\n"%(key,descending[key]))