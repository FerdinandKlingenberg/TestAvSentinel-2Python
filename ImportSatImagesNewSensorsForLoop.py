
# coding: utf-8

from pci.fimport import fimport
import sys
import numpy
import string
import os,time,tarfile,glob

folder = "D:\\D"
filepathresultat = "D:\\D\\SourceFiles"
# Initialize output name
OutputImage = ""
print("Begin geoprocessing: "+time.strftime("%X"))
time.clock()

for name in glob.glob(folder+'\\S2A*\\S2A*.xml'):
    # In data
    rawSentinel2_image = name+":Band Resolution:10M"

    # Generation of filename, with MGRS information
    (filepath, filename) = os.path.split(name)
    outName = glob.glob(filepath+"\\GRANULE\*\\S2A*.xml")
    strTemp = ''.join(outName)

    # Change end of filename with correct file extention
    (filepath, filename) = os.path.split(strTemp)
    OutputImage = filepathresultat+"\\"+filename[:-4]+"_10m.pix"

    # Do the FIMPORT, from Sentinel-2 XML to Geomatica PCI disk format (.pix)
    fimport(rawSentinel2_image, OutputImage, [], "MODE", "BAND")


    print str(OutputImage) + ' done'

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
