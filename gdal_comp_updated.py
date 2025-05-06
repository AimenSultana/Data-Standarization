from osgeo import gdal
import numpy as np
import glob
import os
import time   

def compression(input_image, output_image):
    print("compressing")
    input_dataset = gdal.Open(input_image)

    driver = gdal.GetDriverByName("GTiff")

    output_dataset = driver.CreateCopy(output_image, input_dataset, options=[
        "COMPRESS=LZW",
        "PREDICTOR=2",
        "TILED=YES"
    ])

    input_dataset = None
    output_dataset = None

def rescale(input_path, output_path, brightness_factor):
    print("rescaling")
    input_ds = gdal.Open(input_path)

    if input_ds is None:
        print("Failed to open the input file.")
        return

    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output_path, input_ds.RasterXSize, input_ds.RasterYSize, input_ds.RasterCount, gdal.GDT_Byte, options=['COMPRESS=LZW', 'PREDICTOR=2',"TILED=YES"])

    all_bands = [input_ds.GetRasterBand(i + 1).ReadAsArray() for i in range(input_ds.RasterCount)]
    stacked_bands = np.stack(all_bands, axis=-1)

    input_min = np.nanmin(stacked_bands)
    input_max = np.nanmax(stacked_bands)

    for i in range(input_ds.RasterCount):
        input_band = input_ds.GetRasterBand(i + 1)
        output_band = output_ds.GetRasterBand(i + 1)

        input_array = input_band.ReadAsArray()

        scaled_array = (((input_array - input_min) / (input_max - input_min)) * 255.0) * brightness_factor
        scaled_array = np.clip(scaled_array, 0, 255).astype('uint8')
        

        output_band.WriteArray(scaled_array)
        output_band.SetNoDataValue(0)
        output_band.SetMetadata(input_band.GetMetadata())

    output_ds.SetProjection(input_ds.GetProjection())
    output_ds.SetGeoTransform(input_ds.GetGeoTransform())

    input_ds = None
    output_ds = None


def mosaicing(img_folder, output_raster):
    print("mosaicing")
    tif_files = glob.glob(os.path.join(img_folder, '*.tif'))
    NODATA_VALUE = 0
    g = gdal.Warp(output_raster, tif_files, format="GTiff", dstSRS="EPSG:3857",
                options=["COMPRESS=LZW", "TILED=YES"], srcNodata = NODATA_VALUE,
                        dstNodata = NODATA_VALUE)
    g = None

def extract_bands(input_folder, output_folder, bands):
    mosaic = False
    tif_files = glob.glob(os.path.join(input_folder, '*.tif'))

    if len(tif_files) > 1:
        mosaic = True

    for tif_file in tif_files:
        print(f"processing {tif_file}")
        input_ds = gdal.Open(tif_file)
        geotransform = input_ds.GetGeoTransform()
        projection = input_ds.GetProjectionRef()
        array_list = []
        for i in bands:
            input_ds.GetRasterBand(i).SetNoDataValue(0)
            array_list.append(input_ds.GetRasterBand(i).ReadAsArray())

        stacked_array = np.stack(array_list, axis=0)
        array_list = None

        driver = gdal.GetDriverByName('GTiff')
        n, rows, cols = stacked_array.shape
        output_file = os.path.join(output_folder, os.path.basename(tif_file))
        dataset = driver.Create(output_file, cols, rows, n,
                                        gdal.GDT_UInt16)
        dataset.SetGeoTransform(geotransform)
        dataset.SetProjection(projection)
        for b in range(1,n+1):
            
            band = dataset.GetRasterBand(b) 
            band.WriteArray(stacked_array[b-1]) 

        dataset = None
        stacked_array = None

    return mosaic

t1 = int(time.time())
#imagery folder
input_path = r"D:\Data\Mirpurkhas\1_raster_images\skywatch\raw"
#output folder
extracted_folder = r"D:\Data\Mirpurkhas\1_raster_images\skywatch\raw\4.0"
#rgb bands
bands = [6, 4, 2]
#brightness factor for final imagery
brightness_factor = 4.0

mosaic = extract_bands(input_path, extracted_folder, bands)

# if mosaic:
mosaiced_image = os.path.join(extracted_folder, 'mosaiced.tif')
mosaicing(extracted_folder, mosaiced_image)

rescaled_image = os.path.join(extracted_folder, 'rescaled.tif')
rescale(mosaiced_image, rescaled_image, brightness_factor)

compressed_image = os.path.join(extracted_folder, 'compressed_4.0.tif')
compression(rescaled_image, compressed_image)
t2 = int(time.time())

print('Time taken: ', t2-t1, ' seconds')