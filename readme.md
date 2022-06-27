## Introduction

This repository was created for the Earth Observations Applications for Resiliency team in NASA's Climate Change Research initiative during 2021-2022. In it are the Jupyter notebooks and processed data used to compute land surface temperature (LST) and normalized difference vegetation index (NDVI) in New York City from 1984 to the 2022. 

## Methodology

The following was completed on a Linux Centos computer using Python 3.6.12. The steps outlined below describe the methodology in the Jupyter notebooks. 

### A. Find Viable Data

1. **Perform a dataset search using the USGS API.** All functions related to this are in the script `01-scripts/usgsAPI`, and the notebook used query the API is `00-notebooks/1_find-scenes`. We input the aliases of the desired datasets, Landsats 5 and 8, to obtain a list of dataset objects.
2. **Filter for NYC.** For every dataset object, search for scenes that contain lower left (`ll`) and upper right (`ur`) longitude and latitude coordinates of a square encompassing NYC. 
3. **Filter the resulting scenes for ones with:**
    - less than 10% cloud cover
    - areas that contain the upper left `ul` and lower right `lr` corners of a square encompassing NYC. 
4. **Save results.** Export a list of the `displayId`s of the scenes to the file `02-data/scene-search/scene_c1_l1_displayIds.txt`. A `displayId` is the USGS identifier for the scene. The suffix `c1_l1` refers to Collection 1, Level 1.

<p align="center">
<img src="https://ims.cr.usgs.gov/browse/landsat_8_c1/2015/014/032/LC08_L1TP_014032_20150826_20170225_01_T1.jpg" width="400">
</p>
<p align="center">
    <em>An example of a Landsat scene which fits the search criteria described in the text. </em>
</p>

### B. Download Landsat Data

To download Landsat data, we use the USGS bulk downloader. The steps are:

