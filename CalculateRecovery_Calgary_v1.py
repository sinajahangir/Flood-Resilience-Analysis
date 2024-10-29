# -*- coding: utf-8 -*-
"""
First version: October 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
#This code is for deriving the expected recovery
    ##Recovery is derived (for each DA) based on three components: population, road length, and road index
        ### Road index is derived using the road type
    ## Ensemble mean is calculated for derivation of recovery:
        w1population*w2road_length*w3road_index; w_i are random variables

#Code provided for plotting the shapefile

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
-matplotlib (plotting)
-numpy
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import os
import numpy as np
#%%
#change directory to the shapefiles
os.chdir(r'D:\NRC\Exposure_CalgaryDA')
# Read the shapefiles
#Calgary boundary shapefile
shapefile_one = gpd.read_file('CalgaryDA.shp')
#Road attributes
shapefile_two = gpd.read_file('CalgaryDA_RoadAttribute_v1.shp')

# Make sure both shapefiles use the same CRS (Coordinate Reference System)
if shapefile_one.crs != shapefile_two.crs:
    shapefile_two = shapefile_two.to_crs(shapefile_one.crs)
#%%
# Specify the feature column from shapefile two for which use the attributes
#population
feature_1 = np.asarray(np.float16(shapefile_two['pop']))

#Total road length
feature_2 = np.asarray(shapefile_two['RoadLength'])

#Road index (importance)
feature_3 = np.asarray(shapefile_two['RoadW1_L'])

#implement min-max scaling
feature_1=(feature_1-np.nanmin(feature_1))/(np.nanmax(feature_1)-np.nanmin(feature_1))

feature_2=(feature_2-np.nanmin(feature_2))/(np.nanmax(feature_2)-np.nanmin(feature_2))

feature_3=(feature_3-np.nanmin(feature_3))/(np.nanmax(feature_3)-np.nanmin(feature_3))


#%%
#set number of samples
samples=50
#predefine the recovery array. This will be populated
rec_array=np.zeros((len(feature_1),samples))
# Loop for 50 random weight sets (w1,w2,w3)
for ii in range(0,samples):
    # Generate random weights that sum to 1
    w1,w2,w3 = np.random.dirichlet(np.ones(3), size=1)[0]
    rec_array[:,ii]=feature_1*w1+feature_2*w2+feature_3*w3
#%%
#calculate the stat of ineterest. i.e., mean
rec=np.nanmean(rec_array,axis=1)
#rescale
rec=(rec*(np.nanmax(rec)-np.nanmin(rec))+np.nanmin(rec))*100
#%%
# Assign the recovery to a new column in shapefile one
shapefile_one['Recovery'] =rec

# Save the updated shapefile (optional)
#uncomment to save shapefile
#shapefile_one.to_file('CalgaryDA_Recovery.shp')
#%%
#plot libraries
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable
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
fig, ax = plt.subplots(1, 1,figsize=(4.5, 4.5),dpi=400)
# Create an axis divider for adjusting the size of the colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="20%",pad=-1)  # Adjust size here
# Plot the 'SoVI_NRCan' as a colored map
plot=shapefile_one.plot(column='Recovery', ax=ax, cmap='RdYlGn', legend=True,cax=cax)
# Plot shapefile
shapefile_one.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=1,zorder=2)

# Shrink the colorbar by adjusting its aspect ratio
cax.set_aspect(1)  # Increase/decrease the aspect ratio to shrink/expand the colorbar

# Set plot title and labels
ax.set_title('Recovery', fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)
    
# Calculate the center of the boundary
xmin, ymin, xmax, ymax = shapefile_one.total_bounds
x_center = -114
y_center = 51


# Add label to the colorbar
cbar = plot.get_figure().colorbar(plot.collections[0], cax=cax)
cbar.set_label('Recovery', fontsize=12)

# Define a zoom factor (0.1 means 10% of the total extent)
zoom_factor = 0.1
x_range = (xmax - xmin) * zoom_factor
y_range = (ymax - ymin) * zoom_factor

# Set the axis limits to zoom into the center
ax.set_xlim(x_center - x_range, x_center + x_range)
ax.set_ylim(y_center - y_range, y_center + y_range)

plt.tight_layout()
fig.text(0.01, 0.06, 'Credit: Jahangir and Shirkhani, NRC (2024)', ha='left', va='bottom', fontsize=12)
fig.text(0.01, 0.09, 'Road netwrok recovery', ha='left', va='bottom', fontsize=12)

#plt.tight_layout()   

#save figure
plt.savefig('Recovery_CalgaryDA_v1.png')  
    
    
    
    
    
    
    

