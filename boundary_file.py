### Purpose: Standardize raw shapefiles/geojson/kml boundary data into Validated, reprojected and 
# and sanitized GEOJSON format with consistent naming


### Import libraries ###
import os
import geopandas as gpd
from datetime import datetime
from pyproj import CRS
from shapely.geometry import shape, mapping, MultiPolygon, Polygon
from shapely.validation import make_valid
from tabulate import tabulate

#-----------------------------------------------------
# Configuration
#-----------------------------------------------------


# Raw file input folder
Raw_Data_Dir = r"D:\Test_Standard_script\1_boundary\raw"          
# Processed output folder
Processed_Dir =r"D:\Test_Standard_script\1_boundary\processed"

# This function stored processed file path for final summary
processed_files_summary = []

#----------------------------------------------
# Core Functions
#----------------------------------------------

def reproject_to_4326(gdf):
    """ Ensure all input GeoDataFrames are reprojected to EPSG:4326."""
    if gdf.crs is None:
        print("Warning: Input file has no CRS! Assuming EPSG:4326.")
        gdf.set_crs(epsg=4326, inplace=True)
    elif not gdf.crs.equals(CRS.from_epsg(4326)):
        print(f"Reprojecting from {gdf.crs} to EPSG:4326")
        gdf = gdf.to_crs(epsg=4326)
    return gdf

def sanitize_geometry(gdf):
    """
    1. Validate each geometry
    1. Drop Z-values
    2. Convert Polygons to Multipolygons
    3. Removes empty/invalid features
    """
    def process_geom(geom):
        if not geom or geom.is_empty:
            return None
        try:
            geom = make_valid(geom)             # Fix geometry issue
            geom_2d = shape(mapping(geom))      # Drop Z-values
            if geom_2d.geom_type == "Polygon":
                return MultiPolygon([geom_2d])
            elif geom_2d.geom_type == "MultiPolygon":
                return geom_2d
        except Exception as e:
            print(f"Geometry conversion failed: {e}")
            return None                        

    gdf['geometry'] = gdf['geometry'].apply(process_geom)
    original = len(gdf)
    gdf = gdf.dropna(subset=['geometry'])
    print(f"Retained {len(gdf)} of {original} features after geometry sanitization.")
    return gdf

def preview_file(input_path):
    """Print preview of attribute table (excluding geometry)."""
    try:
        gdf = gpd.read_file(input_path)
        print("\n---Previewing:", os.path.basename(input_path), "---")
        print("Columns and types:")
        print(gdf.dtypes)
        print("\n Sample rows:")
        print(tabulate(gdf.drop(columns = 'geometry', errors='ignore'),headers='keys', tablefmt='grid'))
    except Exception as e:
        print(f"Error previewing file: {e}")

def get_file_metadata():
    """Collect and validate naming info from user."""
    print("\n=== Enter File Naming Details ===")
    metadata = {
        "report_type" : input("Report Type (e.g., Crop_Scan): ").strip(),
        "crop" : input("Crop (e.g., Sugarcane): ").strip(),
        "resolution" : input("Resolution (10m/3m/3m-10m): ").strip(),
        "season" : input("Season (e.g., Fall-2024,2025): ").strip(),
        "client" : input("Client Name: ").strip(),
        "extra_attr" : input("Extra Attributes (leave empty if none): ").strip()
    }

    # Date Validation with retry logic
    while True:
        date_input = input("Date (YYYY-MM-DD): ").strip()
        try:
            year, month, day = date_input.split('-')
            if (len(year) == 4 and year.isdigit() and
                len(month) == 2 and month.isdigit() and 1 <= int(month) <=12 and
                len(day) == 2 and day.isdigit() and 1 <= int(day) <= 31):
                metadata.update({
                    "year" : year,
                    "month" : month,
                    "day" : day
                })
                break
            raise ValueError
        except ValueError:
            print("Invalid data format. please use YYYY-MM-DD (e.g., 2024-05-20)")
            
    # Dynamic boundary type configuration
    print("\n=== Boundary Type Selection ===")
    print("Options: aoi, district, tehsil, cluster, circle, custom... etc")
    boundary_type = input("Boundary type: ").strip().lower()
    metadata["boundary_suffix"] = f"_{boundary_type}_boundary"

    # Pilot boundary falg
    if input("Is this a pilot boundary? (y/n): ").lower() =='y':
        metadata["boundary_suffix"] += "-pilot"
    return metadata

