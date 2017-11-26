# -*- coding: utf-8 -*-
from osgeo import gdal
import sys
import numpy as np

gdal.UseExceptions()

# Initialize input/output names
redBand = ""
greenBand = ""
blueBand = ""

def Usage():
    print("""
    $ getrasterband.py [ band number ] input-raster (any Sentinel-2 band is optionally)
    """)
    sys.exit(1)
    
def calcStats(inputBand):
    inputBand.ComputeStatistics(0)
        

def main( band_num, input_file ):
    redBand = input_file[:-7] + "B04.jp2"
    greenBand = input_file[:-7] + "B03.jp2"
    blueBand = input_file[:-7] + "B02.jp2"
    src_ds = gdal.Open( input_file )
    src_ds_RedRaster = gdal.Open(redBand)
    src_ds_GreenRaster = gdal.Open(greenBand)
    src_ds_BlueRaster = gdal.Open(blueBand)
    if src_ds is None:
        print 'Unable to open %s' % input_file
        sys.exit(1)

    try:
        srcband_Red = src_ds_RedRaster.GetRasterBand(band_num)
        srcband_Green = src_ds_GreenRaster.GetRasterBand(band_num)
        srcband_Blue = src_ds_BlueRaster.GetRasterBand(band_num)

        # Force statistics on the band
        srcband_Red.ComputeStatistics(0)
        srcband_Green.ComputeStatistics(0)
        srcband_Blue.ComputeStatistics(0)

    except RuntimeError, e:
        print 'No band %i found' % band_num
        print e
        sys.exit(1)

    """
    Want to store the absolute maximum and minimum for
    between the three bands
    """
    maximumList = np.array([srcband_Red.GetMaximum(),
                            srcband_Green.GetMaximum(),
                            srcband_Blue.GetMaximum()])
    minimumList = np.array([srcband_Red.GetMinimum(),
                            srcband_Green.GetMinimum(),
                            srcband_Blue.GetMinimum()])

    maxInt = maximumList.max()
    minInt = minimumList.min()
    print u'Den maksimale verdien for alle båndene', maxInt
    print u'Den minimale verdien for alle båndene', minInt
    
    # Inspired from https://gis.stackexchange.com/a/223920
    tifs = [redBand, greenBand, blueBand]
    outvrt = "C:\Users\Ferdinand\Documents\imageCreationGDALPythonScripts\temp.vrt"
    outtif = "C:\Users\Ferdinand\Documents\imageCreationGDALPythonScripts\stacked.tif"
    outds = gdal.BuildVRT(outvrt, tifs, separate=True)
    outds = gdal.Translate(outtif,
                           outds,
                           scaleParams = [[minInt, maxInt, 0 , 255]], 
                           exponents = [0.5, 0.5, 0.5],
                           creationOptions = ['PHOTOMETRIC=RGB'],
                           outputType = gdal.GDT_Byte)
    outds = None

if __name__ == '__main__':

    if len( sys.argv ) < 3:
        print """
        [ ERROR ] you must supply at least two arguments:
        1) the band number to retrieve and 2) input raster
        """
        Usage()

    main( int(sys.argv[1]), sys.argv[2] )
