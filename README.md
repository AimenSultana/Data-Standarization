# Data Standardization Scripts

A collection of Python scripts designed to simplify geospatial data workflows, particularly for shapefiles and raster imagery. These tools help in compressing, transforming, comparing, and analyzing spatial datasets efficiently.

| File Name | Description | Input | Output | Dependencies | Author | Last Updated |
|-----------|-------------|--------|--------|--------------|--------|--------------|
| [`zip_shapefile.py`](compressed_raster.py) | Packages Shapefile components into individual ZIP archives | Folder with Shapefiles | ZIP archives per Shapefile | os, zipfile | Aimen | 2025-05-06 |
| [`shapefile_area_comparison.py`](shapefile_area_comparison.py) | Compares areas between two classification shapefiles | Two Shapefiles | Area comparison results | geopandas | Aimen | 2025-05-06 |
| [`shapefile_area_analyzer.py`](shapefile_area_analyzer.py) | Advanced shapefile area comparison with categorical breakdowns | Two Shapefiles | Area reports and comparisons | geopandas | Aimen | 2025-05-06 |
| [`shapefile_metadata.py`](shapefile_metadata.py) | Analyzes and reports shapefile metadata structure | Folder with Shapefiles | Column inventory table | geopandas, pandas | Aimen | 2025-05-06 |
| [`convert_shapefile_attribute.py`](convert_shapefile_attribute.py) | Standardizes shapefile attributes to predicted/geometry schema | Folder with Shapefiles | Modified Shapefiles | geopandas | Aimen | 2025-05-06 |
| [`convert_shapefile_predicted_datatype.py`](convert_shapefile_predicted_datatype.py) | Converts string 'predicted' columns to integers in shapefiles | Folder with Shapefiles | Standardized Shapefiles | geopandas | Aimen | 2025-05-06 |
| [`raster_clip.py`](raster_clip.py) | Clips rasters to vector boundaries | Raster + Shapefile | Clipped Raster | rasterio, geopandas | Aimen | 2025-05-06 |
| [`dissolve_shapefile.py`](dissolve_shapefile.py) | Dissolves features by attribute with topology repair | Shapefile | Dissolved Shapefile | geopandas | Zainab | 2025-05-06 |
| [`s3_bucket_summary.py`](s3_bucket_summary.py) | Summarizes S3 bucket/folder contents | S3 Credentionals and bucket/folder path | Detailed Summary Excel | geopandas | Aimen | 2025-05-06 |
| [`compressed_raster.py`](compressed_raster.py) | Rescales, compresses, mosaics, and extracts bands from raster imagery | `.tif` raster folder | Compressed RGB `.tif` mosaic | gdal, numpy, glob, os | Hiba Nasir | 2025-05-06 |
 [shapefile_clip.py](shapefile_clip.py) | Clips vector features to boundaries | Shapefile + Boundary | Clipped Shapefile | geopandas | Zainab | 2025-05-06 |

