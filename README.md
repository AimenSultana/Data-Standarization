# Geospatial Boundary & Prediction Processing  

This repository contains two Python scripts designed to help geospatial analysts standardize and process boundary shapefiles and model prediction outputs with clean geometry, consistent formats, and a user-friendly workflow.

---

## 📁 Scripts Included

### 1. `boundary_file.py`
A streamlined tool to:
- Sanitize raw boundary files (Shapefile, KML, GeoJSON)
- Reproject to EPSG:4326
- Assign and clean geometry (Polygon → MultiPolygon, drop Z-values)
- Collect metadata from user inputs
- Generate standardized filenames
- Output as clean `.geojson` files
- Preview summary of results after each file is processed

---

### 2. `model_prediction_refined_file.py`
A refined processor for classification prediction outputs:
- Works with shapefiles containing a `predicted` column (or lets you assign it)
- Reprojects to EPSG:4326
- Cleans geometry (validates and converts to MultiPolygon)
- Collects metadata for consistent naming (e.g., crop type, resolution, scan date, client)
- Automatically zips the output shapefile
- Provides a summary table of all processed files at the end



