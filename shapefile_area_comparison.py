import geopandas as gpd

# Define the source CRS (default) and the target CRS (UTM Zone 42N)
default_crs = "EPSG:4326"  # WGS 84 (Lat/Long)
utm_42n_crs = "EPSG:32642"  # UTM Zone 42N (meters)

# Load the first shapefile (default CRS 4326)
shapefile1 = gpd.read_file(r"D:\5) Corteva Agriscience\9) Corteva Fall Maize Classification 2021\raw\corteva_fall_maize_sowing_2021_results_raw_week-wise_clip_aoi_dissolve_new-week_intersect.shp")

# Load the second shapefile (default CRS 4326)
shapefile2 = gpd.read_file(r"D:\5) Corteva Agriscience\9) Corteva Fall Maize Classification 2021\raw\corteva_fall_maize_sowing_2021_results_raw_week-wise_clip_aoi_dissolve_new-week_intersect.shp")

# Ensure both shapefiles are in the same CRS (default 4326)
shapefile1 = shapefile1.set_crs(default_crs)
shapefile2 = shapefile2.set_crs(default_crs)

# Reproject both shapefiles to UTM Zone 42N
shapefile1 = shapefile1.to_crs(utm_42n_crs)
shapefile2 = shapefile2.to_crs(utm_42n_crs)

# Calculate the area in square meters (since UTM coordinates are in meters)
shapefile1['area_sqm'] = shapefile1.geometry.area
shapefile2['area_sqm'] = shapefile2.geometry.area

# Convert square meters to acres (1 acre = 4046.86 square meters)
shapefile1['area_acres'] = shapefile1['area_sqm'] / 4046.86
shapefile2['area_acres'] = shapefile2['area_sqm'] / 4046.86

# Sum the total area of each shapefile
total_area1_acres = shapefile1['area_acres'].sum()
total_area2_acres = shapefile2['area_acres'].sum()

# Print the results
print(f"Total area of shapefile 1: {total_area1_acres:.2f} acres")
print(f"Total area of shapefile 2: {total_area2_acres:.2f} acres")

# Compare the areas
if total_area1_acres > total_area2_acres:
    print(f"Shapefile 1 is larger by {total_area1_acres - total_area2_acres:.2f} acres.")
elif total_area2_acres > total_area1_acres:
    print(f"Shapefile 2 is larger by {total_area2_acres - total_area1_acres:.2f} acres.")
else:
    print("Both shapefiles have the same area.")
