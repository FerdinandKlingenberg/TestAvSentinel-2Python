#!C:\Python27\ArcGIS10.5
# -*- coding: latin-1 -*-
import os, sys
from  numpy import *
import csv, math
import numpy
#from numpy import matlib
#from numpy.matlib import rand,zeros,ones,empty,eye


data = numpy.loadtxt(r'F:\c\Workspace\20160819-20160921shiftedTo20160819-NCC-15-20-150.txt',skiprows=1, delimiter=",")
X,Y,dx,dy,length,direction,max_corrcoeff,avg_corrcoeff = data.T # data.T

##print data[0,2] # 248
##print X[1]
##print Y[1]

#Antall elementer som skal fylles opp

antallFyll = int((max_corrcoeff > 0.7).sum())
antallTotal = int(max_corrcoeff.sum())

# Initaliserer de foerst
X_ = []
Y_ = []
dx_ = []
dy_ = []
length_ = []
direction_ = []
max_corrcoeff_ = []
avg_corrcoeff_= []


# Fyller med null/tomme
X_ = numpy.zeros(antallFyll)
Y_ = numpy.zeros(antallFyll)
dx_ =numpy.zeros(antallFyll)
dy_ = numpy.zeros(antallFyll)
length_ = numpy.zeros(antallFyll)
direction_ = numpy.zeros(antallFyll)
max_corrcoeff_ = numpy.zeros(antallFyll)
avg_corrcoeff_= numpy.zeros(antallFyll)

# Teller for for-loop
teller = -1

for i in xrange(antallTotal):
    if max_corrcoeff[i] > 0.7:
        teller = teller+1
        X_[teller] = X[i]
        Y_[teller] = Y[i]
        dx_[teller] =dx[i]
        dy_[teller] =dy[i]
        length_[teller] = length[i]
        direction_[teller] = direction[i]
        max_corrcoeff_[teller] = max_corrcoeff[i]
        avg_corrcoeff_[teller] = avg_corrcoeff[i]


# mean lengde
meanLength = numpy.mean(length_)
meanDirection = numpy.mean(direction_)


meanSetning='Mean distance: %s meter'  % (meanLength)
print(meanSetning)
meanDirection='Mean direction: %s degrees'  % (meanDirection)
print(meanDirection)
