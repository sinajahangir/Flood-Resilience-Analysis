# -*- coding: utf-8 -*-
"""
Function(s) for extracting the location of the pixels' of interest, and saving
them in tabular format
@author: Sina Jahangir
"""
#%%
#import necessary libraries
import rasterio
from rasterio.transform import xy
from rasterio.warp import transform
import numpy as np
import pandas as pd
import os
#%%
#change directory
os.chdir(r'D:\NRC\ClippedJBA_Calgary') #where the raster file is located
#%%
geotiff_files = ['CA_202012_FLSW_U_RP100_RB_30m_4326.tif'] #Change name
#%%
threshold=0 #threshold for detecting water
for i, file in enumerate(geotiff_files):
    with rasterio.open(file) as src:
        data = src.read(1)  # First band
        transform_matrix = src.transform
        src_crs = src.crs
        height, width = src.height, src.width
    
        # Get center of raster in source CRS
        center_x, center_y = xy(transform_matrix, height // 2, width // 2)
    
        # Convert center to WGS84 to find UTM zone
        lon_center, lat_center = transform(src_crs, 'EPSG:4326', [center_x], [center_y])
        lon_center, lat_center = lon_center[0], lat_center[0]
    
        # Compute UTM zone number
        utm_zone = int((lon_center + 180) / 6) + 1
        is_northern = lat_center >= 0
        epsg_code = 32600 + utm_zone if is_northern else 32700 + utm_zone
        utm_crs = f"EPSG:{epsg_code}"
    
        print(f"Using UTM CRS: {utm_crs}")
        
        # Get bounds
    # Find non-zero pixel indices
    non_zero_indices = np.argwhere(data > threshold)
    rows, cols = non_zero_indices[:, 0], non_zero_indices[:, 1]
    
    # Convert row/col to source CRS coordinates
    xs, ys = xy(transform_matrix, rows, cols)
    
    # Transform coordinates from source CRS to UTM
    utm_xs, utm_ys = transform(src_crs, utm_crs, xs, ys)
    
    # Extract pixel values
    values = data[rows, cols]
    
    # Create DataFrame
    df = pd.DataFrame({
        'easting': utm_xs,
        'northing': utm_ys,
        'value': values
    })
    df.to_csv('%s.csv'%(file[:-4]))
