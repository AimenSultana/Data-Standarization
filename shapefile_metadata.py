import os
import geopandas as gpd
import pandas as pd

# Define input folder containing shapefiles
input_folder = r"D:\1) Area Optimizations\2025\Bank_Al-Falah_TAY\1_shapefile"  # Change this to your folder path

# List to store shapefile column info
shapefile_data = []

# Process all shapefiles in the folder
for file in os.listdir(input_folder):
    if file.endswith(".shp"):
        file_path = os.path.join(input_folder, file)
        
        # Read the shapefile
        try:
            gdf = gpd.read_file(file_path)
            
            # Store column names and data types
            for col in gdf.columns:
                shapefile_data.append([file, col, str(gdf[col].dtype)])

            print(f"Processed: {file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

# Convert to Pandas DataFrame for a table-like format
df = pd.DataFrame(shapefile_data, columns=["Shapefile", "Column Name", "Data Type"])

# Print the formatted table
print("/nSummary of Shapefile Columns:/n")
print(df.to_string(index=False))

