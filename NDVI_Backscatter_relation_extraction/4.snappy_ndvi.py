# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:12:25 2021

@author: Shahla
"""

import numpy
import os
from snappy import String
from snappy import Product
from snappy import ProductData
from snappy import ProductUtils
from snappy import jpy
from snappy import ProgressMonitor, VectorDataNode, WKTReader, ProductIO, PlainFeatureFactory,SimpleFeatureBuilder, DefaultGeographicCRS,ListFeatureCollection, FeatureUtils, WKTReader, HashMap, GPF
import pathlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#%%
cwd = os.getcwd()
scences_directory= [os.path.join(filepath,'MTD_MSIL1C.xml') for filepath in pathlib.Path(cwd).glob('*')]
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
def ndvi_maker(subset,name, width, height):
    b4 = subset.getBand('b4')
    b8 = subset.getBand('b8')
    ndviProduct = Product('NDVI', 'NDVI', width, height)
    ndviBand = ndviProduct.addBand('ndvi', ProductData.TYPE_FLOAT32)
    ndviBand.setNoDataValue(numpy.nan)
    ndviBand.setNoDataValueUsed(True)
    ProductUtils.copyGeoCoding(subset, ndviProduct)
    writer = ProductIO.getProductWriter('BEAM-DIMAP')
    ndviProduct.setProductWriter(writer)
    newname='ndvi'+name+'dim'
    ndviProduct.writeHeader(String(newname))

    r4  = numpy.zeros(width, dtype=numpy.float32)
    r8 = numpy.zeros(width, dtype=numpy.float32)

    v4  = numpy.zeros(width, dtype=numpy.uint8)
    v8 = numpy.zeros(width, dtype=numpy.uint8)


    for y in range(height):
        b4.readPixels(0, y, width, 1, r4)
        b8.readPixels(0, y, width, 1, r8)

        b4.readValidMask(0, y, width, 1, v4)
        b8.readValidMask(0, y, width, 1, v8)

        invalidMask4 = numpy.where(v4 == 0, 1, 0)
        invalidMask8 = numpy.where(v8 == 0, 1, 0)

        ma4 = numpy.ma.array(r4, mask=invalidMask4, fill_value=numpy.nan)
        ma8 = numpy.ma.array(r8, mask=invalidMask8, fill_value=numpy.nan)

        ndvi = (ma8 - ma4) / (ma8 + ma4)
        ndviBand.writePixels(0, y, width, 1, ndvi.filled(numpy.nan))

    ndviProduct.closeIO()
#%%


for scene in scences_directory:
    product = ProductIO.readProduct(scene)
    print(product.getName())
    subset = subset_maker(product, geometry)
    name, width, height, desc, band_names = info_derive(subset)
    print(name)
    ndvi_maker(subset, name, width, height)
    print('Done this one')



#%%
'''
sub_b6 = subset.getBand('B6')
print("band read")

print("subset size : ", width, height)
sub_b6_data = np.zeros(width*height, dtype = np.float32)
sub_b6.readPixels(0,0,width,height, sub_b6_data)
sub_b6_data.shape = height, width
print("reading data...")
plt.figure(1)
fig = plt.imshow(sub_b6_data, cmap = cm.gray)
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)
plt.show()
'''


