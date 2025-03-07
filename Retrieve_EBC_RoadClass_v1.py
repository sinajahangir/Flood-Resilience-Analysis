# -*- coding: utf-8 -*-
"""
Last updated February 2025
@author: Mohammad Sina Jahangir
Email:mohammadsina.jahangir@gmail.com
#This code is for retrieving EBC (edge betweenness centrality and road class)
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
"""
#%%
#Importing the necessary libraries
import os
import geopandas as gpd
#%%
# Define paths
source_shapefile = r"D:\NRC\Exposure_CalgaryDA\CalgaryDA.shp"
clipped_folder = r"D:\NRC\Exposure_CalgaryDA\ClipRoad"  #Road clipped shapefiles
output_shapefile = r"D:\NRC\Exposure_CalgaryDA\CalgaryEBC_Class.shp"  # Name of the output shapefile

# Read the source shapefile
source_gdf = gpd.read_file(source_shapefile)

# Initialize lists to store computed values
mean_values = []
max_length_values = []

# List all shapefiles in the folder
shapefiles = [file for file in os.listdir(clipped_folder) if file.endswith(".shp")]
#%%
for ii in range(len(shapefiles)):
    input_file = clipped_folder+ '\\' + 'ClippedShapefile_FID_%d.shp'%(ii)
    gdf = gpd.read_file(input_file)
    if not gdf.empty:
        mean_val = gdf["EBC"].mean()  # Replace with actual column name
        max_length_row = gdf.loc[gdf["Length"].idxmax(), "ROADCLASS"]
    else:
        mean_val = None
        max_length_row = None
    
    mean_values.append(mean_val)
    max_length_values.append(max_length_row)

# Add new columns to source shapefile
source_gdf["EBC"] = mean_values
source_gdf["RoadClass"] = max_length_values

# Save the updated shapefile
source_gdf.to_file(output_shapefile)
    
    
    
    
    
    

