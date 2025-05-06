import geopandas as gpd   # type: ignore
import time  # Import time module

def dissolve_shapefile(input_shapefile, output_shapefile, dissolve_field):  
    start_time = time.time()  # Start the timer

    # Load the shapefile  
    gdf = gpd.read_file(input_shapefile)  
    # Fix geometries before dissolving  
    gdf['geometry'] = gdf.geometry.buffer(0)  
    # Dissolve the shapefile based on the specified field  
    dissolved_gdf = gdf.dissolve(by=dissolve_field)  
    # Explode the dissolved geometries to keep disjoint features separate  
    exploded_gdf = dissolved_gdf.explode(index_parts=True)  # index_parts=True keeps the original index  
    # Reset index to have a clean dataframe  
    exploded_gdf = exploded_gdf.reset_index(drop=False)  
    
    # Keep only the 'predicted' column and 'geometry'  
    exploded_gdf = exploded_gdf[['predicted', 'geometry']]

    # Save the dissolved and exploded shapefile  
    exploded_gdf.to_file(output_shapefile)  

    end_time = time.time()  # End the timer
    duration = end_time - start_time  # Calculate the duration in seconds
    
    # Convert duration to hours, minutes, and seconds
    hours, rem = divmod(duration, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Shapefile successfully dissolved and saved as {output_shapefile}")
    print(f"Time taken: {int(hours):02}:{int(minutes):02}:{int(seconds):02} (hh:mm:ss)")

# Example usage  
input_shapefile = r"D:\Data_Migration_IQ_Dashboard\20_Transmara_Data\3_Model_file\Crop-Scan_Sugarcane_3m_2024_2024-09-12_Transmara_classification_1.shp"# Replace with your input shapefile path  
output_shapefile = r"D:\Data_Migration_IQ_Dashboard\20_Transmara_Data\3_Model_file\Dissolved\Crop-Scan_Sugarcane_3m_2024_2024-09-12_Transmara_classification_1_Dissolved.shp"  # Replace with the desired output path  
dissolve_field = 'predicted'  # Replace with the field you want to dissolve by  

dissolve_shapefile(input_shapefile, output_shapefile, dissolve_field)

