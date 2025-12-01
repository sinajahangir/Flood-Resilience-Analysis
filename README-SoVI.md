#Census Data Analysis and Clustering: SoVI derivation

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

# Exposure Analysis
## Summary

This script computes surface water (SW) flood exposure for Calgary’s road network across three return periods (RP): 20, 100, and 500 years, using JBA flood data.

Process:
1. Loads SoVI (Social Vulnerability Index) data for Calgary Dissemination Areas (DAs), including EBC (Edge Betweenness Centrality) from the road network graph.
2. For each RP (20, 100, 500):
   - Reads per-DA exposure CSV files with flooded road segments classified by maximum flood class.
   - Calculates exposure as: (number of flooded segments / total segments) × 100 × EBC (scaled by 1e7).
   - If no flooding data is available, exposure is set to 0.
3. Exports results:
   - Writes CSV files with exposure values per DA.
   - Creates shapefiles with exposure mapped to DA geometries.
4. Generates maps using `RdYlGn_r` showing exposure per DA, zoomed to Calgary’s center, with a colorbar and title showing the return period.

# Road Weight
## Summary

This script computes road network density and importance metrics for Calgary's Dissemination Areas (DAs) based on road type classifications.

**Main Process:**

1. **Loads road data:**
   - Reads clipped road network shapefiles for each DA from the `ClipRoad` folder
   - Each shapefile contains road segments with classification (`ROADCLASS`) and length attributes

2. **Defines road class weights:**
   - Assigns importance weights to road types (multiples of 2, 1–512):
     - Rapid Transit: 512
     - Freeway: 256
     - Expressway/Highway: 128
     - Arterial: 64
     - Resource/Recreation: 32
     - Collector: 16
     - Ramp: 8
     - Local/Street types: 4
     - Alleyway/Lane: 2
     - Service Lane: 1

3. **Calculates metrics per DA:**
   - **RoadLength**: Total length of all road segments in the DA
   - **RoadW1_L**: Weighted importance metric = sum of (weight / length) for each road segment, reflecting the importance-to-length ratio

4. **Updates shapefile:**
   - Adds `RoadLength` and `RoadW1_L` as new attributes to the main Calgary DA shapefile
   - Saves the updated shapefile as `CalgaryDA_RoadAttribute_v1.shp`

These metrics (particularly `RoadW1_L`) are later used in recovery capacity calculations, where higher-weighted roads contribute more to recovery potential.


# Recovery

## Summary

This script calculates expected recovery capacity for Calgary’s Dissemination Areas (DAs) based on road network characteristics.

**Main Process:**

1. Loads data:
   - Calgary DA boundary shapefile
   - Road attribute shapefile with population, road length, and road index (importance/weight)

2. Normalizes features (min-max scaling):
   - Population (`pop`)
   - Total road length (`RoadLength`)
   - Road index/importance (`RoadW1_L`)

3. Calculates ensemble recovery:
   - Generates 50 random weight sets (w1, w2, w3) using a Dirichlet distribution (sum to 1)
   - For each set, computes: `w1 × population + w2 × road_length + w3 × road_index`
   - Takes the mean across all 50 samples to get expected recovery

4. Rescales recovery values to a 0–100 range for visualization

5. Exports results:
   - Adds recovery values to the DA shapefile
   - Creates a choropleth map using the `RdYlGn` colormap, zoomed to Calgary’s center
   - Saves the figure as `Recovery_CalgaryDA_v1.png`

Recovery reflects the capacity to recover from disruptions by combining population, road infrastructure length, and road importance using a probabilistic weighting scheme.

# Flood sampling
## Summary

This script samples flood raster data for road network segments across multiple return periods using parallel processing for efficiency on HPC systems.

**Main Process:**

1. **Identifies input files:**
   - Finds all clipped road network shapefiles (`.shp`) in the `ClipRoad` directory
   - Each shapefile represents road segments for a specific Dissemination Area (DA)

2. **Defines flood scenarios:**
   - Processes seven return periods (RP): 20, 50, 75, 100, 200, 500, and 1500 years
   - Uses riverine flood (RF) type raster files from JBA (format: `CA_202012_FLRF_U_RP{d}_RB_30m_4326.tif`)

3. **Samples flood rasters per road segment:**
   - For each road segment in a shapefile:
     - Extracts the bounding box corners (min-min, min-max, max-max, max-min)
     - Samples the flood raster at these four corner coordinates
     - Takes the maximum value among the four samples as the flood exposure class for that segment
   - This approach captures the maximum flood depth/class intersecting each road segment

