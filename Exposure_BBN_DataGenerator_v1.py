# -*- coding: utf-8 -*-
"""
Last updated January 2025
@author: Mohammad Sina Jahangir
Email:mohammadsina.jahangir@gmail.com
#Tested on Python 3.7.16
Copyright (c) [2024] [Mohammad Sina Jahangir]

#This code is used creating the csv file input to the BBN for exposure analysis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

#%%
import pandas as pd
import numpy as np
import os
#%%
#change directory to the target folder
os.chdir(r'D:\NRC')
#%%
#pre-define a df
ii = 0
df_total = pd.DataFrame()

for kk in [20, 100, 500]:
    #updated for the new exposure including edge betweenness centrality
    name_ = 'EBC_Clagary_%d_JBA_SW' % (kk)
    df = pd.read_csv('ExposureRoad_%s_v1.csv' % (name_))
    
    # Initialize df_temp within the loop
    df_temp = pd.DataFrame()
    
    # Population density
    pop_dense = df['pop'] / df['a']
    df_temp['pop_d'] = pop_dense
    
    # Return period
    df_temp['rp'] = kk
    
    # Population density class
    df_temp['pop_d_c'] = 'Moderate'
    df_temp.loc[pop_dense < np.nanpercentile(pop_dense, 30), 'pop_d_c'] = 'Low'
    df_temp.loc[pop_dense > np.nanpercentile(pop_dense, 95), 'pop_d_c'] = 'High'
    
    # Exposure
    expose = df['Exposure']
    df_temp['f_exp'] = expose
    
    # Exposure class
    df_temp['f_exp_c'] = 'Moderate'
    df_temp.loc[expose < np.nanpercentile(expose, 30), 'f_exp_c'] = 'Low'
    df_temp.loc[expose > np.nanpercentile(expose, 95), 'f_exp_c'] = 'High'
    
    
    # Road class
    df_temp['rc'] = df['RoadClass'].str.split(' ', expand=True)[0]
    
    if ii == 0:
        df_total = df_temp
    else:
        df_total = pd.concat((df_total, df_temp), axis=0, ignore_index=True)
    
    ii += 1
df_total.dropna(inplace=True)   
#%%
df_total.to_csv('Exposure_All_BBFInput_v1.csv')