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

def readCor(fIn):
    datIn = pd.read_table(fIn, header = None)
    xx = -1*datIn[3].values
    yy = datIn[5].values
    zz = datIn[7].values
    tt = datIn[0].values.astype('float64') # tt is tape-length
    return(xx,yy,zz,tt)

def readGGA(fIN):
    datIn = pd.read_csv(fIn, header = None)
    # Convert DM to DD
    degLats = int(str(datIn[3][0])[:2])
    lats = (datIn[3] - degLats*100)/60+(degLats)
    # Check hemisphere
    if all(datIn[4]=='S'):
        lats = lats * -1
    degLons = int(str(datIn[5][0])[:3])
    lons = (datIn[5] - degLons*100)/60+(degLons)
    xx = lats
    yy = lons
    zz = datIn[10].values
    tt = datIn[0].values.astype('float64') # tt is tape-length
    return(xx,yy,zz,tt)

def interpolateData(xx,yy,zz,tt):
    # Interpolate
    robust = True
    nc = 5
    x = np.asarray(pygimli.frameworks.harmfit(xx,tt, nc = nc, robust = robust)[0])
    y = np.asarray(pygimli.frameworks.harmfit(yy,tt, nc = nc, robust = robust)[0])
    z = np.asarray(pygimli.frameworks.harmfit(zz,tt, nc = nc, robust = robust)[0])

    # Display plot
#    plt.figure()
    fig, ax = plt.plot(xx,yy, 'bx-',x,y,'r-')
#    plt.plot(tt,zz, 'bx-',tt,z,'r-')
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

def exportToCor(fIn,tt,xx,yy,zz):
    tt = tt.astype(int)
    dateCol = np.repeat(pd.to_datetime('today'),len(tt))
    xx = xx *-1
    lonHemi = np.repeat('S', len(tt))
    yy = yy.astype(float)
    latHemi = np.repeat('E', len(tt))
    zz = np.ones(len(zz)).astype(int)
    elevForm = np.repeat('M', len(tt))
    lastCol = np.repeat(1,len(tt))

    cor = pd.DataFrame(data = [tt,dateCol,xx,lonHemi,yy,latHemi,zz,elevForm,lastCol]).T
    # Check for directory and make if nonexistent.
    if os.path.isdir(fDir+"\\out\\"):
        pass
    else:
        os.mkdir(fDir+"\\out\\")
    dirOut = (fDir+"\\out\\" + fIn + ".cor")
    cor.to_csv(dirOut, index = False, header = None, float_format = '%.8f', sep = '\t' )
    return None

#    # Check for directory and make if nonexistent.
#    if os.path.isdir(fDir+"\\out\\"):
#        pass
#    else:
#        os.mkdir(fDir+"\\out\\")
#
#    # Set export name and directory
#    dirOut = (fDir+"\\out\\" + fIn + "_smoothed.cor")
#    datOut.to_csv(dirOut, index = False, header = None)
#    return None
#%%

# Read data
fDir = "G:\OpenSpatial\Data\Coogee"
currDir = os.getcwd()
os.chdir(fDir)
fList = glob.glob('*.gga') #Make a list of the cor's in the directory.
if len(fList) == 0:
    fList = [fDir]

for fIn in fList:
    print(fIn)
    if os.path.getsize(fIn) > 0:
        if 'gga' in fIn:
            xx,yy,zz,tt = readGGA(fIn)
            if np.var(tt) <= 1:
                print('Possible coordinate error found in file.')
                continue
        elif 'cor' in fIn:
            xx,yy,zz,tt = readCor(fIn)
#        x,y,z = interpolateData(xx,yy,zz,tt)
#        exportToKML(fIn, x,y)
        exportToCor(fIn,tt,xx,yy,zz)
    else:
        print('File is empty - skipping file.')
print('Done.')