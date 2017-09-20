import sys
#sys.path.append('/home/fklingenberg/.snap/snap-python')
sys.path.append('/home/fklingenberg/.snap/snap-python/snappy')
import snappy
from snappy import ProductIO
from snappy import Product
from snappy import ProductData
from snappy import GPF
from snappy import jpy
from snappy import ProductUtils
from snappy import FlagCoding
import numpy
import string
import matplotlib.pylab as plt
import os,time,tarfile,glob
#folder = '/media/fklingenberg/Expansion Drive/D/t'
#filepathresultat = '/media/fklingenberg/Expansion Drive/D/results'
folder = '/home/fklingenberg/Documents/Mosaicing_python/Data2/2'
filepathresultat = '/home/fklingenberg/Documents/Mosaicing_python/Data2/resultsL1C'

teller = 0
resampleProduct1PathOgNavn=""
resampleProduct2PathOgNavn=""

print("Begin geoprocessing: "+time.strftime("%X"))
time.clock()

#for name in glob.glob(folder+'/S2A_USER*/GRANULE/*/IMG_DATA/R20m/*_B11_20m.jp2'):
for name in glob.glob(folder+'/S2A*/GRANULE/*/IMG_DATA/*_B11.jp2'):
    (filepath, filename) = os.path.split(name)
    ny = ""
    ny = filepath+'/'+filename
    
    product = ProductIO.readProduct(ny)
    width = product.getSceneRasterWidth()
    height = product.getSceneRasterHeight()
    namee = product.getName()
    description = product.getDescription()
    band_names = product.getBandNames()
    print("Product: %s, %d x %d pixels, %s" % (namee, width, height, description))
    print("Bands:   %s" % (list(band_names)))
    
    HashMap = snappy.jpy.get_type('java.util.HashMap')    
    snappy.GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    
    parameters.put('targetResolution', 10)
    parameters.put('upsampling', 'Nearest')
    parameters.put('downsampling', 'First')
    parameters.put('flagDownsampling', 'First')
    parameters.put('resampleOnPyramidLevels', 'false')

    result = snappy.GPF.createProduct('Resample', parameters, product)
    
    print("Writing...")
    (shortname, extension) = os.path.splitext(filename)
    resultatName = ""
   # resultatName = filepathresultat+'/'+shortname+'_resample.tif'
    resultatName = filepathresultat+'/'+shortname+'_resample.dim'

    
   # ProductIO.writeProduct(result, resultatName, 'GeoTIFF')
    ProductIO.writeProduct(result, resultatName, 'BEAM-DIMAP')
    result.closeIO()
    
    teller=teller+1
    if teller == 1:
        resampleProduct1PathOgNavn = resultatName
        print(resampleProduct1PathOgNavn)
    elif teller == 2:
        resampleProduct2PathOgNavn = resultatName
        print(resampleProduct2PathOgNavn)
    
    print("Done.")
    
    
#for name in glob.glob(filepathresultat+'/_resample.dim'):

# Read resampled band 11 and set height and width constants
product1 = ProductIO.readProduct(resampleProduct1PathOgNavn)
Product1_band = product1.getBand('band_1')
product2 = ProductIO.readProduct(resampleProduct2PathOgNavn)
Product2_band = product2.getBand('band_1')

# Read the NDVI bands
# Hint from https://stackoverflow.com/a/3675423
def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

tempNDVI_1 = resampleProduct1PathOgNavn
tempNDVI_2 = resampleProduct2PathOgNavn

ndvi1navn = replace_last(tempNDVI_1, 'B11_resample.dim', 'ndvi.dim')
ndvi2navn = replace_last(tempNDVI_2, 'B11_resample.dim', 'ndvi.dim')

ndviProduct1 = ProductIO.readProduct(ndvi1navn)
ndvi1_band = ndviProduct1.getBand('ndvi')
ndviProduct2 = ProductIO.readProduct(ndvi2navn)
ndvi2_band = ndviProduct2.getBand('ndvi')


# File information to product master raster
width = product1.getSceneRasterWidth()
height = product1.getSceneRasterHeight()
name = product1.getName()
description = product1.getDescription()
band_names = product1.getBandNames()

# setting up created product
masterProduct = Product('ResampleBest', 'ResampleBest', width, height)
masterBand = masterProduct.addBand('resampleBest', ProductData.TYPE_FLOAT32)
writer = ProductIO.getProductWriter('GeoTIFF')

