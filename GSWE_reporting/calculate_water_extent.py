# stdlib
import os
import glob

# third-party
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.ops import unary_union

def clip_basin_to_boundary(hydrobasin, national_boundary, target_crs = '+proj=utm +zone=30 +ellps=WGS84 +datum=WGS84 +units=m +no_defs '):
	"""Clips hydrobasins to national boundary
	
	Args:
	    hydrobasin (GeoDataFrame): GeoDataFrame of HydroBASINs
	    national_boundary (GeoDataFrame): Description
	    target_crs (STR): Coordinate Reference System for hydroBASIN clip, defaults to WGS 84
	
	Returns:
	    GeoDataFrame: GeoDataFrame of hydroBASIN clipped to the national boundary
	"""
	if len(national_boundary) != 1:
		print('union national boundary')
		boundary_union = national_boundary.unary_union
		national_boundary = gpd.GeoDataFrame(crs = national_boundary.crs, geometry = [boundary_union])

	hydrobasin = hydrobasin.to_crs(target_crs) 
	national_boundary = national_boundary.to_crs(target_crs)

	xmin, ymin, xmax, ymax = national_boundary.total_bounds
	national_hydrobasin = hydrobasin.cx[xmin:xmax, ymin:ymax]

	hydrobasins_clipped = gpd.overlay(national_hydrobasin, national_boundary, how='intersection')

	return hydrobasins_clipped

def get_gswe_paths(dirpath, extension = '.tif'):
	"""Lists local files in the directory path with the extension
	
	Args:
	    dirpath (STR): directory path of GSWE exports
	    extension (TYPE): extension of GSWE exports, defaults to '.tif'
	
	Returns:
	    List: List of GSWE exports
	"""

	extension = '*' + extension
	path = os.path.join(dirpath, extension)
	file_path_list = glob.glob(path)
	file_path_list.sort()
	return file_path_list

def reproject_GSWE(GSWE_file_list, target_crs = '+proj=utm +zone=30 +ellps=WGS84 +datum=WGS84 +units=m +no_defs '):
	"""Summary
	
	Args:
	    GSWE_file_list (TYPE): Description
	    target_crs (str, optional): Description
	"""
	try:
		os.makedirs("./Reprojected")
	except FileExistsError:
		# directory already exists
		pass

	## Reporject GSWE exports from WGS to target_crs
	for gsw in GSWE_file_list:
		head, tail = os.path.split(gsw)
		with rio.open(gsw) as src:
			transform, width, height = calculate_default_transform(
				'+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs', target_crs, src.width, src.height, *src.bounds)
			kwargs = src.meta.copy()
			kwargs.update({
				'crs': target_crs,
				'transform': transform,
				'width': width,
				'height': height,
				'compress': 'lzw'
			})
			with rio.open('./Reprojected/'+tail[0:-4]+'UTM.tif', 'w', **kwargs) as dst:
				reproject(
					source=rio.band(src, 1),
					destination=rio.band(dst, 1),
					src_transform=src.transform,
					src_crs=src.crs,
					dst_transform=transform,
					dst_crs=target_crs,
					resampling=Resampling.nearest)



def groupcounter(arr):
	"""Counts total of every unique value"""
	return np.stack(np.unique(arr, return_counts=True), axis=1)

def getFeatures(gdf):
	"""Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
	import json
	return [json.loads(gdf.to_json())['features'][0]['geometry']]

def pixel_size(raster):
	raster_affine = raster.transform
	pixel_size_x = raster_affine[0]
	pixel_size_y = -raster_affine[4]
	return pixel_size_x*pixel_size_y

def counts_in_hydrobasin(hydrobasin, raster):
	"""Counts pixels of every water type in a hydrobasin"""
	water_type_counts = []

	for polygon in hydrobasin['geometry']:
		polygon_gdf = gpd.GeoDataFrame({'geometry': polygon}, index=[0], crs='+proj=utm +zone=30 +datum=WGS84 +units=m +no_defs')
		coords = getFeatures(polygon_gdf)
		out_image, out_transform = mask(raster, coords, crop=True)
		stats = groupcounter(out_image)
		st_dict = dict(stats)
		water_type_counts.append(tuple(st_dict[q] if q in st_dict.keys() else 0 for q in range(1,4)))

	return pd.DataFrame(water_type_counts)


def surface_water_extent(GSWE_file_list, hydrobasin_gdf):
	"""Function to iterate through each GSWE output calculate water extent by type for each HydroBASIN"""

	extent_water_type = []

	for GSWE_file in GSWE_file_list:
		head, tail = os.path.split(GSWE_file)
		year = tail.split('UTM.')[0]
		print(year)

		with rio.open(GSWE_file) as raster:
			pixel_area = pixel_size(raster)

			for i in range(len(hydrobasin_gdf['HYBAS_ID'])):
				try:
					## For hydroBASINs that are multipolygons - split multipolygons into individual polygons
					hydrobasin_polygon = gpd.GeoDataFrame({'geometry': hydrobasin_gdf['geometry'][i]}, crs = ('+proj=utm +zone=30 +datum=WGS84 +units=m +no_defs'))

				except:
					## For hydroBASINs that are single polygons  
					hydrobasin_polygon = hydrobasin_gdf.iloc[i:i+1]


				water_type_counts = counts_in_hydrobasin(hydrobasin_polygon, raster)

				hydrobasin_extent = [hydrobasin_gdf['HYBAS_ID'][i]] + [year] + list(water_type_counts.sum()*pixel_area/1e6)
				extent_water_type.append(hydrobasin_extent)

	return pd.DataFrame(extent_water_type, columns= ['HYBAS_ID','Year', 'Ephemeral', 'Seasonal', 'Permanent'])


def filter_years(df, from_year, to_year, basin_id, water_type):
    filtered = df[(df['HYBAS_ID'] == str(basin_id)) & \
                  (df['Year'] >= from_year) & \
                  (df['Year'] <= to_year)][water_type]
    return filtered











