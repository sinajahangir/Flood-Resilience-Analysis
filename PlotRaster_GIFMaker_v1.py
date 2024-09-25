# -*- coding: utf-8 -*-
"""
First version: Jan 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
# This code is for plotting a raster alongside a shapefile
    ## GIF maker added for showing different return periods
# This version implemented for JBA data (city of Calgary)

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

#Dependencies:
-geopandas
-rasterio
-json
-numpy
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import os
import imageio
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib import rcParams
#%%
#change directory
os.chdir(r'D:\NRC\Calgary')
#The source shapefile
    ## change directory
input_shapefile=r"D:\NRC\RoadNetwork\CalgaryReprojected.shp"
gdf=gpd.read_file(input_shapefile)
#%%
#plotting options
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
rcParams['font.family'] = 'Calibri'
#%%
#Flood type
    ##Either RF (riverine flood) or SW (surface water)
fl_t='RF'
#Return period
    ##from 20,50,75,100,200,500,1500
rp=1500
# Load raster data
    ##change directory
raster_path = r'D:\NRC\ClippedJBA_Calgary\CA_202012_FL%s_U_RP%d_RB_30m_4326.tif'%(fl_t,rp)
with rasterio.open(raster_path) as src:
    raster_data = np.float16(src.read(1))  # Read the first band
    raster_extent = src.bounds  # Get the bounds of the raster
    raster_transform = src.transform

index_zero=raster_data==0
raster_data[index_zero]=np.nan


unique_values = np.unique(raster_data[~np.isnan(raster_data)])  # Exclude NaNs
n_unique = len(unique_values)
# Create a plot
fig, ax = plt.subplots(1, 1,figsize=(6, 6),dpi=400)
norm = Normalize(vmin=np.nanmin(raster_data), vmax=np.nanmax(raster_data))
cmap = cm.get_cmap('tab20b', n_unique)  # Discrete colormap based on unique values
# Plot raster
raster_img = ax.imshow(raster_data, extent=[raster_extent.left, raster_extent.right,\
                    raster_extent.bottom, raster_extent.top],cmap=cmap,interpolation='none')

# Plot shapefile
gdf.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=1)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm._A = []
cbar = fig.colorbar(sm, ax=ax,fraction=0.046, pad=0.04)
cbar.set_label('Class')

# Set plot title and labels
ax.set_title('%s with a RP=%d'%(fl_t,rp), fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)


[x.set_linewidth(2) for x in ax.spines.values()]
ax.tick_params(direction="inout", right=True, length=8)


# Set colorbar ticks to match the unique values
cbar_ticks = np.linspace(np.min(unique_values), np.max(unique_values), n_unique + 1)[:-1] + np.diff(unique_values)[0] / 2
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels(unique_values)


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

plt.tight_layout()
fig.text(0.01, 0.01, 'Credit: Jahangir and Shirkhani, NRC (2024)', ha='left', va='bottom', fontsize=12)
fig.text(0.01, 0.04, 'RF=Riverine Flood; SW=Surface Water', ha='left', va='bottom', fontsize=12)
    
#%%
# GIF maker
# Temporary directory to save frames
temp_dir = 'temp_frames'
os.makedirs(temp_dir, exist_ok=True)
RP=[20,50,75,100,200,500,1500]
# Create frames
frame_paths = []
#Flood type
    ##Either RF or SW
fl_t='RF'
for ii in RP:
# Create a plot with latitude and longitude axes
    raster_path = r'D:\NRC\ClippedJBA_Calgary\CA_202012_FL%s_U_RP%d_RB_30m_4326.tif'%(fl_t,ii)
    with rasterio.open(raster_path) as src:
        raster_data = np.float16(src.read(1))  # Read the first band
        raster_extent = src.bounds  # Get the bounds of the raster
        raster_transform = src.transform

    index_zero=raster_data==0
    raster_data[index_zero]=np.nan


    unique_values = np.unique(raster_data[~np.isnan(raster_data)])  # Exclude NaNs
    n_unique = len(unique_values)
    # Create a plot
    fig, ax = plt.subplots(1, 1,figsize=(6, 6),dpi=400)
    norm = Normalize(vmin=np.nanmin(raster_data), vmax=np.nanmax(raster_data))
    cmap = cm.get_cmap('tab20b', n_unique)  # Discrete colormap based on unique values
    # Plot raster
    raster_img = ax.imshow(raster_data, extent=[raster_extent.left, raster_extent.right,\
                        raster_extent.bottom, raster_extent.top],cmap=cmap,interpolation='none')

    # Plot shapefile
    gdf.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=1)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax,fraction=0.046, pad=0.04)
    cbar.set_label('Class')

    # Set plot title and labels
    ax.set_title('%s with a RP=%d'%(fl_t,ii), fontsize=16, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=14)
    ax.set_ylabel('Latitude', fontsize=14)


    [x.set_linewidth(2) for x in ax.spines.values()]
    ax.tick_params(direction="inout", right=True, length=8)


    # Set colorbar ticks to match the unique values
    cbar_ticks = np.linspace(np.min(unique_values), np.max(unique_values), n_unique + 1)[:-1] + np.diff(unique_values)[0] / 2
    cbar.set_ticks(cbar_ticks)
    cbar.set_ticklabels(unique_values)


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


    
    fig.text(0.01, 0.01, 'Credit: Jahangir and Shirkhani, NRC (2024)', ha='left', va='bottom', fontsize=12)
    fig.text(0.01, 0.04, 'RF=Riverine Flood; SW=Surface Water', ha='left', va='bottom', fontsize=12)
    plt.tight_layout()
    
    # Save the frame
    frame_path = os.path.join(temp_dir, f'frame_{ii}.png')
    plt.savefig(frame_path)
    plt.close(fig)
    frame_paths.append(frame_path)

# Create a GIF
gif_path = 'Flood_%s_Calgary.gif'%(fl_t)
with imageio.get_writer(gif_path, mode='I', duration=1.5) as writer:
    for frame_path in frame_paths:
        image = imageio.imread(frame_path)
        writer.append_data(image)

# Cleanup temporary frames
for frame_path in frame_paths:
    os.remove(frame_path) 
    
    
    
    
    
    
    
    

