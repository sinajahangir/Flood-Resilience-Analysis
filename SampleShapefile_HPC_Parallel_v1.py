# -*- coding: utf-8 -*-
"""
First version: August 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
#This code is for sampling a shapefile by a shapefile
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
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import os
import multiprocessing as mp
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
list_flood=[5,10,50,100]
def flood_exposure(RP):
    rp=RP
    target_shapefile='./FloodLayers/FloodReprojected_1_%d.shp'%(rp)
    output_dir='./Sample%d'%(rp)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print('started %d simulation'%(rp))
        #ii=len(res)
    for ii in range(0,len(res)):
        input_file='./ClipRoad/ClippedShapefile_FID_%d.shp'%(ii)
        output_file=output_dir+'/'+'Exposure_FID_%s_v1.csv'%(ii)
        gdf_target=gpd.read_file(target_shapefile)
        gdf=gpd.read_file(input_file)
        gdf=gdf.to_crs(gdf_target.crs)
        
        intersection_gdf = gpd.overlay(gdf, gdf_target, how='intersection')
        intersection_gdf.to_csv(output_file)
    return
ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK',default=1))
pool = mp.Pool(processes=ncpus)
if __name__ == '__main__': 
    pool.map(flood_exposure, list_flood)
    
    
    
    
    
    
    

