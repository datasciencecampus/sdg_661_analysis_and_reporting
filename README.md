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

## UK Results
The results for the UK can be found in `water_type_w_total.csv` and `water_extent_change.csv`. 

### Water Extent
`water_type_w_total.csv` contains the spatial extent for each of the water types that can be derived from the Global Surface Water Explorer data (Permanent, Seasonal, and Ephemeral), aggregated to HydroBASINs from 1984 to 2019. It also contains the spatial extent expressed as a proportion of the HydroBASIN's area.

 Columns |  |
| :---: | :---: |
| HYBAS_ID | Unique HydroBASIN ID |
| area | Area of the  HydroBASIN (km<sup>2</sup>) |
| Year | Year of GSWE data |
| Ephemeral | Spatial extent of ephemeral water (km<sup>2</sup>) |
| Seasonal | Spatial extent of seasonal water (km<sup>2</sup>) |
| Permanent | Spatial extent of permanent water (km<sup>2</sup>) |
| % Ephemeral | Proportion of HydroBASIN area that is ephemeral water|
| % Seasonal | Proportion of HydroBASIN area that is seasonal water |
| % Permanent | Proportion of HydroBASIN area that is permanent water|


### Water Extent Change
As described by the [indicators metadata](https://unstats.un.org/sdgs/metadata/files/Metadata-06-06-01a.pdf), is calculated as:

<a href="https://www.codecogs.com/eqnedit.php?latex=Percentage&space;Change&space;in&space;Spatial&space;Extent&space;=&space;\frac{\left&space;(\beta&space;-\gamma&space;\right&space;)}{\beta&space;}\times&space;100" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Percentage&space;Change&space;in&space;Spatial&space;Extent&space;=&space;\frac{\left&space;(\beta&space;-\gamma&space;\right&space;)}{\beta&space;}\times&space;100" title="Percentage Change in Spatial Extent = \frac{\left (\beta -\gamma \right )}{\beta }\times 100" /></a>

where:  
<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;\beta&space;=" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;\beta" title="\beta" /></a> = the average national extent from 2001-2005  
<a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;\beta&space;=" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;\gamma" title="\gamma" /></a> = the average national extent of any other 5-year period

The results for the UK can be found in `water_extent_change.csv` and describes the spatial extent change from the baseline to 2010-14 and 2015-2019.
