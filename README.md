Census Data Analysis and Clustering

This project involves analyzing census data, performing correlation analysis, and applying K-means clustering to uncover patterns and insights. The results are visualized through various plots, including a heatmap of correlation coefficients and a bar plot of significant correlations.

This project aims to:

1-Analyze the census data by calculating Pearson correlation coefficients between different variables.
2-Identify and visualize significant correlations.
3-Apply K-Means clustering to categorize the data into meaningful clusters.
4-Sort and rank clusters based on specific variables like median income.
5-Export the clustering results as shapefiles for geographical analysis.

Data Preparation
The first step is to read and prepare the census data:

Change Directory: Ensure the script points to the correct directory where the census data CSV file is stored.
Read the Data: Load the census data from a CSV file into a Pandas DataFrame.

Convert to Array: Extract relevant columns for analysis.

Correlation Analysis: The project calculates Pearson correlation coefficients between the variables:

Correlation Matrix: This function computes the correlation matrix and filters out insignificant correlations (values lower than 0.5 are set to NaN for clarity).
Non-NaN Count: Counts the number of significant correlations for each variable.
The results are visualized using:

Bar Plot: Displays the number of significant correlations per variable, sorted in descending order.
Heatmap: Visualizes the correlation matrix, with annotations for correlation coefficients.

K-Means Clustering
Elbow Method
To determine the optimal number of clusters:

Elbow Method: The Within-Cluster Sum of Squares (WCSS) is calculated for different cluster numbers. The "elbow" point in the resulting plot indicates the optimal number of clusters.
Clustering
Once the optimal number of clusters is identified:

K-Means Clustering: The data is clustered into the identified number of clusters.
Cluster Labeling: Cluster labels are assigned, and clusters are sorted and renumbered based on a specific variable (e.g., median income).

Visualization
Cluster Plot: Visualizes the clusters with scatter plots.
Bar Plot: Shows the average value of the variable of interest across sorted clusters.
Exporting Results
The clustered data is exported as shapefiles for further geographical analysis:

Shapefile Export: The results are saved as shapefiles with the cluster labels.
