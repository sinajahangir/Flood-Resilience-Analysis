# -*- coding: utf-8 -*-
"""
@author: Sina Jahangir
# This script reads the exposure shapefiles (derived beforehand), uses k-means
# clustering to cluster it alongside the socio-economic variables, and finally
# derives resilience categorization accordingly

#Note: The main difference between this version and the previous one (v1.01) is
# how exposure was claculated. Also, any row having a NaN value in any columns
# is set to NaN

#Note: It seems that the DAs with the most flood exposure have missing census data

# -------------------------------------------
# K-Means Clustering Description:
# 
# K-Means is an unsupervised machine learning algorithm that partitions the dataset 
# into 'K' distinct clusters. The algorithm works by assigning each data point 
# to the nearest cluster center (centroid) based on Euclidean distance.
# 
# The algorithm iteratively updates the positions of the centroids to minimize 
# the Within-Cluster Sum of Squares (WCSS), a measure of the compactness of 
# the clusters. The objective is to minimize WCSS across all clusters.
# 
# The optimal number of clusters can be determined using the elbow method, 
# where WCSS is plotted against the number of clusters, and the "elbow" point 
# in the plot suggests a suitable number of clusters.
# 
# In this context, the code scales the data, applies K-Means clustering with 
# the optimal number of clusters determined from the elbow method, and then 
# labels each data point with its respective cluster. The clusters are further 
# sorted based on a specified column, and the analysis continues from there.
# -------------------------------------------

***
All Rights Reserved.
   Copyright [2024] [SinaJahangir].
   Contact: [mohammadsina.jahangir@gmail.com]
***
Date: September 2024
**
Usage: 1-Clustering using k-means was applied to derive the resilience index related to pluvial
flooding
"""
#%%Import necessary libraries
#Before using this code, ensure you have the following dependencies installed:
'''
Python (version 3.75 or higher preferrably)
NumPy
Pandas
SciPy
Matplotlib
sklearn
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from os import chdir
import geopandas as gpd
#%%
#change directory to the mother folder containing the census data (csv)
#this should be changed
chdir(r'D:\NRC')
#%%Reading the census data
#The data should be in csv format
#The name should be changed
df_da=pd.read_csv('DA_Calgary_Variables_Resilience.csv')
#%%
#Selecting census data
da=df_da.iloc[:,3:]
#%%
#Reading shapefile associated with the RP of intrest.e.g., 100 years
RP=[100]
for ii in RP:
    shapefile_path = r'Exposure_Shapefile_Clagary_%d_Length\ExposureRoad_Clagary_%d_Length_2024_v1.shp'%(ii,ii)
    gdf = gpd.read_file(shapefile_path)
#subsetting exposure
exposure=gdf['Exposure']
#%%
#Appending exposure df to census df
da['exposure']=exposure
#%%
# Set all rows containing at least one NaN to NaN for all columns
da.loc[da.isna().any(axis=1)] = np.nan
#%%
#Applying k-means for clustering
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
#%%
# Handle missing values by replacing NaN with column averages before scaling
imputer = SimpleImputer(strategy='mean')
data_with_imputed_values = imputer.fit_transform(da)
# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_with_imputed_values)
#%%
# Calculate WCSS for different numbers of clusters
wcss = []
max_clusters = 16

for i in range(1, max_clusters + 1):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)  # inertia_ is the WCSS for each cluster

# Plot the elbow method graph
plt.figure(figsize=(6, 6),dpi=300)
plt.plot(range(1, max_clusters + 1), wcss, marker='o', linestyle='--',color='k',linewidth=2)
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xlabel('Number of Clusters')
#Within-Cluster Sum of Squares
plt.ylabel('WCSS')
# Set x-ticks to be multiples of 2, starting from 1
xticks = np.arange(1,max_clusters,2)  # Adjust based on your data range
plt.xticks(ticks=xticks)
#%%
# Apply K-Means clustering with the optimal number of clusters
optimal_clusters = 7

# Apply K-Means clustering
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(scaled_data)

# Add the cluster labels to the original DataFrame
da['Cluster'] = cluster_labels

#Plot the clusters if you have 2D or 3D data
plt.figure(figsize=(6, 6),dpi=300)
plt.scatter(scaled_data[:, 0], scaled_data[:,-1], c=cluster_labels, cmap='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', marker='X')
plt.title('K-Means Clustering')
plt.xlabel('Population density')
plt.ylabel('Exposure')
#%%
# Specify the column to sort by: exposure
# This could change
sort_column = 'exposure'

# Create a DataFrame with cluster labels and the sort_column
cluster_sort_df = da[['Cluster', sort_column]].copy()

# Determine the new cluster labels based on the max value in sort_column
sorted_clusters = cluster_sort_df.groupby('Cluster')[sort_column].median().sort_values(ascending=False).index
cluster_map = {cluster: i + 1 for i, cluster in enumerate(sorted_clusters)}

# Map the old cluster labels to the new labels
da['RES'] = da['Cluster'].map(cluster_map)
#%%
# Calculate the average value of the variable of interest for each sorted cluster
avg_values = da.groupby('RES')[sort_column].mean().sort_index()

# Plot the average values
plt.figure(figsize=(8, 6),dpi=400)
bars = plt.bar(avg_values.index, avg_values.values, color='#E05C5C', edgecolor='black')

# Add title and labels
plt.xlabel('RES Cluster', fontsize=14)
plt.ylabel('Exposure', fontsize=14)

# Add the value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval,2), ha='center', fontsize=12)
#%%
#classify labels
#This is subjective and data driven
da['class_res']='Low'
da['class_res'][da['RES']>2]='High'
#%%
#remove "exposure" column from the dataframe. This is already saved the gdf
da = da.drop('exposure', axis=1)
#%%
def classify_column(series):
    mean = series.mean()
    std = series.std()
    # Classify values based on mean and standard deviation
    return series.apply(lambda x: 'Low' if x < (mean - std)
                       else 'High' if x > (mean + std)
                       else 'Moderate')
#%%
#classifying each column based on quantiles (0.33,)
census_df=da.iloc[:,:-3]
classified_df = census_df.apply(classify_column)
#%%
#concat to create a single dataframe
df_res=pd.concat((classified_df,da['class_res']),axis=1)
#save shapefile
for ii in df_res.columns:
    gdf[ii]=df_res[ii]
gdf.to_file(r'RS_KM_Calgary_RP=%d_v1.1.shp'%(RP[0]))