def generate_output_name(metadata):
    """ Generate standardized filename with proper formatting."""
    parts = [
        metadata["report_type"],
        metadata["crop"],
        metadata["resolution"],
        metadata["season"],
        f"{metadata['year']}-{metadata['month']}-{metadata['day']}", #YYYY-MM-DD format
        metadata["client"]
    ]
    filename = "_".join(filter(None, parts)) + metadata["boundary_suffix"]
    if metadata["extra_attr"]:
        filename += f"_{metadata['extra_attr']}"
    return filename + ".geojson"

def process_boundary_file(input_path, metadata):
    """Complete file standardization for one boundary input. """
    try:
        gdf = gpd.read_file(input_path)             # Read file (Input Files format SHP, KML, Geojson, etc.)
        gdf = reproject_to_4326(gdf)                # Convert CRS
        
        # Assign name column before geometry cleaning
        print(f"Available columns: {list(gdf.columns)}")
        name_col = input("which column contains names? (Press Enter to use client name):").strip()
        
        if name_col and name_col in gdf.columns:
            gdf["name"] = gdf[name_col].astype(str)
        else:
            gdf["name"] = os.path.splitext(os.path.basename(input_path))[0]     #filename without extension  

        gdf = sanitize_geometry(gdf)                # Clean Geometries 
        if gdf.empty:
            print(" Skipping: No Valid geometries found after cleaning.")
            return False                         

        gdf = gdf[["name", "geometry"]]                             # keep only 'name' and 'geometry' columns in output shapefile
        output_name = generate_output_name(metadata)
        output_path = os.path.join(Processed_Dir, output_name)      # Save to Output as GeoJSON
        
        # Check and overwrite File
        if os.path.exists(output_path):
            print(f"File already exists: {output_name}")
            if input("Same Metadata? Overwrite? (y/n): ").lower() !='y':
                print("Skipping save.")
                return False

        gdf.to_file(output_path, driver='GeoJSON')


        processed_files_summary(output_path)
        geometry_info = f"{gdf.geometry.geom_type.iloc[0]} ({len(gdf)})"
        col_info = ", ".join([f"{col}: {gdf[col].dtype}" for col in gdf.columns if col != 'geometry'])
        processed_files_summary.append([output_name, str(gdf.crs), geometry_info, col_info])
        print(f"Success: {output_name}")
                          

    except Exception as e:
        print(f"Failed to process {os.path.basename(input_path)}: {str(e)}") 
        return False


#---------------------------------------------------------
# Main Workflow
#--------------------------------------------------------

def main():
    # Create output directory if missing
    os.makedirs(Processed_Dir, exist_ok=True)

    print("\n=== Scanning raw files ===")
    input_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(Raw_Data_Dir)
        for f in files
        if f.lower().endswith(('.shp', '.kml', '.geojson'))
    ]
        
        
    if not input_files:
        print("No Boundary files found!")
        return
    
    # Process each file
    for file_path in input_files:
        preview_file(file_path)
        if input("Process this file ?(y/n): ").strip().lower() !='y':
            print("Skipped.\n")
            continue
        metadata = get_file_metadata()
        process_boundary_file(file_path, metadata)

    print("\nProcessing Complete!")

    if processed_files_summary:
        print("\n\n--- Processed Files Summary ---")
        print(tabulate(
            processed_files_summary,
            headers = ["File Name", "CRS", "Geometry Info", "Columns (Name: Type)"],
            tablefmt = "grid",
            maxcolwidths = [30, 20, 25, 40],
            stralign = "left"
        ))

if __name__ == "__main__":
    main()

    



