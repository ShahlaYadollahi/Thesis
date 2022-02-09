# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 21:46:57 2021

@author: Shahla
"""

import glob
import os
import gdal 
import numpy as np
import csv


common= ['06/08/2020', '10/06/2020', '07/03/2020', '10/31/2020']
common_dates = ['20200608', '20201006', '20200703', '20201031']

ndvi_path = glob.glob(os.path.join("/theia/scratch/brussel/104/vsc10412/NDVI/", '*.tif'))
s1_path = glob.glob(os.path.join("/theia/scratch/brussel/104/vsc10412/delta_backscattered_sentinel1/", '*.tif'))

s1_ndvi = {}
xs=[]
ys=[]
for i in common_dates:
  for j in ndvi_path:
    if i==j[63:71]:
      for k in s1_path:
        if i==k[95:103]:
          print(j, k)
          stacks=[]
          s1 = gdal.Open(k)
          ndvi = gdal.Open(j)
          s1_array = s1.GetRasterBand(1).ReadAsArray(0,0).astype(np.float)
          ndvi_array = ndvi.GetRasterBand(1).ReadAsArray().astype(np.float)
          print(s1_array.shape)
          for a in range(s1_array.shape[0]):
            for b in range(s1_array.shape[1]):
              if ndvi_array[a,b] < 0.8 and ndvi_array[a,b]>0.1:
                xs.append([ndvi_array[a,b]])
                ys.append([s1_array[a,b]])




with open('ndvi_values.csv', 'w') as f:
  write = csv.writer(f) 
  write.writerows(xs)

with open('s1_values.csv', 'w') as f:
  write = csv.writer(f) 
  write.writerows(ys)
