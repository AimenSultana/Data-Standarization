import geopandas as gpd

# Load the main shapefile (the one you want to clip)
main_shapefile = gpd.read_file(r"D:\Data_Migration_IQ_Dashboard\22_Shahmurad_Data\1_Boundaries\Shahmurad_gates_optimize.shp")
# Load the clipping shapefile
clip_shapefile = gpd.read_file(r"D:\Data_Migration_IQ_Dashboard\22_Shahmurad_Data\1_Boundaries\Shahmurad .geojson")

# Perform the clip operation
clipped_shapefile = gpd.overlay(main_shapefile, clip_shapefile, how='intersection')

# Save the result to a new shapefile
clipped_shapefile.to_file(r"D:\Data_Migration_IQ_Dashboard\22_Shahmurad_Data\1_Boundaries\Shahmurad_gates_optimize_clip.shp")