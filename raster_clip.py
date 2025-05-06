import rasterio
from rasterio.mask import mask
import geopandas as gpd

def clip_raster(raster_path, mask_shapefile_path, output_path):
    """Clips a raster file using a vector mask layer.

    Args:
        raster_path (str): Path to the input raster file.
        mask_shapefile_path (str): Path to the vector mask shapefile.
        output_path (str): Path to save the clipped raster output.
    """

    # Read the mask shapefile
    mask_gdf = gpd.read_file(mask_shapefile_path)

    # Open the raster file and get geospatial metadata
    with rasterio.open(raster_path) as src:
        # Use mask() to clip the raster, get the result as an in-memory array and updated metadata 
        out_image, out_transform = mask(src, mask_gdf.geometry, crop=True, nodata=0)
        out_meta = src.meta.copy()

    # Update metadata with the new transform and shape
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    # Write the clipped raster to a new file
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_image)


# Example usage
raster_path = r"D:\test_del\fsml_2024-02-07.tif"
mask_shapefile_path = r"D:\test_del\fsml_sugarcane.shp"
output_path = r"D:\test_del\fsml_2024-02-07_sugarcane_clip.tif"

clip_raster(raster_path, mask_shapefile_path, output_path)