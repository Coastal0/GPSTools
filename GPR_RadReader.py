# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 09:36:41 2018
@author: 264401k
RADREADER
"""
import pandas as pd
import glob

print('Reading *.RAD files...')
fList = glob.glob('*.rad')
print(len(fList), ' file/s found.')
print('Makeing dataframes...')
df_fList = (pd.read_csv(f, delimiter=":", header=None, index_col=0) for f in fList)
data = pd.concat(df_fList, axis=1).T.reset_index(drop=True)
data = data.apply(pd.to_numeric, errors='ignore')
writer = pd.ExcelWriter('.\GPR_RadFiles.xlsx')
print('Writing Spreadsheet:', writer.path)
data.to_excel(writer, 'Raw')
data.describe().to_excel(writer, 'Descriptions')
writer.save()
print('Done.')
