# -*- coding: utf-8 -*-
"""
Function(s) for extracting the location of the centrod of a shapefile of interest, and saving
them in tabular format
@author: Sina Jahangir
"""
#%%
#import necessary libraries
import geopandas as gpd
import pandas as pd
from rasterio.warp import transform
import os
#%%
#change directory
os.chdir(r'D:\NRC\Exposure_CalgaryDA\SocialNRCan_Calgary') #where the shapefile is located
#%%
# Load the shapefile
shapefile_path = "CalgaryDA_SoVI.shp"  # Replace with your path
gdf = gpd.read_file(shapefile_path)

# Ensure geometry is in WGS84 for coordinate extraction
gdf = gdf.to_crs("EPSG:4326")

# Project temporarily to a global equal-area projection for accurate centroid calculation
gdf_projected = gdf.to_crs("EPSG:3857")  # Web Mercator for general-purpose use
gdf['centroid'] = gdf_projected.geometry.centroid.to_crs("EPSG:4326")  # Convert centroids back to WGS84

# Extract latitude and longitude from centroid
lon = gdf['centroid'].x
lat = gdf['centroid'].y

# Convert to UTM
utm_xs = []
utm_ys = []
utm_zones = []
#%%
for lat_val, lon_val in zip(lat, lon):
    utm_zone = int((lon_val + 180) / 6) + 1
    is_northern = lat_val >= 0
    epsg_code = 32600 + utm_zone if is_northern else 32700 + utm_zone
    utm_crs = f"EPSG:{epsg_code}"
    
    utm_x, utm_y = transform("EPSG:4326", utm_crs, [lon_val], [lat_val])
    utm_xs.append(utm_x[0])
    utm_ys.append(utm_y[0])
    utm_zones.append(epsg_code)

# Create output DataFrame
df = pd.DataFrame({
    'feature_id': gdf.index,
    'latitude': lat,
    'longitude': lon,
    'easting': utm_xs,
    'northing': utm_ys,
    'utm_epsg': utm_zones
})

print(df.head())










