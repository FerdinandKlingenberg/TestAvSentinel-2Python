# -*- coding: utf-8 -*-

import rasterio
import cv2
#import numpy as np


outfile = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Resultater\rasterio\GDAL_Composite8bitWithOpenCV.tif'
#url to the bands
b4 = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Originalscener\B04.jp2'
b3 = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Originalscener\B03.jp2'
b2 = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Originalscener\B02.jp2'
gdalLaget = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Resultater\OTB\exportOTB_Composite8bit.tif'

#open the bands (I can't believe how easy is this with rasterio!)
with rasterio.open(b4) as red:
    RED = red.read()
with rasterio.open(b3) as green:
    GREEN = green.read()
with rasterio.open(b2) as blue:
    BLUE = blue.read()
with rasterio.open(gdalLaget) as comp:
    COMP = comp.read()
    

#compute the ndvi
#ndvi = (NIR-RED)/(NIR+RED)
#ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR+RED)
#print(ndvi.min(), ndvi.max()) The problem is alredy here
outputImg8U = cv2.convertScaleAbs(COMP, alpha=(255.0/65535.0))


profile = comp.meta
profile.update(driver='GTiff')
#profile.update(dtype=rasterio.float32)
profile.update(dtype=rasterio.uint8)
#profile.update(count=3)

with rasterio.open(outfile, 'w', **profile) as dst:
#    dst.write(outputImg8U)
    dst.write(outputImg8U.astype(rasterio.uint8))
#    dst.write(ndvi.astype(rasterio.float32))