ProductUtils.copyGeoCoding(product1, masterProduct)


masterProduct.setProductWriter(writer)
masterProduct.writeHeader('resampleMasterProduct.tif')

# Create variables numpy
array1 = numpy.zeros((width, height), dtype=numpy.float32)  
array2 = numpy.zeros((width, height), dtype=numpy.float32) 

array1_ndvi1 = numpy.zeros((width, height), dtype=numpy.float32)  
array2_ndvi2 = numpy.zeros((width, height), dtype=numpy.float32) 

temp = numpy.zeros((width, height), dtype=numpy.float32)  

array1 = Product1_band.readPixels(0, 0, width-1, height-1, array1)
array2 = Product2_band.readPixels(0, 0, width-1, height-1, array2)

array1_ndvi1 = ndvi1_band.readPixels(0, 0, width-1, height-1, array1_ndvi1)
array2_ndvi2 = ndvi2_band.readPixels(0, 0, width-1, height-1, array2_ndvi2)

print("Calculating...")


for x in range(width):
    for y in range(height):
        if array1[x,y] < array2[x,y] and array1_ndvi1[x,y] > array2_ndvi2[x,y]:
            temp[x,y] = array1[x,y]
        else:
            temp[x,y] = array2[x,y]
#        elif array1[x,y] < array2[x,y] and array1_ndvi1[x,y] < array2_ndvi2[x,y]:
#            temp[x,y] = array2[x,y]
#       elif array1[x,y] > array2[x,y] and array1_ndvi1[x,y] > array2_ndvi2[x,y]:
#            temp[x,y] = array2[x,y]
#        elif array1[x,y] > array2[x,y] and array1_ndvi1[x,y] < array2_ndvi2[x,y]:
#            temp[x,y] = array1[x,y]
#        elif array1[x,y] == array2[x,y] and array1_ndvi1[x,y] < array2_ndvi2[x,y]:
#            temp[x,y] = array2[x,y]
#        elif array1[x,y] == array2[x,y] and array1_ndvi1[x,y] > array2_ndvi2[x,y]:
#            temp[x,y] = array1[x,y]
#        elif array1[x,y] == array2[x,y] and array1_ndvi1[x,y] == array2_ndvi2[x,y]:
#            temp[x,y] = array1[x,y] #just chose one...
        

#for x in range(width):
#    for y in range(height):
#        temp[x,y] = array1[x,y] if array1[x,y] < array2[x,y] else array2[x,y]
        

masterBand.writePixels(0, 0, width-1, height-1, temp)
masterProduct.closeIO()



print("End geoprocessing: "+time.strftime("%X"))
seconds = time.clock()
hours = seconds // (60*60)
seconds %= (60*60)
minutes = seconds // 60
seconds %= 60
if hours < 1:
    if minutes < 1:
        print("Elapsed time: "+str(int(seconds))+"sec")
    else:
        print("Elapsed time: "+str(int(minutes))+"min and "+ str(int(seconds))+"sec")
else:
    print("Elapsed time: " + str(int(hours))+"h, "+str(int(minutes))+"min and "+str(int(seconds))+"sec")


# In[ ]:




# In[ ]:




# In[6]:

tempNDVI_1 = resampleProduct1PathOgNavn
tempNDVI_2 = resampleProduct2PathOgNavn

ndvi1navn = replace_last(tempNDVI_1, 'B11_resample.dim', 'ndvi.dim')
ndvi2navn = replace_last(tempNDVI_2, 'B11_resample.dim', 'ndvi.dim')

ndviProduct1 = ProductIO.readProduct(ndvi1navn)
#Product1_band = product1.getBand('band_1')
ndviProduct2 = ProductIO.readProduct(ndvi2navn)
#Product2_band = product2.getBand('band_1')



print ("NDVI band name er:")
band_names = ndviProduct2.getBandNames()
print("Bands:   %s" % (list(band_names)))


# In[4]:

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

s = resampleProduct1PathOgNavn
r = replace_last(s, 'B11_resample.dim', 'ndvi.dim')
print r
print r


# In[27]:

masterBand.writePixels(0, 0, width-1, height-1, temp)
masterProduct.closeIO()



a = numpy.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
print a[1,2]
print height
print array1[3,3]

