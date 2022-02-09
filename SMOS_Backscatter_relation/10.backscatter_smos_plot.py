#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 20:38:58 2021

@author: vsc10412
"""
#reading timeseries

import pandas as pd
import matplotlib as plt
import os

#%%
os.chdir("/theia/scratch/brussel/104/vsc10412/")

ascending_smos_data=pd.read_csv("/theia/scratch/brussel/104/vsc10412/a_cell_info.csv",header=None)
descending_smos_data=pd.read_csv("/theia/scratch/brussel/104/vsc10412/d_cell_info.csv",header=None)

backscatter_data = pd.read_csv("/theia/scratch/brussel/104/vsc10412/backscatter_timeseries.csv",header=None)

dates = [backscatter_data.iloc[i][0] for i in range(58)]

smos_backscatter_dic = {}

for d in dates:
    
    backscatter = backscatter_data[(backscatter_data==d).any(1)].stack()[lambda x: x != d].unique()
    smos = descending_smos_data[(descending_smos_data==d).any(1)].stack()[lambda x: x != d].unique()
    if smos.size>0:
        smos_backscatter_dic[backscatter[0]]=smos[0]
        
plt.pyplot.scatter(smos_backscatter_dic.values(),smos_backscatter_dic.keys())

df=pd.DataFrame.from_dict(smos_backscatter_dic,orient='index')
df.to_csv("smos_backscatter_descending.csv")

for d in dates:
    
    backscatter = backscatter_data[(backscatter_data==d).any(1)].stack()[lambda x: x != d].unique()
    smos = ascending_smos_data[(ascending_smos_data==d).any(1)].stack()[lambda x: x != d].unique()
    if smos.size>0:
        smos_backscatter_dic[backscatter[0]]=smos[0]
        
plt.pyplot.scatter(smos_backscatter_dic.values(),smos_backscatter_dic.keys())

df=pd.DataFrame.from_dict(smos_backscatter_dic,orient='index')
df.to_csv("smos_backscatter_ascending.csv")
