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
df_temp=pd.DataFrame()
ii=0
#RPs
for kk in [20,100,500]:
    name_='Clagary_%d_JBA_SW'%(kk)
    df=pd.read_csv('ExposureRoad_%s_v1.csv'%(name_))
    #population density
    pop_dense=df['pop']/df['a']
    df_temp['pop_d']=df['pop']/df['a']
    #return period
    df_temp['rp']=kk
    #population density class
    df_temp['pop_d_c']='Moderate'
    df_temp['pop_d_c'][pop_dense<np.nanpercentile(pop_dense, 30)]='Low'
    df_temp['pop_d_c'][pop_dense>np.nanpercentile(pop_dense, 95)]='High'
    expose=df['Exposure']
    #exposure
    df_temp['f_exp']=expose
    #exposure class
    df_temp['f_exp_c']='Moderate'
    df_temp['f_exp_c'][expose<np.nanpercentile(expose, 30)]='Low'
    df_temp['f_exp_c'][expose>np.nanpercentile(expose, 95)]='High'
    if ii==0:
        df_total=df_temp
    else:
        df_total=pd.concat((df_total,df_temp),axis=0)
    ii=ii+1
df_total.dropna(inplace=True)   
