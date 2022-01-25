#third party
import ee

# Set constants for Asset IDs
# Currently versions 1.3 are active and others deprecated.
# May change in future!
GSWE_MONTHLY = "JRC/GSW1_3/MonthlyHistory"
GSWE_YEARLY = "JRC/GSW1_3/YearlyHistory"

def baseline_image_mask():
    """Creates a reduced sum image of monthly observations during baseline years (2001-2005)
    
    Returns:
        ee.Image: Number of observations a pixel had over the baseline period
    """
    baseline_months_collection = ee.ImageCollection(GSWE_MONTHLY).filterDate('2001-01', '2006-01')
    baseline_months_sum = baseline_months_collection.reduce(ee.Reducer.sum())
    baselines_sum_img = ee.Image(baseline_months_sum)
    
    return baselines_sum_img


def extract_baseline_to_drive(data_asset, geometry, drive_folder, mask):
    """Extract the baseline image to Google Drive
    
    Args:
        data_asset (str): Asset ID of image collection
        geometry (ee.Geometry.Polygon): Bounding box of area of interest
        drive_folder (str): Googke Drive folder for exports
        mask (ee.Image): Earth Engine image used to mask
    
    Returns:
        GeoTIFF: Baseline image
    """
    baseline_years = ee.ImageCollection(data_asset).filterDate(str(2001), str(2006))
    baseline_mode = baseline_years.reduce(ee.Reducer.mode())
    
    img_masked = baseline_mode.updateMask(mask.gte(1)) ## Update layer using baseline mask - 0 = no observations    
    
    task_config = {
    'region': geometry.coordinates().getInfo(), 
    'scale': 30,
    'description': 'gswbaseline',
    'folder': drive_folder,
    'maxPixels':3932959350
    } 
    
    return ee.batch.Export.image.toDrive(img_masked, **task_config).start()


def extract_gswe_to_drive(data_asset, geometry, start, end, drive_folder, mask):
    """Extracts yearly GSWE images in area of interest to Google Drive
    
    Args:
        data_asset (str): Asset ID of image collection
        geometry (ee.Geometry.Polygon): Bounding box of area of interest
        start (int): start year
        end (int): end year
        Googke Drive folder for exports
        mask (ee.Image): Reduced image of monthly observations
    """
    gsw = ee.ImageCollection(data_asset).filterDate(str(start), str(end))
    img_count = gsw.size().getInfo()
    collectionList = gsw.toList(img_count)
    collectionSize = collectionList.size().getInfo()
    for i in range(img_count):
        img = ee.Image(collectionList.get(i))
        img_masked = img.updateMask(mask.gte(1)) ## Update layer using baseline mask: 0 == no observations
        img_masked = ee.Image(img_masked)
        ee.batch.Export.image.toDrive(
            image = img_masked.clip(geometry),
            folder = drive_folder,
            scale = 30,
            fileNamePrefix = 'gsw'+str(int(start)+i),
            maxPixels = 3932959350).start()
    
    
def extract_gswe(data_asset, geometry, start, end, drive_folder):
    """Extracts both baseline image and yearly GSWE images
    
    Args:
        data_asset (str): Asset ID of image collection
        geometry (ee.Geometry.Polygon): Bounding box of area of interest
        start (int): start year
        end (int): end year
        Googke Drive folder for exports
    
    Returns:
        str: Completion message
    """
    mask = baseline_image_mask()
    extract_baseline_to_drive(data_asset, geometry, drive_folder, mask)
    extract_gswe_to_drive(data_asset, geometry, start, end, drive_folder, mask)
    
    return print(f'GSWE files are being extracted to {drive_folder} in your Google Drive')