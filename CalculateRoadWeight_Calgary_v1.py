# -*- coding: utf-8 -*-
"""
First version: October 2024
@author: Mohammad Sina Jahangir (Ph.D)
Email:mohammadsina.jahangir@gmail.com
#This code is for calculating road netwrok "density" and "importance" (based on type)
for each DA
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
-pandas
-numpy
    
"""

#%%
import pandas as pd
import numpy as np
import os
import geopandas as gpd
#%%
folder_path=r'D:\NRC\RoadNetwork\ClippedRoad'
os.chdir(r'D:\NRC\RoadNetwork\ClippedRoad')
# Define the names of the attributes and road class column
attribute2 = 'Length'  # Replace with the actual attribute to divide by
road_class_column = 'ROADCLASS'  # Column that contains the road class
new_attribute_name = 'weighted_attr_ratio'  # Name for the new attribute
#%%
# Define the weights for the road classes (using multiples of 2)
road_class_weights = {
    'Alleway / Lane': 2,
    'Arterial': 64,
    'Collector': 16,
    'Expressway / Highway': 128,
    'Freeway': 256,
    'Local / Strata': 4,
    'Local / Street': 4,
    'Local / Unknown': 4,
    'Ramp': 8,
    'Rapid Transit': 512,
    'Resource / Recreation': 32,
    'Service Lane': 1
}
#Local type is repeated X 3
sum_weights=np.sum(list(road_class_weights.values()))-8
#%%
# Initialize a list to hold the new calculated attribute values
new_attribute_values = []
total_length=[]
# Only process shapefiles (.shp)
shapefiles = [f for f in os.listdir(folder_path) if f.endswith(".shp")]
# Iterate through each file in the folder
for shapefile in shapefiles:
    gdf = gpd.read_file(shapefile)
        #temp lists for poulating
            ##w: weighted 1/length
            ##l: length
    temp_w=[]
    temp_l=[]
      

        # Loop through each row in the GeoDataFrame
    for idx, row in gdf.iterrows():
            # Get the road class and the corresponding weight
        road_class = row[road_class_column]
        weight = road_class_weights.get(road_class, 1)  # Default to 1 if not found

            # Calculate the weighted attribute ratio (avoid division by zero)
        if row[attribute2] != 0:
            weighted_ratio = (weight) / row[attribute2]
        else:
            weighted_ratio = None  # Handle division by zero
        temp_w.append(weighted_ratio)
        temp_l.append(row[attribute2])
    # Append the result to the list
    new_attribute_values.append(np.sum(temp_w)/sum_weights)
    total_length.append(np.sum(temp_l))


       
        
        
        
        
        
        
        
    
    
