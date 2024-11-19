# -*- coding: utf-8 -*-
"""

Last updated November 2024
@author: Mohammad Sina Jahangir
Email:mohammadsina.jahangir@gmail.com
#This code is for calculating exposure
#Tested on Python 3.7.16
Copyright (c) [2024] [Mohammad Sina Jahangir]

#This code is used for 

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
import pandas as pd
import numpy as np
import os
import geopandas as gpd
#%%
os.chdir(r'D:\NRC')
#%%
sovi_=pd.read_csv(r"D:\NRC\DA_Calgary_Table.csv")
#%%
#seven flood scenarios
len_sovi=len(sovi_)
exposure_=np.zeros((len_sovi,1))
for kk in [100]:
    for ii in range(0,len_sovi):
        flag_=0
        try:
            expos_temp=pd.read_csv(r'D:\NRC\SW_SampleJBA_RP=%d\Exposure_FID_%d_v1.csv'%(kk,ii),index_col=0)
            length=np.asarray(expos_temp['Maximum class']).reshape((-1,1))
            if len(expos_temp)==0:
                flag_=1
        except Exception as e:
            print(e)
            print(ii)
            flag_=1
        if flag_==0:
            temp_1=length
            exposure_[ii,0]=np.sum(temp_1)/len(temp_1)*100
    gdf=gpd.read_file(r"D:\NRC\Exposure_CalgaryDA\CalgaryDA.shp")
    gdf['Exposure']=(exposure_-np.min(exposure_))/(np.max(exposure_)-np.min(exposure_))
    name_='Clagary_%d_JBA_SW'%(kk)
    try:
        gdf.to_file(r'Exposure_Shapefile_JBA\ExposureRoad_%s_v1.shp'%(name_))
    except Exception as e:
        print(e)
        print('Creating Directory')
        os.mkdir('Exposure_Shapefile_JBA')
        gdf.to_file(r'Exposure_Shapefile_JBA\ExposureRoad_%s_v1.shp'%(name_))
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
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots(1, 1, figsize=(4.5, 4.5), dpi=400)

# Create an axis divider for adjusting the size of the colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=-0.5)  # Adjust size and padding for clarity

# Plot the 'Exposure' column as a colored map
plot = gdf.plot(column='Exposure', ax=ax, cmap='RdYlGn_r', legend=False)

# Plot shapefile on top
gdf.plot(ax=ax, facecolor='none', edgecolor='gray', linewidth=1, zorder=2)

# Add and customize the colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlGn_r', norm=plt.Normalize(vmin=gdf['Exposure'].min(), vmax=gdf['Exposure'].max()))
cbar = fig.colorbar(sm, cax=cax)
cbar.set_label('Exposure', fontsize=12, fontweight='bold')

# Set plot title and axis labels
ax.set_title('Exposure', fontsize=16, fontweight='bold')
ax.set_xlabel('Longitude', fontsize=14)
ax.set_ylabel('Latitude', fontsize=14)

# Calculate the center of the boundary
xmin, ymin, xmax, ymax = gdf.total_bounds
x_center = -114
y_center = 51

# Define a zoom factor (0.15 means 15% of the total extent)
zoom_factor = 0.15
x_range = (xmax - xmin) * zoom_factor
y_range = (ymax - ymin) * zoom_factor

# Set axis limits to zoom into the center
ax.set_xlim(x_center - x_range, x_center + x_range)
ax.set_ylim(y_center - y_range, y_center + y_range)

# Add credit and description text
fig.text(0.01, 0.06, 'Credit: Jahangir and Shirkhani, NRC (2024)', ha='left', va='bottom', fontsize=12)
fig.text(0.01, 0.09, 'Flood exposure', ha='left', va='bottom', fontsize=12)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('Exposure_SW_CalgaryDA_v1.png')

    

    
    

       
        
        
        
        
        
        
        
    
    
