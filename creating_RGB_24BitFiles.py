# -*- coding: utf-8 -*-

import rasterio

outfile = r'C:\Users\Ferdinand\Documents\imageEnhance_to24bit\Resultater\rasterio\ndvi.tif'
#url to the bands
b4 = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/V/NL/2017/8/11/0/B04.jp2'
b3 = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/V/NL/2017/8/11/0/B03.jp2'
b2 = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/V/NL/2017/8/11/0/B02.jp2'

#open the bands (I can't believe how easy is this with rasterio!)
with rasterio.open(b4) as red:
    RED = red.read()
with rasterio.open(b3) as green:
    GREEN = green.read()
with rasterio.open(b2) as blue:
    BLUE = blue.read()

#compute the ndvi
#ndvi = (NIR-RED)/(NIR+RED)
ndvi = (NIR.astype(float) - RED.astype(float)) / (NIR+RED)
#print(ndvi.min(), ndvi.max()) The problem is alredy here

profile = red.meta
profile.update(driver='GTiff')
#profile.update(dtype=rasterio.float32)
profile.update(dtype=rasterio.uint8)
profile.update(count=3)

with rasterio.open(outfile, 'w', **profile) as dst:
    dst.write(ndvi.astype(rasterio.uint8))
#    dst.write(ndvi.astype(rasterio.float32))