4. **Exports results:**
   - Writes CSV files for each DA and return period
   - Format: `Exposure_FID_{ii}_v1.csv` containing the 'Maximum class' for each road segment
   - Files are organized in directories like `RF_SampleJBA_RP={rp}/`

5. **Parallel processing:**
   - Uses multiprocessing to process all seven return periods simultaneously
   - Automatically detects available CPUs from the SLURM environment variable (`SLURM_CPUS_PER_TASK`) for HPC clusters

The resulting exposure CSVs are then used in downstream analysis (e.g., `CalculateExposure_Calgary_Road_JBA.py`) to calculate aggregate flood exposure metrics per DA.

# Bayesian network input
## Summary

This script prepares exposure analysis data as input to a Bayesian Belief Network (BBN) by extracting, computing, and categorizing variables from road network exposure data.

**Main Process:**

1. **Loads exposure data:**
   - Reads pre-computed exposure CSV files (from `CalculateExposure_Calgary_Road_JBA.py`)
   - Currently processes return period 100 (configurable in the loop)
   - File format: `ExposureRoad_EBC_Clagary_{rp}_JBA_SW_v1.csv` (includes Edge Betweenness Centrality)

2. **Computes and categorizes variables:**

   - **Population density (`pop_d`)**: Population divided by area (pop/a)
   
   - **Population density class (`pop_d_c`)**: Categorized using percentiles:
     - Low: < 30th percentile
     - Moderate: 30th–95th percentile  
     - High: > 95th percentile
   
   - **Flood exposure (`f_exp`)**: Continuous exposure values (directly from input)
   
   - **Flood exposure class (`f_exp_c`)**: Categorized using the same percentile thresholds:
     - Low: < 30th percentile
     - Moderate: 30th–95th percentile
     - High: > 95th percentile
   
   - **Road class (`rc`)**: First word of the RoadClass attribute (e.g., "Arterial", "Local")
   
   - **Return period (`rp`)**: The return period value (100 in current configuration)

3. **Exports BBN input:**
   - Combines all processed variables into a single DataFrame
   - Removes rows with missing values
   - Saves as `Exposure_All_BBFInput_v1.csv` for use in the Bayesian Belief Network

The output provides both continuous and discrete (categorized) variables that the BBN can use to model relationships between population density, road characteristics, and flood exposure.

# Bayesian Belief Network
## Summary

This notebook constructs and uses a Bayesian Belief Network (BBN) to model relationships between flood exposure, population density, road characteristics, and return periods for the Calgary road network analysis.

**Main Process:**

1. **Data Preparation:**
   - Loads the preprocessed CSV file (`Exposure_All_BBFInput_v1.csv`) generated by `Exposure_BBN_DataGenerator_v1.py`
   - Maps return period values to categorical classes:
     - RP 500 → 'High'
     - RP 100 → 'Moderate'
     - RP 20 → 'Low'

2. **Network Structure Definition:**
   - Variables: `pop_d_c` (population density class), `rp` (return period), `rc` (road class), `f_exp_c` (flood exposure class)
   - Defines directed edges:
     - `pop_d_c` → `f_exp_c`
     - `rp` → `f_exp_c`
     - `rc` → `f_exp_c`
     - `pop_d_c` → `rc`

3. **Model Training:**
   - Creates a `DiscreteBayesianNetwork` with the defined structure
   - Fits Conditional Probability Distributions (CPDs) using Expectation-Maximization algorithm
   - Manually sets return period prior probabilities:
     - Low (RP 20): 0.8 (80%)
     - Moderate (RP 100): 0.16 (16%)
     - High (RP 500): 0.04 (4%)

4. **Probabilistic Inference:**
   - Uses Variable Elimination for queries
   - Examples:
     - Given high flood exposure, infer road class probabilities
     - Given high flood exposure, infer population density class probabilities
     - Given return period, population density, and road class, predict flood exposure
     - Compare road class distributions for high vs. low population density areas

5. **Model Export:**
   - Saves the trained BBN model in BIF (Bayesian Interchange Format) as `BBN_Model_RoadNetwork.bif` for future use

The BBN captures probabilistic dependencies to support predictive inference and scenario analysis for flood exposure based on population density, road infrastructure type, and flood return periods.