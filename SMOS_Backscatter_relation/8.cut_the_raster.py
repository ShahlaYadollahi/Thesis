#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:05:33 2021

@author: vsc10412
"""

import gdal
import pathlib
import glob
import os

#%% 

#cutting preprocessed sentinel1 to SMOS bounds
gdal.UseExceptions()
os.chdir("/theia/scratch/brussel/104/vsc10412/cut_preprocessed_sentinel/")

shpin = "/theia/scratch/brussel/104/vsc10412/s1_smos_intersect.shp"
in_path = "/theia/scratch/brussel/104/vsc10412/preprocessed_sentinel1/"

data_dir = pathlib.Path(in_path)
files = glob.glob(os.path.join(in_path, "*.tif"))

for rasin in files:

    rasout =rasin[:-4]+'_cut.tif'
    result = gdal.Warp(rasout, rasin, cutlineDSName=shpin, cropToCutline=True)