# -*- coding: utf-8 -*-
"""
Convert *.cor files (MALA GPS) to Google-earth text files.

Created on Wed Jul 18 09:21:56 2018

@author: 264401k
"""
import os
import glob
import pandas as pd

fDir = "G:\Data\OMP_005"
currDir = os.getcwd()
os.chdir(fDir)
fList = glob.glob('*.cor') #Make a list of the cor's in the directory.

for fIn in fList:
    print(fIn)
    if os.path.getsize(fIn) > 0:
        datIn = pd.read_table(fIn, header = None)
        datIn[7] = 0
        datIn.to_csv((fIn[0:-4]+'_nullElevs.cor'), index = False, header = None)

os.chdir(currDir)