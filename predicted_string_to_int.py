import os
import geopandas as gpd

# Define input folder containing shapefiles
input_folder = r"D:\Data_Migration_IQ_Dashboard\1_Corteva_Data"  # Change this to your folder path

# Process all shapefiles in the folder
for file in os.listdir(input_folder):
    if file.endswith(".shp"):
        file_path = os.path.join(input_folder, file)
        
        # Read the shapefile
        gdf = gpd.read_file(file_path)
        
        # Check if 'predicted' column exists and is of type string
        if 'predicted' in gdf.columns and gdf['predicted'].dtype == 'object':
            print(f"Processing '{file}': Converting 'predicted' column from string to integer.")

            # Convert 'predicted' column to integer (handling potential conversion errors)
            try:
                gdf['predicted'] = gdf['predicted'].astype(int)
            except ValueError:
                print(f"Warning: Unable to convert some values in '{file}'. Skipping this file.")
                continue  # Skip saving the file if conversion fails

            # Keep only the 'predicted' column and geometry
            gdf = gdf[['predicted', 'geometry']]

            # Save the modified shapefile (overwrite)
            gdf.to_file(file_path)
            print(f"Updated '{file}' successfully.")
        else:
            print(f"No 'predicted' column found or it's already numeric in '{file}'. Skipping.")

print("Processing complete!")
