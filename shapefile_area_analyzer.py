import geopandas as gpd

# Define the source CRS (default) and the target CRS (UTM Zone 42N)
default_crs = "EPSG:4326"  # WGS 84 (Lat/Long)
utm_42n_crs = "EPSG:32642"  # UTM Zone 42N (meters)

# Load the first shapefile (default CRS 4326)
shapefile1 = gpd.read_file(r"D:\1) Area Optimizations\2025\Bank_Al-Falah_TAY\1_shapefile\Bank-Al-Falah_Tando-Allahyar_deh_Boundary_sindh-board-of-revenue_Map.shp")

# Load the second shapefile (default CRS 4326)
shapefile2 = gpd.read_file(r"D:\1) Area Optimizations\2025\Bank_Al-Falah_TAY\1_shapefile\Bank-Al-Falah_Tando-Allahyar_deh_Boundary_sindh-board-of-revenue_Map.shp")

# Ensure both shapefiles are in the same CRS (default 4326)
shapefile1 = shapefile1.set_crs(default_crs)
shapefile2 = shapefile2.set_crs(default_crs)

# Reproject both shapefiles to UTM Zone 42N
shapefile1 = shapefile1.to_crs(utm_42n_crs)
shapefile2 = shapefile2.to_crs(utm_42n_crs)

# Calculate the area in square meters
shapefile1['area_sqm'] = shapefile1.geometry.area
shapefile2['area_sqm'] = shapefile2.geometry.area

# Convert square meters to acres (1 acre = 4046.86 square meters)
shapefile1['area_acres'] = shapefile1['area_sqm'] / 4046.86
shapefile2['area_acres'] = shapefile2['area_sqm'] / 4046.86

# Calculate total area for each shapefile
total_area1_acres = shapefile1['area_acres'].sum()
total_area2_acres = shapefile2['area_acres'].sum()

# Function to calculate area summary for all categorical attributes
def calculate_area_summary(shapefile):
    summary = {}
    for column in shapefile.columns:
        if shapefile[column].dtype == 'object':  # Check if the column is categorical
            area_summary = shapefile.groupby(column)['area_acres'].sum()
            summary[column] = area_summary
    return summary

# Compute area summaries for both shapefiles
summary1 = calculate_area_summary(shapefile1)
summary2 = calculate_area_summary(shapefile2)

# Print the results
print("Total area breakdown for Shapefile 1:")
for column, values in summary1.items():
    print(f"\nSummary based on {column}:")
    for value, area in values.items():
        print(f"{value} = {area:.2f} acres")

print("\nTotal area breakdown for Shapefile 2:")
for column, values in summary2.items():
    print(f"\nSummary based on {column}:")
    for value, area in values.items():
        print(f"{value} = {area:.2f} acres")

# Compare the total areas
print("\nComparison of Total Areas:")
print(f"Total area of Shapefile 1: {total_area1_acres:.2f} acres")
print(f"Total area of Shapefile 2: {total_area2_acres:.2f} acres")

if total_area1_acres > total_area2_acres:
    print(f"Shapefile 1 is larger by {total_area1_acres - total_area2_acres:.2f} acres.")
elif total_area2_acres > total_area1_acres:
    print(f"Shapefile 2 is larger by {total_area2_acres - total_area1_acres:.2f} acres.")
else:
    print("Both shapefiles have the same total area.")
