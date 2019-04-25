# -*- coding: utf-8 -*-
"""
Convert *.cor files (MALA GPS) to Google-earth text files.

Created on Wed Jul 18 09:21:56 2018

@author: 264401k
"""
import simplekml
import os
import glob
import pandas as pd

fDir = "F:\CityBeach2018\Raw\OMP_008\OMP_008_0001_1.cor"
currDir = os.getcwd()
os.chdir(fDir)
fList = glob.glob('*.cor') #Make a list of the cor's in the directory.

for fIn in fList:
    print(fIn)
    if os.path.getsize(fIn) > 0:
        datIn = pd.read_table(fIn, header = None)
        #datIn.dropna(inplace=True)
        if all(datIn[4] == 'S'):
            datIn[3] = datIn[3]*-1

        datIn.drop([4,6,8,9], axis = 1, inplace = True)

        datIn[8] = datIn[1]+ " " + datIn[2]
        datIn.drop([1,2], axis = 1, inplace = True)

        #fOut = fIn[:-4]+"_GoogleEarthImport.txt"
        #datIn.to_csv(fOut, header = ['Trace', 'Lat', 'Lon', 'Elev', 'Date'], index = False)

        kml = simplekml.Kml()
        kml.document.name = os.path.split(fIn)[1]

        for i in datIn.itertuples():
            pnt = kml.newpoint(name = str(i[1]), coords = [(i[3],i[2],i[4])])
            pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
            pnt.style.labelstyle.scale = 0  # Make the text twice as big
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

        kml.save((fIn+".kml"))

os.chdir(currDir)