import os
import zipfile

# Define the folder containing shapefiles
input_folder = r"D:\2) Pakistan Shapefile + Thailand Shapefile\1_Deh Boundaries"  # Change this to your folder path
output_folder = r"D:\2) Pakistan Shapefile + Thailand Shapefile\1_Deh Boundaries"  # Folder to save ZIP files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all shapefiles in the folder
for file in os.listdir(input_folder):
    if file.endswith(".shp"):
        shapefile_name = os.path.splitext(file)[0]  # Get shapefile name without extension
        zip_filename = os.path.join(output_folder, f"{shapefile_name}.zip")

        # Create a ZIP file
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Find all related shapefile components
            for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg"]:
                file_path = os.path.join(input_folder, shapefile_name + ext)
                if os.path.exists(file_path):  # Check if the file exists
                    zipf.write(file_path, os.path.basename(file_path))

        print(f"Zipped: {zip_filename}")

print("All shapefiles have been zipped successfully!")
