# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 08:31:55 2018

@author: 264401k
This script smooths *.cor files (i.e. GPR GPS files) and exports to KML
"""
import pandas as pd
import numpy as np
import pygimli.frameworks
import matplotlib.pyplot as plt
import simplekml
import os
import glob

def interpolateData(datIn):
    # Interpolate
    xx = -1*datIn[3].values
    yy = datIn[5].values
    zz = datIn[7].values
    tt = datIn[0].values.astype('float64') # tt is tape-length
    x = np.asarray(pygimli.frameworks.harmfit(xx,tt, nc = 10)[0])
    y = np.asarray(pygimli.frameworks.harmfit(yy,tt, nc = 10)[0])
    z = np.asarray(pygimli.frameworks.harmfit(zz,tt, nc = 2)[0])

    # Display plot
    fig, ax = plt.plot(xx,yy, 'bx-',x,y,'r-')
    plt.plot(tt,zz, 'bx-',tt,z,'r-')
    return x,y,z

def exportToKML(fIn, x,y):
    # Export to kml
    vals = np.stack([y,x]).T
    kml = simplekml.Kml()
    kml.document.name = os.path.split(fIn)[1]
    for n,val in enumerate(vals):
        print(n,val)
        pnt = kml.newpoint(name = str(n), coords = [val])
        pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
        pnt.style.labelstyle.scale = 0
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

    kml.save((fIn + "_smoothed.kml"))
    return None

def exportToCor(datIn,x,y,z):
    datOut = datIn
    datOut[3] = -1*x
    datOut[5] = y
    datOut[7] = z

    # Check for directory and make if nonexistent.
    if os.path.isdir(fDir+"\\out\\"):
        pass
    else:
        os.mkdir(fDir+"\\out\\")

    # Set export name and directory
    dirOut = (fDir+"\\out\\" + fIn + "_smoothed.cor")
    datOut.to_csv(dirOut, index = False, header = None)
    return None


# Read data
fDir = "G:\OpenSpatial\Data\BucklandHill\Out"
currDir = os.getcwd()
os.chdir(fDir)
fList = glob.glob('*.cor') #Make a list of the cor's in the directory.

for fIn in fList:
    print(fIn)
    if os.path.getsize(fIn) > 0:
        datIn = pd.read_table(fIn, header = None)
        x,y,z = interpolateData(datIn)
        exportToKML(fIn, x,y)
        exportToCor(datIn,x,y,z)
    else:
        print('File is empty - skipping file.')
print('Done.')