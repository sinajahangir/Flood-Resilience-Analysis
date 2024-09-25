# -*- coding: utf-8 -*-
"""
First version: August 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
#This code is for sampling a raster by a shapefile
    ##The computation is parallelized for efficiency

#Tested on Python 3.10
Copyright (c) [2024] [Mohammad Sina Jahangir]

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

#Dependencies:
-geopandas
-rasterio
-numpy
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import os
import rasterio
import multiprocessing as mp
import numpy as np
import pandas as pd
#%%
#where clipped shapefiles are.
dir_path='./ClipRoad'
res = []
# Iterate directory
for file in os.listdir(dir_path):
    # check only text files
    if file.endswith('.shp'):
        res.append(file)
#%%
list_flood=[20,50,75,100,200,500,1500]
#flood_type
fl_t='RF'
def flood_exposure(RP):
    rp=RP
    #change directory
    target_raster='./ClippedJBA_Calgary/CA_202012_FL%s_U_RP%d_RB_30m_4326.tif'%(fl_t,rp)
    output_dir='./%s_SampleJBA_RP=%d'%(fl_t,rp)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print('started %d simulation'%(rp))
        #ii=len(res)
    for ii in range(0,len(res)):
        input_file='./ClipRoad/ClippedShapefile_FID_%d.shp'%(ii)
        output_file=output_dir+'/'+'Exposure_FID_%s_v1.csv'%(ii)
        gdf=gpd.read_file(input_file)
        
        coord_list_min_min = [(x, y) for x, y in zip(gdf["geometry"].bounds['minx'], gdf["geometry"].bounds['miny'])]
        coord_list_min_max = [(x, y) for x, y in zip(gdf["geometry"].bounds['minx'], gdf["geometry"].bounds['maxy'])]
        
        coord_list_max_max = [(x, y) for x, y in zip(gdf["geometry"].bounds['maxx'], gdf["geometry"].bounds['maxy'])]
        coord_list_max_min = [(x, y) for x, y in zip(gdf["geometry"].bounds['maxx'], gdf["geometry"].bounds['miny'])]
        
        coord_list=[coord_list_min_min,coord_list_min_max,\
                    coord_list_max_max,coord_list_max_min]
        
        
        
        src = rasterio.open(target_raster)
        temp_sample=np.zeros((len(gdf),len(coord_list)))
        sample_all=np.zeros((len(gdf),1))
        jj_=0
        for kk in range(0,len(coord_list)):
            coord_list_temp=coord_list[kk]
            temp_sample[:,kk]=np.asarray([x for x in src.sample(coord_list_temp)]).ravel()
        sample_all[:,jj_]=np.nanmax(temp_sample,axis=1).ravel()
        
        
        #write to csv
        df_all=pd.DataFrame(sample_all,columns=['Maximum class'])
        df_all.to_csv(output_file,index_label='FID')
    return
ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK',default=1))
pool = mp.Pool(processes=ncpus)
if __name__ == '__main__': 
    pool.map(flood_exposure, list_flood)
    
    
    
    
    
    
    