1. **Install the bulk downloader application from [USGS](https://dds.cr.usgs.gov/bulk).** For Linux, I had to first install Java 11 in my local directory. To run the installer, I define the `INSTALL4J_JAVA_HOME` variable in my `.bash_profile` file. After refreshing terminal (or just loading the editted `.bash_profile` as the source), I make the downloaded installer executable and run it through command line. When it asks for download locations, make sure to select ones within the local directory if you do not have root access. To run the program in the future, navigate to the executable in install directory you chose.
2. **Create a bulk download request.** In the [EarthExplorer](https://earthexplorer.usgs.gov/) webpage, select `Manage Criteria`. Click on `Scene Lists` in the left menu. Then click on Landsat Product ID list. Copy and paste the Landsat IDs that were saved to `scene_c1_l1_displayIDs.txt` into the text box. Then click upload. 
3. **Select download type.** The next page asks you to select the type of image you would like for every single scene. Instead of this, click the `Options` button and select the Level-1 option, which should then select this for all the scenes.
4. **Download scenes.** Follow instructions within the bulk downloader to select scenes. 

**NOTE:** Even though USGS encourages us to use Collection 2 Landsat data, the bulk-download request returns an error whenever a Collection 2 scene is requested. This is why only Collection 1 scenes were used. (As of February 2022.)

### C. Clip Raw Data to NYC 

We clip raw Landsat data to the New York City boundary. We clip only the band numbers that are needed for LST and NDVI calculations. The bands used are summarized in the following table.

|Satellite| Bands|
|---------|------|
|Landsat 5| 3, 4, and 6|
|Landsat 8| 4, 5, and 10|

To clip, we use python's `geopandas` and `rioxarray` libraries. The function is called `clip_and_export` and is located in `01-scripts/helpers.py`.

Clipped files are exported to the `landsat_clipped_nyc/` folder. They are given the same name as the original Landsat file, prepended with "clipped_nyc_". For example, `clipped_nyc_LC08_L1TP_013032_20140731_20170304_01_T1_B10.TIF`.


### D. Compute LST and NDVI

Two Jupyter notebooks are created to compute LST and NDVI for Landsats 5 and 8. The input data are the clipped NYC TIF files and metadata files obtained with the raw Landsat data.

To compute LST, we follow the procedure outline by McConnell et al. in their 2022 paper. The steps are 

1. Convert Band 6 to Top of Atmosphere (TOA) spectral radiance using two constants from Landsat metadata
2. Compute brightness temperature using TOA and 2 constants from metadata
3. Compute NDVI using 
\begin{align}
\frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}
\end{align}
4. Convert NDVI to vegetation fraction
5. Compute emissivity
6. Compute LST using brightness temperature, emissivity, and some constants (specified in McConnell's paper)

Data is exported to the folders `02-data/ndvi_clipped_nyc` and `02-data/lst_clipped_nyc`. The exported filenames contain the parameter computed with the truncated Landsat filename. For example, the file `ndvi_LT05_L1TP_013032_19910801_20160929_01_T1.tif` contains the NDVI calculation in NYC obtained Landsat files `LT05_L1TP_013032_19910801_20160929_01_T1_BX`, where the `X` refers to bands 3, 4, or 6.

<p align="center">
<img src="https://github.com/aderras/nyc-lst-ndvi/blob/main/03-figs/lst_LT05_L1TP_014032_20110831_20160831_01_T1.png" width="600">
</p>
<p align="center">
    <em>An example of land surface temperature computed in NYC using raw data from the Landsat files "LT05_L1TP_014032_20110831_20160831_01_T1". Temperature scale is in Kelvin. </em>
</p>

### E. Compute Summary Statistics

Having computed LST and NDVI across NYC, we compute summary statistics within HOLC grades. We compute the 

- mean
- median
- minimum
- maximum
- standard deviation

of the LST and NDVI within every HOLC boundary and save the results to a CSV file, `summary_stats/stats_lst_LANDSAT-IDENTIFIER.csv`. For every Landsat file, we end up with a set of mean pixels, median pixels, etc, associated with every HOLC boundary. Each boundary forms a row in the exported summary statistics file.

We additionally compute aggregate summary statistics. For every Landsat file, we compute the mean of the medians for each HOLC grade, along with the mean of the means, mean of the minima, etc. Results are stored as a row in the aggregated statistics file in `summary_stats_agg/lst_mean_stats_combined.csv` and `summary_stats_agg/ndvi_mean_stats_combined.csv`

## Data

LST and NDVI are computed using raw data from Landsats 5 and 8. The raw data is available from the USGS, and the scenes used are listed in [Table 1](#landsatids). Data sources, data types, and naming conventions for the raw and processed data are shown in [Tables 2](#raw-data) and [3](#processed-data). All data is stored in the `02-data/` folder of the project. All folders referred to below are with respect to this one. 

### Table 1: Landsat scenes used <a id="landsatids"></a>

A total of 113 Landsat scenes fit the search criteria. Their identifiers are stored in `scene-search/scene_c1_l1_displayIDs"` and are listed in the following table. 

| Landsat IDs |
|------------------------------------------|
| LC08_L1TP_014032_20130820_20170309_01_T1 |
| LC08_L1TP_013032_20140917_20170303_01_T1 |
| LC08_L1TP_014032_20140807_20170304_01_T1 |
| LC08_L1TP_013032_20140731_20170304_01_T1 |
| LC08_L1TP_014032_20140706_20170304_01_T1 |
| LC08_L1TP_014032_20150826_20170225_01_T1 |
| LC08_L1TP_013032_20150803_20170226_01_T1 |
| LC08_L1TP_014032_20150725_20170226_01_T1 |
| LC08_L1TP_014032_20160828_20170221_01_T1 |
| LC08_L1TP_014032_20160812_20170222_01_T1 |
| LC08_L1TP_013032_20160805_20170222_01_T1 |
| LC08_L1TP_014032_20160727_20170222_01_T1 |
| LC08_L1TP_013032_20160720_20170222_01_T1 |
| LC08_L1TP_013032_20170909_20170927_01_T1 |
| LC08_L1TP_014032_20170730_20170811_01_T1 |
| LC08_L1TP_014032_20180903_20180912_01_T1 |
| LC08_L1TP_013032_20180710_20180717_01_T1 |
| LC08_L1TP_014032_20190922_20190926_01_T1 |
| LC08_L1TP_013032_20190830_20190916_01_T1 |
| LC08_L1TP_013032_20190729_20190801_01_T1 |
| LC08_L1TP_013032_20190713_20190719_01_T1 |
| LC08_L1TP_014032_20210826_20210901_01_T1 |
| LT05_L1TP_014032_19840921_20161004_01_T1 |
| LT05_L1TP_014032_19840719_20161004_01_T1 |
| LT05_L1TP_013032_19850917_20161004_01_T1 |
| LT05_L1TP_013032_19850901_20161004_01_T1 |
| LT05_L1TP_014032_19850823_20161004_01_T1 |
| LT05_L1TP_014032_19870914_20161003_01_T1 |
| LT05_L1TP_014032_19880916_20161003_01_T1 |
| LT05_L1TP_014032_19880831_20161003_01_T1 |
| LT05_L1TP_014032_19880815_20161003_01_T1 |
| LT05_L1TP_013032_19880808_20161002_01_T1 |
| LT05_L1TP_014032_19880730_20161003_01_T1 |
| LT05_L1TP_014032_19880628_20161003_01_T1 |
| LT05_L1TP_013032_19880621_20161002_01_T1 |
| LT05_L1TP_014032_19890903_20161002_01_T1 |
| LT05_L1TP_013032_19890726_20161002_01_T1 |
| LT05_L1TP_014032_19890701_20161002_01_T1 |
| LT05_L1TP_013032_19900830_20161001_01_T1 |
| LT05_L1TP_014032_19900720_20161002_01_T1 |
| LT05_L1TP_014032_19900704_20161002_01_T1 |
| LT05_L1TP_013032_19910902_20161001_01_T1 |
| LT05_L1TP_013032_19910817_20160929_01_T1 |
| LT05_L1TP_013032_19910801_20160929_01_T1 |
| LT05_L1TP_013032_19910716_20160929_01_T1 |
| LT05_L1TP_014032_19910621_20160929_01_T1 |
| LT05_L1TP_013032_19920920_20160929_01_T1 |
| LT05_L1TP_014032_19920826_20160928_01_T1 |
| LT05_L1TP_014032_19930829_20160927_01_T1 |
| LT05_L1TP_014032_19930728_20160928_01_T1 |
| LT05_L1TP_014032_19930626_20160928_01_T1 |
| LT05_L1TP_013032_19940910_20160927_01_T1 |
| LT05_L1TP_013032_19940825_20160927_01_T1 |
| LT05_L1TP_013032_19940809_20160927_01_T1 |
| LT05_L1TP_013032_19940708_20160927_01_T1 |
| LT05_L1TP_013032_19940622_20160927_01_T1 |
| LT05_L1TP_014032_19950904_20160926_01_T1 |
| LT05_L1TP_014032_19950819_20160926_01_T1 |
| LT05_L1TP_013032_19950727_20160927_01_T1 |
| LT05_L1TP_013032_19960830_20160924_01_T1 |
| LT05_L1TP_014032_19960805_20160924_01_T1 |
| LT05_L1TP_014032_19960720_20160924_01_T1 |
| LT05_L1TP_013032_19960627_20160924_01_T1 |
| LT05_L1TP_014032_19970621_20160923_01_T1 |
| LT05_L1TP_014032_19980912_20160923_01_T1 |
| LT05_L1TP_013032_19980905_20160924_01_T1 |
| LT05_L1TP_013032_19980820_20160922_01_T1 |
| LT05_L1TP_013032_19980703_20160922_01_T1 |
| LT05_L1TP_013032_19990823_20160919_01_T1 |
| LT05_L1TP_013032_19990706_20160919_01_T1 |
| LT05_L1TP_014032_20000917_20160918_01_T1 |
| LT05_L1TP_013032_20000825_20160918_01_T1 |
| LT05_L1TP_014032_20000816_20160918_01_T1 |
| LT05_L1TP_013032_20000708_20160922_01_T1 |
| LT05_L1TP_013032_20010913_20160917_01_T1 |
| LT05_L1TP_013032_20010727_20160917_01_T1 |
| LT05_L1TP_014032_20010702_20160917_01_T1 |
| LT05_L1TP_014032_20020907_20160916_01_T1 |
| LT05_L1TP_013032_20020815_20160916_01_T1 |
| LT05_L1TP_014032_20020806_20160916_01_T1 |
| LT05_L1TP_014032_20020705_20160916_01_T1 |
| LT05_L1TP_014032_20030910_20160914_01_T1 |
| LT05_L1TP_014032_20030825_20160915_01_T1 |
| LT05_L1TP_013032_20030717_20160915_01_T1 |
| LT05_L1TP_013032_20030701_20160915_01_T1 |
| LT05_L1TP_013032_20040820_20160914_01_T1 |
| LT05_L1TP_013032_20040703_20160913_01_T1 |
| LT05_L1TP_013032_20050908_20160912_01_T1 |
| LT05_L1TP_013032_20050823_20160912_01_T1 |
| LT05_L1TP_014032_20050814_20160912_01_T1 |
| LT05_L1TP_014032_20060918_20160911_01_T1 |
| LT05_L1TP_014032_20060801_20160911_01_T1 |
| LT05_L1TP_014032_20060716_20160909_01_T1 |
| LT05_L1TP_014032_20070921_20160906_01_T1 |
| LT05_L1TP_014032_20070905_20160910_01_T1 |
| LT05_L1TP_014032_20070804_20160907_01_T1 |
| LT05_L1TP_013032_20070712_20160907_01_T1 |
| LT05_L1TP_014032_20070703_20160908_01_T1 |
| LT05_L1TP_013032_20070626_20160907_01_T1 |
| LT05_L1TP_014032_20080907_20160909_01_T1 |
| LT05_L1TP_013032_20080831_20160905_01_T1 |
| LT05_L1TP_014032_20080822_20160905_01_T1 |
| LT05_L1TP_013032_20090919_20160903_01_T1 |
| LT05_L1TP_014032_20090825_20160903_01_T1 |
| LT05_L1TP_013032_20090818_20160903_01_T1 |
| LT05_L1TP_013032_20100922_20160831_01_T1 |
| LT05_L1TP_013032_20100906_20160831_01_T1 |
| LT05_L1TP_014032_20100828_20160831_01_T1 |
| LT05_L1TP_013032_20100704_20160901_01_T1 |
| LT05_L1TP_014032_20110916_20160830_01_T1 |
| LT05_L1TP_014032_20110831_20160831_01_T1 |
| LT05_L1TP_014032_20110730_20160831_01_T1 |
| LT05_L1TP_014032_20110714_20160831_01_T1 |
| LT05_L1TP_013032_20110707_20160831_01_T1 |

### Table 2: Raw Data <a id="raw-data"></a>

| Description | Location | Data type | Source | Naming convention | 
|--|--|--|--|--|
| List of Landsat scenes used | `scene-search/` | TXT | USGS API | "scene_c1_l1_displayIds.txt" | 
| Landsat data | External hard drive | TIF, TXT | USGS | See [USGS website](https://www.usgs.gov/faqs/what-naming-convention-landsat-collections-level-1-scenes#:~:text=L%20%3D%20Landsat,%E2%80%9C08%E2%80%9D%3DLandsat%208) |
| NYC boundary shapefiles | `boundaries/nyc/` and `boundaries/nyc_boroughs` | ".shp" | NOT SURE |"nyc" for the whole city and "nybb" for boroughs |
| NYC HOLC shapefiles | `boundaries/holc_nyc/` and the folders within | ".shp" | NOT SURE | The shapefiles themselves are called "cartodb-query.shp", and each borough's shapefile is within a the folder `NYBoroughNameYearCreated/` |

### Table 3: Processed Data <a id="processed-data"></a>

Below we refer to an identifier called **TRUNCATED-LANDSAT-FILENAME**. This is the Landsat identifier with band number omitted. E.g. "LC08_L1TP_013032_20140731_20170304_01_T1_B4.TIF" has the truncated identifier "LC08_L1TP_013032_20140731_20170304_01_T1"

| Description | Location | Data type | Naming convention | 
|----|--|--|----|
| Clipped Landsat data | `landsat_clipped_nyc/` | TIF | "clipped_nyc_**RAW-LANDSAT-FILENAME**.TIF" |
| LST | `lst_clipped_nyc/` | TIF | "lst_**TRUNCATED-LANDSAT-FILENAME**.TIF" |
| NDVI | `ndvi_clipped_nyc/` | TIF | "ndvi_**TRUNCATED-LANDSAT-FILENAME**.TIF" |
| Summary statistics | `summary_stats` | CSV | "stats_lst_**TRUNCATED-LANDSAT-FILENAME**.csv" and "stats_ndvi_**TRUNCATED-LANDSAT-FILENAME**.csv" |
| Aggregated summary statistics | `summary_stats_agg` | CSV | `lst_mean_stats_combined` and `ndvi_mean_stats_combined` |