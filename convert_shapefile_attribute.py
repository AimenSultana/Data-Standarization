import os
import geopandas as gpd

# Define input folder containing shapefiles
input_folder = r"D:\Data_Migration_IQ_Dashboard\17_Omni_Data\7_annotation"  # Change this to your folder path

# Process all shapefiles in the folder
for file in os.listdir(input_folder):
    if file.endswith(".shp"):
        file_path = os.path.join(input_folder, file)
        
        # Read the shapefile
        gdf = gpd.read_file(file_path)
        
        # Find the first numeric column
        numeric_columns = gdf.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_columns:
            column_to_convert = numeric_columns[0]  # Select the first numeric column
            print(f"Processing '{file}': Using column '{column_to_convert}' as 'predicted'.")

            # Convert column to integer and rename it to 'predicted'
            gdf['predicted'] = gdf[column_to_convert].astype(int)

            # Keep only the 'predicted' column and geometry
            gdf = gdf[['predicted', 'geometry']]

            # Save the modified shapefile (overwrite)
            gdf.to_file(file_path)
            print(f"Updated '{file}' successfully.")
        else:
            print(f"No numeric column found in '{file}'. Skipping.")

print("Processing complete!")
