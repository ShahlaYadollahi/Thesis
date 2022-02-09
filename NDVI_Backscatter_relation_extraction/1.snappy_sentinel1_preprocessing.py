# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 23:08:12 2021

@author: Shahla
"""
import os
from snappy import String
from snappy import Product
from snappy import ProductData
from snappy import ProductUtils
from snappy import jpy
from snappy import ProgressMonitor, VectorDataNode, WKTReader, ProductIO, PlainFeatureFactory,SimpleFeatureBuilder, DefaultGeographicCRS,ListFeatureCollection, FeatureUtils, WKTReader, HashMap, GPF
import gc

#%%
cwd = "/theia/scratch/brussel/104/vsc10412/Sentinel1/"
scences_directory= [os.path.join(cwd, pat) for pat in os.listdir(cwd)]
SubsetOp = jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
wkt = 'POLYGON ((-82.71469116210936 42.34636533160187,-83.15826416015625 42.348395259793,-83.13766479492188 41.96153247330561,-82.694091796875 41.95949009892467,-82.71469116210936 42.34636533160187))'
geometry = WKTReader().read(wkt)


#%%
def subset_maker(product, geometry):
    op = SubsetOp()
    op.setSourceProduct(product)
    op.setGeoRegion(geometry)
    op.setCopyMetadata(True)
    subset = op.getTargetProduct()
    return subset

#%%
def info_derive(subset):
    name = subset.getName()
    width = subset.getSceneRasterWidth()
    height = subset.getSceneRasterHeight()
    desc = subset.getDescription()
    band_names = list(subset.getBandNames())
    return (name, width, height, desc, band_names)

#%%
def do_apply_orbit_file(source):
    print('\tApply orbit file...')
    parameters = HashMap()
    parameters.put('Apply-Orbit-File', True)
    output = GPF.createProduct('Apply-Orbit-File', parameters, source)
    return output

#%%
def do_thermal_noise_removal(source):
    print('\tThermal noise removal...')
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, source)
    return output

#%%
def do_calibration(source, intensity, pols):
    print('\tCalibration...')
    parameters = HashMap()
    parameters.put('outputSigmaBand', False)
    parameters.put('sourceBands', intensity)
    parameters.put('selectedPolarisations', pols)
    parameters.put('outputImageScaleInDb', True)
    output = GPF.createProduct('Calibration', parameters, source)
    return output


#%%
def do_speckle_filtering(source):
    print('\tSpeckle filtering...')
    parameters = HashMap()
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', 5)
    parameters.put('filterSizeY', 5)
    output = GPF.createProduct('Speckle-Filter', parameters, source)
    return output
#%%
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
def do_reprojection(product):
    print('\tReprojection...')
    parameters = HashMap()
    parameters.put('crs', 'EPSG:32617')
    parameters.put('resampling', 'Nearest')
    reprojProduct = GPF.createProduct('Reproject', parameters, product)
    return reprojProduct
#%%
def do_terrain_correction(source, downsample):
    print('\tTerrain correction...')
    parameters = HashMap()
    parameters.put('demName', 'GETASSE30')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    #parameters.put('mapProjection', proj)       # comment this line if no need to convert to UTM/WGS84, default is WGS84
    parameters.put('saveProjectedLocalIncidenceAngle', False)
    parameters.put('saveSelectedSourceBand', True)
    while downsample == 1:                      # downsample: 1 -- need downsample to 40m, 0 -- no need to downsample
        parameters.put('pixelSpacingInMeter', 10.0)
        break
    output = GPF.createProduct('Terrain-Correction', parameters, source)
    return output

def linear_to_db(product):
    parameters = HashMap()
    lineartodb = GPF.createProduct('linearToFromdB', parameters, product)
    return lineartodb

def getResampled(product, resolution):
    # TODO: this should be tested!!!
    # More info: http://forum.step.esa.int/t/aggregation-and-interpolation-of-sentinel-products-should-i-use-snappy-or-gdal-tools/2522/3
    parameters = HashMap()
    parameters.put('sourceProduct', product)
    parameters.put('upsampling', "Bilinear")
    parameters.put('downsampling', "Mean")
    # As I checked in SNAP desktop, 'targetResolution' option is sometimes not available
    # and I need to use targetHeight and targetWidth instead
    # RuntimeError: org.esa.snap.core.gpf.OperatorException: Operator 'ResamplingOp': Value for 'Target resolution' must be of type 'Integer'.
    # So I convert it to Integer
    parameters.put('targetResolution', int(resolution))
    result = GPF.createProduct('Resample', parameters, product)
    return result    

#%%
for scene in scences_directory:
    product = ProductIO.readProduct(scene)
    print(product.getName())
    name, width, height, desc, band_names = info_derive(product)
    orbit_applied = do_apply_orbit_file(product)
    thermal_removed = do_thermal_noise_removal(orbit_applied)
    calibrated = do_calibration(thermal_removed, 'Intensity_VV', 'VV')

    speckle_filtered = do_speckle_filtering(calibrated)

    terrain_corrected = do_terrain_correction(speckle_filtered, 1)

    reprojected = do_reprojection(terrain_corrected)
    lineartodb = linear_to_db(reprojected)
    resampled = getResampled(lineartodb, 10)
    subset = subset_maker(resampled, geometry)
    print(info_derive(subset))
    output_name = "preprocessed_"+name
    ProductIO.writeProduct(subset, output_name, 'GeoTiff')
    os.remove(scene)
    orbit_applied=0
    thermal_removed =0
    calibrated = 0
    speckle_filtered = 0
    terrain_corrected = 0
    reprojected =0 
    lineartodb = 0
    resampled=0
    subset = 0
    gc.collect()

