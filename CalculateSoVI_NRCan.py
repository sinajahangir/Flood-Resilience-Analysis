# -*- coding: utf-8 -*-
"""
First version: October 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
#This code is for upscaling the social fabric product of NRCan. See: https://open.canada.ca/data/en/dataset/36d4b36f-e21f-49b7-b6a6-4d14551c8be6
    ##Social vulnerability is derived for each DA for the city of Calgary
    ##The code uses mean for upscaling. Other stats can also be adopted (e.g., max, median)

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
#Tested on Python 3.7.16
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import os
#%%
#change directory to the shapefiles
os.chdir(r'D:\NRC\Exposure_CalgaryDA\SocialNRCan_Calgary')
# Read the shapefiles
#Calgary boundary shapefile
shapefile_one = gpd.read_file('CalgaryDA.shp')
#Social fabric
shapefile_two = gpd.read_file('SocialFabric.shp')

# Make sure both shapefiles use the same CRS (Coordinate Reference System)
if shapefile_one.crs != shapefile_two.crs:
    shapefile_two = shapefile_two.to_crs(shapefile_one.crs)
#%%
# Specify the feature column from shapefile two for which to calculate the mean
feature_column = 'SVlt_Score'  

# Initialize an empty list to store the mean values for each feature in shapefile one
mean_feature_values = []

# Loop through each feature in shapefile one
for idx_one, row_one in shapefile_one.iterrows():
    # Get the geometry of the current feature in shapefile one
    geom_one = row_one.geometry
    
    # Intersect the features of shapefile two with the current feature of shapefile one
    intersected = shapefile_two[shapefile_two.intersects(geom_one)]
    
    if not intersected.empty:
        # Calculate the mean value of the specified feature from the intersected features
        mean_value = intersected[feature_column].mean()
    #This is not applicable here. For general use.
    else:
        mean_value = None  # No intersection found
    # Append the max value to the list
    mean_feature_values.append(mean_value)
#%%
# Assign the max feature values to a new column in shapefile one
shapefile_one['SoVI_NRCan'] = mean_feature_values

# Save the updated shapefile (optional)
shapefile_one.to_file('CalgaryDA_SoVI.shp')
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
plot=shapefile_one.plot(column='SoVI_NRCan', ax=ax, cmap='RdYlGn_r', legend=True,cax=cax)
# Plot shapefile
shapefile_one.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=1,zorder=2)

# Shrink the colorbar by adjusting its aspect ratio
cax.set_aspect(1)  # Increase/decrease the aspect ratio to shrink/expand the colorbar

# Set plot title and labels
ax.set_title('SoVI', fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)
    
# Calculate the center of the boundary
xmin, ymin, xmax, ymax = shapefile_one.total_bounds
x_center = -114.1
y_center = 51


# Add label to the colorbar
cbar = plot.get_figure().colorbar(plot.collections[0], cax=cax)
cbar.set_label('Relative SoVI', fontsize=12)

# Define a zoom factor (0.1 means 10% of the total extent)
zoom_factor = 0.15
x_range = (xmax - xmin) * zoom_factor
y_range = (ymax - ymin) * zoom_factor

# Set the axis limits to zoom into the center
ax.set_xlim(x_center - x_range, x_center + x_range)
ax.set_ylim(y_center - y_range, y_center + y_range)

plt.tight_layout()
fig.text(0.01, 0.06, 'Credit: Jahangir and Shirkhani, NRC (2024)', ha='left', va='bottom', fontsize=12)
fig.text(0.01, 0.09, 'SoVI: Social Vulnerability', ha='left', va='bottom', fontsize=12)

#plt.tight_layout()   

#save figure
plt.savefig('SoVI_CalgaryDA_NRCan_v1.png')  
    
    
    
    
    
    
    

