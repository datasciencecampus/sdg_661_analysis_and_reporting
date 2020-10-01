# sdg_661_analysis_and_reporting

The Sustainable Development Goals (SDGs) have been developed by the United Nations as a “blueprint to achieve a better and more sustainable future for all”; designed to end poverty, 
halt climate change and reduce inequalities. The SDGs are made up of 17 goals and 244 indicators, making the mandate placed on all National Statistics Institutes to report on the 
SDGs a huge challenge. 

This open-source tool looks to report on one of the 244 SDG indicators, 6.6.1:: Change in the extent of water-related ecosystems over time. The indicator focuses on water-related 
ecosystems that provide an important service to society, including open waters (rivers and estuaries, lakes and reservoirs), wetlands (peatland and reedbeds), and groundwater aquifers.  

## Data
Here we use the Global Surface Water Explorer (GSWE) dataset developed by UN Environment Programme (UNEP), the European Commission Joint Research Council, and Google. GSWE is based on satellite imagery from the past 35 years. Currently 
GSWE measures changes in the distribution of inland open water e.g., lakes and reservoirs, a sub-indicator of 6.6.1.

GSWE is globaly and publicaly availabe, and can be extracted via the [Google Earth Engine](https://earthengine.google.com/)

## Extracting GSWE
Code has been developed to extract GSWE data to Google Drive using the `GSWE_reporting` package. 

```
import ee
from GSWE_reporting import extract_gswe

ee.Authenticate()
ee.Initialize()  

geometry = ee.Geometry.Polygon( 
        [[[-12.598544729822379, 61.78863494939058],
          [-12.598544729822379, 49.00174346741333],
          [3.749111520177621, 49.00174346741333],
          [3.749111520177621, 61.78863494939058]]]) ## UK bounding box
          
extract_gswe('JRC/GSW1_2/YearlyHistory', geometry, 1984, 2020, 'GSWE_exports')
```

## Reprojecting GSWE
The GSWE is exported into WGS84 and when calculating water extent should be reprojected into a projected coordinate system

```
from GSWE_reporting import get_gswe_paths, reproject_GSWE

gswe_files = get_gswe_paths('./GSW_output/', '.tif')
reproject_GSWE(gsw_files, '+proj=utm +zone=30 +ellps=WGS84 +datum=WGS84 +units=m +no_defs ')
```

## Preparing the boundary file
Water extent is aggregated to hydroBASINs (a series of polygon layers that depict watershed boundaries). They can be downloaded the HydroSHEDS page [here](https://hydrosheds.org/page/hydrobasins).
This is then clipped to a national boundary to ensure coastal waters are not included in reporting of inland waters.

```
from GSWE_reporting import clip_basin_to_boundary
hydrobasin_clipped = clip_basin_to_boundary(hydrobasin, boundary, target_crs)
```


## Calculating Water Extent
With both the boundary and GSWE data processed, inland water extent can be calculated:

```
from GSWE_reporting import surface_water_extent

gsw_file_path_list = get_gswe_paths('./Reprojected/', 'UTM.tif')
hydro_basin = gpd.read_file('./boundaries/boundary.shp')
water_extent = surface_water_extent(gsw_file_path_list, hydro_basin)
```


