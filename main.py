import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pystac_client
import planetary_computer
import stackstac
import xarray
import xrspatial
import rasterio
import rioxarray
import leafmap.foliumap as leafmap
import matplotlib.pyplot as plt
import os
import zipfile
import localtileserver
from rasterio.io import MemoryFile
from io import BytesIO
import pydeck as pdk
import tempfile
from streamlit_folium import st_folium
import folium

st.title('Geospatial Data Downloader')
st.text('This Application will help you download MSI, NDVI and EVI with one click for your Region of Interest')

st.divider()

st.text('Upload your Region of Interest as KML or Geopackage or GeoJSON')

uploaded_file = st.file_uploader('Upload your file', 
                 type = ['kml', 'gpkg', 'geojson'])

if not uploaded_file is None:
    
    filename = uploaded_file.name
    st.write(f'Succesfully uploaded file: {filename}')

    gdf = gpd.read_file(uploaded_file)

    gdf_4326 = gdf.to_crs('EPSG:4326')
    gdf_geom = gdf_4326.geometry.union_all().__geo_interface__

    #User input for date of interst
    st.text('Please select the Date Range for your Region of Interest')

    start_date = st.date_input('Select Start Date', value = None, key = 'Date_input')
    start_date_str = str(start_date)
    start_date_format = start_date_str.replace('/', '-')

    end_date = st.date_input('Select End Date', value = None, key = 'date')
    end_date_str = str(end_date)
    end_date_format = end_date_str.replace('/', '-')

    date = start_date_format + '/' + end_date_format

    st.write(f'Selected Date Range is: {start_date} to {end_date}')

    if start_date or end_date != 'None': 

        @st.cache_data
        def sentinel_extracter(geometry, datetime):

            catalog = pystac_client.Client.open(
                
                "https://planetarycomputer.microsoft.com/api/stac/v1",
                modifier = planetary_computer.sign_inplace

            )

            search = catalog.search(   
                collections = ['sentinel-2-l2a'],
                datetime = str(datetime),
                intersects = geometry,
                query = {'eo:cloud_cover': {'lt': 5}}
            )

            items = search.get_all_items()
            st.write(f'Found {len(items)} Sentinel images with less than 5% of Cloud Cover for {date}, for your ROI {filename}')

            ##Stacking items, clipping, scaling and composite creation
            bands = ['B02', 'B03', 'B04', 'B08', 'B8A', 'B11', 'B12']

            stacked = stackstac.stack(items, assets = bands, chunksize = 1024, 
                                    epsg = 4326)

            stacked_median = stacked.median(dim = 'time', keep_attrs = True)
            stacked_clipped = stacked_median.rio.clip(gdf_4326.geometry, gdf_4326.crs)
            stacked_scaled = stacked_clipped * 0.0001

            return stacked_scaled

        stacked_scaled = sentinel_extracter(geometry = gdf_geom, datetime = date)

        selector = st.selectbox('Choose an Index', 
                    options = ['NDVI', 'EVI'], 
                    placeholder = 'Select an Index', 
                    index = None 
                    )
        
        if selector != 'None': 

            indices_name = selector.lower()

            @st.cache_data
            def indices_calculator(indices_name):
                blue = stacked_scaled.sel(band = 'B02')
                red = stacked_scaled.sel(band = 'B04')
                nir = stacked_scaled.sel(band = 'B08')

                #NDVI Calculation
                ndvi = (nir - red) / (nir + red)

                #EVI Calculation
                evi = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)

                if indices_name == 'evi':
                    return evi
                else:
                    return ndvi

            indices = indices_calculator(indices_name)

            import leafmap.foliumap as leafmap

            from matplotlib.colors import ListedColormap

            indices_cmap = ListedColormap(['blue', 'yellow', 'green'])

            map = leafmap.Map()
            map.add_basemap('HYBRID')
            map.add_gdf(gdf_4326, layer_name = filename, 
                        edgecolor = 'black', fillcolor = None )
            map.add_raster(stacked_scaled, indexes = [3, 2, 1], 
                           layer_name = 'True Color Composite', nodata = np.nan)
            map.add_raster(indices, colormap = indices_cmap, nodata = np.nan, 
                           layer_name = indices_name)

            map.to_streamlit()   

            ##Download Button

            memfile = MemoryFile()
            with memfile.open(

                driver = 'GTiff',
                width = indices.shape[1],
                height = indices.shape[0],
                count = 1,
                crs = indices.rio.crs,
                transform = indices.rio.transform(),
                nodata = np.nan,
                dtype = indices.dtype,
            ) as dataset:
                dataset.write(indices.values, 1)

            tiff_bytes = memfile.read()

            st.download_button(

                    label = 'Download Indices',
                    data = tiff_bytes,
                    file_name = f'{filename}_{indices_name}.tif',
                    mime = 'image/tiff'
                )


            memfile2 = MemoryFile()
            with memfile2.open(

                driver = 'GTiff',
                width = stacked_scaled.shape[2],
                height = stacked_scaled.shape[1],
                count = stacked_scaled.shape[0],
                crs = stacked_scaled.rio.crs,
                transform = stacked_scaled.rio.transform(),
                nodata = np.nan,
                dtype = stacked_scaled.dtype,
            ) as dataset2:
                dataset2.write(stacked_scaled.values.squeeze())

            tiff_bytes2 = memfile2.read()

            st.download_button(

                        label = 'Download Sentinel 10m MSI',
                        data = tiff_bytes2,
                        file_name = f'{filename}_MSI.tif',
                        mime = 'image/tiff'
                    )
        else:
            st.stop()
    else:
        st.stop()
    
else:

    st.stop()

