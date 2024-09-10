# -*- coding: utf-8 -*-
"""
@author: Sina Jahangir
# This script reads a CSV file into a pandas DataFrame, calculates the Pearson correlation 
# coefficient between all numerical columns, and visualizes the resulting correlation matrix 
# as a heatmap using matplotlib. The heatmap provides an intuitive way to assess the strength 
# and direction of linear relationships between the variables, where values close to +1 or 
# -1 indicate strong correlations, and values near 0 suggest weak or no linear relationship.

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
Date: August 2024
**
Usage: 1-This version was used to check the cross-correlation (linear) between
the deriving variables of SoVI in the city of Calgary using 2021 census data
2-Clustering using k-means was applied to derive the SoVI index related to pluvial
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
#%%
#change directory to the mother folder containing the census data (csv)
#this should be changed
chdir(r'D:\NRC')
#%%Reading the census data
#The data should be in csv format
#The name should be changed
df_da=pd.read_csv('DA_Calgary_Variables_v1.csv')
#%%
#Subsetting
da=df_da.iloc[:,7:]
#%%
# Calculate Pearson correlation coefficient
correlation_matrix = da.corr(method='pearson')
#%%
# Set correlation values lower than 0.5 to NaN
#This for better visuilazation
correlation_matrix[abs(correlation_matrix) < 0.5] = np.nan
#%%
# Calculate the number of non-NaN values for each variable
non_nan_counts = correlation_matrix.notna().sum()
#%%
# Sort the variables based on the number of non-NaN counts in descending order
non_nan_counts_sorted = non_nan_counts.sort_values(ascending=False)

# Plot the bar plot
plt.figure(figsize=(12, 8))
bars = plt.bar(non_nan_counts_sorted.index, non_nan_counts_sorted.values, color='#E05C5C',edgecolor='black')

# Add title and labels
plt.title('Number of Significant Correlations (≥ 0.5) per Variable', fontsize=16)
plt.xlabel('Variables', fontsize=14)
plt.ylabel('Number of Significant Correlations', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right', fontsize=12)

# Add the value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', fontsize=12)
#%%
# Plot heatmap using matplotlib
plt.figure(figsize=(12, 12))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none', aspect='auto')
plt.colorbar()

# Add ticks and labels
plt.xticks(np.arange(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45, ha='right')
plt.yticks(np.arange(len(correlation_matrix.columns)), correlation_matrix.columns)

# Add title
plt.title('Correlation Heatmap')

# Add correlation coefficient values on the heatmap
for i in range(len(correlation_matrix.columns)):
    for j in range(len(correlation_matrix.columns)):
        if not np.isnan(correlation_matrix.iloc[i, j]):
            plt.text(j, i, f"{correlation_matrix.iloc[i, j]:.2f}", ha='center', va='center', color='black')
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
xticks = [1, 2, 4, 6, 8, 10, 12,14,16]  # Adjust based on your data range
plt.xticks(ticks=xticks)
#%%
# Apply K-Means clustering with the optimal number of clusters
optimal_clusters = 9

# Apply K-Means clustering
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(scaled_data)

# Add the cluster labels to the original DataFrame
da['Cluster'] = cluster_labels

#Plot the clusters if you have 2D or 3D data
plt.figure(figsize=(6, 6),dpi=300)
plt.scatter(scaled_data[:, 1], scaled_data[:,-6], c=cluster_labels, cmap='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', marker='X')
plt.title('K-Means Clustering')
plt.xlabel('Population density')
plt.ylabel('Median income')
#%%
# Specify the column to sort by: median income
#This could change
sort_column = da.columns[-6]

# Create a DataFrame with cluster labels and the sort_column
cluster_sort_df = da[['Cluster', sort_column]].copy()

# Determine the new cluster labels based on the max value in sort_column
sorted_clusters = cluster_sort_df.groupby('Cluster')[sort_column].median().sort_values(ascending=False).index
cluster_map = {cluster: i + 1 for i, cluster in enumerate(sorted_clusters)}

# Map the old cluster labels to the new labels
da['SoVI'] = da['Cluster'].map(cluster_map)
#%%
# Calculate the average value of the variable of interest for each sorted cluster
avg_values = da.groupby('SoVI')[sort_column].mean().sort_index()

# Plot the average values
plt.figure(figsize=(8, 6),dpi=400)
bars = plt.bar(avg_values.index, avg_values.values, color='#E05C5C', edgecolor='black')

# Add title and labels
plt.xlabel('SoVI Cluster', fontsize=14)
plt.ylabel('Average median income', fontsize=14)

# Add the value labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', fontsize=12)
#%%
# Importing library to save the df to shapefile
import geopandas as gpd
#%%
RP=[100]
# Load the shapefile
# Define the feature based on which you want to color the fill
feature_column = 'SoVI_KM'
for ii in RP:
    shapefile_path = r'Exposure_Shapefile_Clagary_%d_Length&EBC\ExposureRoad_Clagary_%d_Length&EBC_2024_v1.shp'%(ii,ii)
    gdf = gpd.read_file(shapefile_path)
    gdf[feature_column]=da['SoVI']
    gdf.to_file(r'SoVI_KM_Calgary_RP=%d_v1.shp'%(ii))