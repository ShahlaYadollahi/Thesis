import rasterio
import numpy as np
from glob import glob
import pandas as pd
import os

#%%
data_dir = "/theia/scratch/brussel/104/vsc10412/cut_preprocessed_sentinel/"
file_list = glob(os.path.join(data_dir, '*.tif'))

def read_file(file):
    with rasterio.open(file) as src:
        return(src.read(1))

# Read all data as a list of numpy arrays 
array_list = [read_file(x) for x in file_list]
# Perform averaging
mean_list=[np.mean(file) for file in array_list]

dates = [file[95:103] for file in file_list]

data={'date':dates, 'raster_mean':mean_list}
df=pd.DataFrame(data)

os.chdir("/theia/scratch/brussel/104/vsc10412/")

df.to_csv('backscatter_timeseries.csv')
