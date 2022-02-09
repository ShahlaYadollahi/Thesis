#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:58:37 2021

@author: vsc10412
"""

# module load Spyder/4.1.5-foss-2020a-Python-3.8.2

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt


#%%

ndvi = pd.read_csv("/theia/scratch/brussel/104/vsc10412/ndvi_values.csv", header=None)
s1 = pd.read_csv("/theia/scratch/brussel/104/vsc10412/s1_values.csv", header=None)

round_ndvi = ndvi.round(2)

# zipped = zip(round_ndvi, s1)

ndvi_s1_dic = {}

for i in tqdm(range(len(ndvi),desc = 'Progress'):
    j = round_ndvi.loc[i][0]
    
    if j in ndvi_s1_dic.keys():
        if s1.loc[i][0]>20:
            ndvi_s1_dic[j].append(s1.loc[i][0])
    
    else:
        if s1.loc[i][0]>20:
            ndvi_s1_dic[j]=[]
            ndvi_s1_dic[j].append(s1.loc[i][0])
            
with open('ndvi_s1_dic.csv', 'w') as f:
    for key in ndvi_s1_dic.keys():
        f.write("%s,%s\n"%(key,ndvi_s1_dic[key]))
    
        
#%%
my_data = genfromtxt("/theia/scratch/brussel/104/vsc10412/ndvi_s1_dic.csv", delimiter=',')
x_total =[]
y_total=[]
for i in range(my_data.shape[0]):
    y = list(my_data[i,:])
    y=sorted(y,reverse=True)
    y=y[:20]
    z=my_data[i,0]
    x = [z for j in range(20)]
    x_total.extend(x)
    y_total.extend(y)

x=np.array(x_total)
y=np.array(y_total)

m, b = np.polyfit(x, y, 1)
y_reg = m*x + b
ndvi= genfromtxt("/theia/scratch/brussel/104/vsc10412/ndvi_values.csv")
s1 = genfromtxt("/theia/scratch/brussel/104/vsc10412/s1_values.csv")
plt.figure(figsize=(20,20))
plt.scatter(ndvi,s1)
plt.scatter(x,y)
plt.plot(x, y_reg, color='red',label='y={:.2f}x+{:.2f}'.format(m,b))
plt.show()