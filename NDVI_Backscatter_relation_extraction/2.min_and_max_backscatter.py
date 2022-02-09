import os 
import gdal
import numpy as np
import glob


directory = os.getcwd()
dataset_paths = glob.glob(os.path.join(directory, '*.tif'))
dataset= gdal.Open(dataset_paths[0])
metadata = {}
metadata['array_rows'] = dataset.RasterYSize
metadata['array_cols'] = dataset.RasterXSize
mapinfo = dataset.GetGeoTransform()
metadata['projection'] = dataset.GetProjection()

first_file = dataset.GetRasterBand(1).ReadAsArray(0,0,dataset.RasterXSize,dataset.RasterYSize).astype(np.float)
i = 0
for index, file in enumerate(dataset_paths):
 if index ==0:
  minimum_array = first_file
  maximum_array = first_file
 f = gdal.Open(file)
 dataset = f.GetRasterBand(1).ReadAsArray(0,0,f.RasterXSize,f.RasterYSize).astype(np.float)
 if dataset.shape[0]==4331:
  dataset = np.delete(dataset, 4330, 0)
 if dataset.shape[1]==5169:
  dataset = np.delete(dataset, 5168, 1)

 minimum_array = np.minimum(minimum_array, dataset)
 maximum_array = np.maximum(maximum_array, dataset)
 print('Processing is done for the raster: ',i)
 i+=1



driver = gdal.GetDriverByName("GTiff")
dsOut = driver.Create("minimum_backscatter_signal_2020.tif", metadata['array_cols'],metadata['array_rows'], 1,gdal.GDT_Float32, ['TFW=YES', 'NUM_THREADS=1'])
dsOut.SetGeoTransform(mapinfo)
dsOut.SetProjection(metadata['projection'] )
dsOut.GetRasterBand(1).WriteArray(minimum_array)
print("Done this one", minimum_array.shape)
dsOut = None

dsOut = driver.Create("maximum_backscatter_signal_2020.tif", metadata['array_cols'],metadata['array_rows'], 1,gdal.GDT_Float32, ['TFW=YES', 'NUM_THREADS=1'])
dsOut.SetGeoTransform(mapinfo)
dsOut.SetProjection(metadata['projection'] )
dsOut.GetRasterBand(1).WriteArray(maximum_array)
print("Done this one", maximum_array.shape)
dsOut = None
