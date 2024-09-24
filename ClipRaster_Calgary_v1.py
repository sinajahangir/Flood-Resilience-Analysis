# -*- coding: utf-8 -*-
"""
First version: Jan 2024
@author: Mohammad Sina Jahangir (Ph.D.)
Email:mohammadsina.jahangir@gmail.com
#This code is for clipping a raster with a shapefile
#Used in this version for clipping JBA data by the city of Calgary border

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
#Tested on Python 3.7.16
"""
#%%
#Importing the necessary libraries
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import json
import os
#%%
class ClipRaster:
    def __init__(self, input_raster,input_shapefile,output_raster):
        self.shapefile_inp = input_shapefile
        self.raster_inp = input_raster
        self.raster_out=output_raster
        self.df = gpd.read_file(self.shapefile_inp)
        self.src=rasterio.open(self.raster_inp)
    
    def getFeatures(self):
        """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
        gpd_filtered_json_str = self.df.to_json()
        gpd_filtered_json_dict = json.loads(gpd_filtered_json_str)
        self.shapes = [feature["geometry"] for feature in gpd_filtered_json_dict["features"]]

        return self.shapes
    
    def clip(self):
        coords = self.getFeatures()
        clipped_array, clipped_transform = mask(dataset=self.src, shapes=coords, crop=True)
        self.df= self.df.to_crs(self.src.crs)

        out_meta = self.src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": clipped_array.shape[1],
                         "width": clipped_array.shape[2],
                         "transform": clipped_transform})
        out_tif= self.raster_out
        with rasterio.open(out_tif, "w", **out_meta) as dest:
            dest.write(clipped_array)
        return

#%%
#path to the folder containing all the raster files
dir_path=r"E:\JBA-Flood Layers"
res = []
# Iterate directory
for file in os.listdir(dir_path):
    # check raster files (tif format)
    if file.endswith('.tif'):
        res.append(file)
#%%
#path to the folder where the clipped ratsers are saved
target_folder=r'D:\NRC\ClippedJBA_Calgary'
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
#%%
#The source shapefile to use for clipping
input_shapefile=r"D:\NRC\RoadNetwork\CalgaryReprojected.shp"
gdf=gpd.read_file(input_shapefile)
#%%
#iterate through the rasters
for ii in res:
    output_raster=target_folder+r'\\'+ii
    input_raster=dir_path+r'\\'+ii
    class_clip=ClipRaster(input_raster, input_shapefile, output_raster)
    class_clip.clip()

    
    
    
    
    
    
    
    
    
    

