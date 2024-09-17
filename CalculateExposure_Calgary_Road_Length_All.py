# -*- coding: utf-8 -*-
"""

First updated Jan 2024
@author: Mohammad Sina Jahangir
Email:mohammadsina.jahangir@gmail.com
#This code is for calculating exposure
#Tested on Python 3.7.16
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

This code primary use is to calculate exposure based on the previously conducted
geospatial analysis

The previous version(s) used edge betweennes centrality (EBC, calculated for the road netwrok)
as one of the features. Further analysis proved such an approach will results in
non-realistic exposure classes in the region.
"""

#%%
import pandas as pd
import numpy as np
import os
import geopandas as gpd
#%%
os.chdir(r'D:\NRC')
#%%
sovi_=pd.read_csv(r"D:\NRC\DA_Calgary_Table.csv")
#%%
#seven flood scenarios based on different RPs
len_sovi=len(sovi_)
exposure_=np.zeros((len_sovi,1))
for kk in [2,5,10,50,100,200,1000]:
    for ii in range(0,len_sovi):
        flag_=0
        try:
            expos_temp=pd.read_csv(r'D:\NRC\Exposure_CalgaryDA\Samples\Sample%d\Exposure_FID_%d_v1.csv'%(kk,ii),index_col=0)
            length=np.asarray(expos_temp['Length']).reshape((-1,1))
            #ebc=np.asarray(expos_temp['EBC']).reshape((-1,1))*1e5
            #flow=np.asarray(expos_temp['flow_rate']).reshape((-1,1))
            if len(expos_temp)==0:
                flag_=1
        except Exception as e:
            print(e)
            print(ii)
            flag_=1
        if flag_==0:
            temp_1=length
            #temp_2=ebc
            #calculating exposure only based on the road netwrok length
            exposure_[ii,0]=np.sum(temp_1)
    gdf=gpd.read_file(r"D:\NRC\Exposure_CalgaryDA\CalgaryDA.shp")
    gdf['Exposure']=(exposure_-np.min(exposure_))/(np.max(exposure_)-np.min(exposure_))
    name_='Clagary_%d_Length'%(kk)
    try:
        gdf.to_file(r'Exposure_Shapefile_%s\ExposureRoad_%s_2024_v1.shp'%(name_,name_))
    except Exception as e:
        print(e)
        print('Creating Directory')
        os.mkdir('Exposure_Shapefile_%s'%(name_))
        gdf.to_file(r'Exposure_Shapefile_%s\ExposureRoad_%s_2024_v1.shp'%(name_,name_))
#%%
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
from matplotlib import rcParams
rcParams['font.family'] = 'Calibri'
#%%
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import imageio
#%%
# Temporary directory to save frames
temp_dir = 'temp_frames'
os.makedirs(temp_dir, exist_ok=True)
RP=[2,5,10,50,100,200,1000]
# Load the shapefile

# Define the feature based on which you want to color the fill
feature_column = 'Exposure'
# Create frames
frame_paths = []

for ii in RP:
# Create a plot with latitude and longitude axes
    fig, ax = plt.subplots(1, 1, figsize=(6, 6),dpi=600)
    shapefile_path = r'Exposure_Shapefile_Clagary_%d_Length\ExposureRoad_Clagary_%d_Length_2024_v1.shp'%(ii,ii)
    gdf = gpd.read_file(shapefile_path)

    # Plot the boundaries in black
    #gdf.boundary.plot(ax=ax, color='black')
    
    # Plot the fill colors based on the feature
    norm = Normalize(vmin=gdf[feature_column].min(), vmax=gdf[feature_column].max())
    cmap =cm.get_cmap('tab20b', 20)
    gdf.plot(column=feature_column, ax=ax, legend=False, edgecolor='black', cmap=cmap, norm=norm)
    
    # Create a colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax,fraction=0.046, pad=0.04)
    cbar.set_label(feature_column)
    
    # Set axis labels to latitude and longitude
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    
    [x.set_linewidth(2) for x in ax.spines.values()]
    ax.tick_params(direction="inout", right=True, length=8)
    
    # Calculate the center of the boundary
    xmin, ymin, xmax, ymax = gdf.total_bounds
    x_center = -114.2
    y_center = 51
    
    # Define a zoom factor (0.1 means 10% of the total extent)
    zoom_factor = 0.25
    x_range = (xmax - xmin) * zoom_factor
    y_range = (ymax - ymin) * zoom_factor
    
    # Set the axis limits to zoom into the center
    ax.set_xlim(x_center - x_range, x_center + x_range)
    ax.set_ylim(y_center - y_range, y_center + y_range)
    
    ax.set_title('Road Exposure: RP=%d'%(ii))
    
    fig.text(0.01, 0.01, 'Credit: Jahangir and Shirkhani, National Research Council Canada (2024)', ha='left', va='bottom', fontsize=12)
    
    # Save the frame
    frame_path = os.path.join(temp_dir, f'frame_{ii}.png')
    plt.savefig(frame_path)
    plt.close(fig)
    frame_paths.append(frame_path)

# Create a GIF
gif_path = 'RoadExposure_Calgary_NRC_Length.gif'
with imageio.get_writer(gif_path, mode='I', duration=1.5) as writer:
    for frame_path in frame_paths:
        image = imageio.imread(frame_path)
        writer.append_data(image)

# Cleanup temporary frames
for frame_path in frame_paths:
    os.remove(frame_path) 
    

    
    

       
        
        
        
        
        
        
        
    
    
