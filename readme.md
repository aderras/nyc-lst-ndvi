

## Introduction

This repository was created for the Earth Observations Applications for Resiliency team in NASA's Climate Change Research initiative. In it are the Jupyter notebooks and processed data used to compute land surface temperature (LST) and normalized difference vegetation index (NDVI) in New York City from the 1984 to the 2022.

## Methodology

### A. Find viable data

1. Perform a dataset search using the USGS API. We input the aliases of the desired datasets, Landsats 5 and 8, to obtain a list of dataset objects.
2. For every dataset object, search for scenes that contain lower left (`ll`) and upper right (`ur`) longitude and latitude coordinates of a square encompassing NYC. 
3. Filter the resulting scenes for:
    - Less than 10% cloud cover
    - Areas that contain the upper left `ul` and lower right `lr` corners of a square encompassing NYC. 
4. Export a list of the `displayId`s of the scenes to the file `02-data/scene-search/scene_c1_l1_displayIds.txt`. A `displayId` is a USGS identifier for the scene. The suffix `c1_l1` refers to collection 1, level 1.

### B. Download Landsat Data

To download landsat data, we use the USGS bulk downloader. The steps are:

1. **Install the bulk downloader application from [USGS](https://dds.cr.usgs.gov/bulk).** For Linux, I had to first install Java 11 in my local directory. To run the installer, I define the `INSTALL4J_JAVA_HOME` variable in my `.bash_profile` file. After refreshing terminal (or just loading the editted `.bash_profile` as the source), I make the downloaded installer executable and run it through command line. When it asks for download locations, make sure to select ones within the local directory if you do not have root access. To run the program in the future, navigate to the executable in install directory you chose.
2. **Create a bulk download request.** In the [EarthExplorer](https://earthexplorer.usgs.gov/) webpage, select `Manage Criteria`. Click on `Scene Lists` in the left menu. Then click on Landsat Product ID list. Copy and paste the Landsat IDs that were saved to `scene_c1_l1_displayIDs.txt` into the text box. Then click upload. 
3. **Select download type.** The next page asks you to select the type of image you would like for every single scene. Instead of this, click the `Options` button and select the Level-1 option, which should then select this for all the scenes.
4. **Download scenes.** Follow instructions within the bulk downloader to select scenes. 

**NOTE:** Even though USGS encourages us to use Collection 2 Landsat data, the bulk-download request returns an error whenever a Collection 2 scene is requested. This is why only Collection 1 scenes were used. (As of January 2022.)

### C. Clip Raw Data to NYC 

We clip raw Landsat data to the New York City boundary. We clip only the band numbers that are needed for land surface temperature (LST) and normalized-difference vegetation index (NDVI) calculations. The bands used are summarized in the following table.

|Satellite| Bands|
|---------|------|
|Landsat 5| 3, 4, and 6|
|Landsat 8| 4, 5, and 10|

To clip, we use python's `geopandas` and `rioxarray` libraries. The function is called `clip_and_export` and is located in `01-scripts/helpers.py`.

Clipped files are exported to the `landsat_clipped_nyc/` folder. They are given the same name as the original landsat file, prepended with "clipped_nyc_". For example, `clipped_nyc_LC08_L1TP_013032_20140731_20170304_01_T1_B10.TIF`.

### D. Compute LST and NDVI

### E. Compute Summary Statistics


## Data

LST and NDVI are computed using raw data from Landsats 5 and 8. The raw data is available from the USGS, and the scenes used are listed in [Table 1](#landsatids).

## Table 1: Landsat scenes used <a id="landsatids"></a>

A total of 114 Lansat scenes fit the search criteria. Their identifiers are in the following table. 

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
