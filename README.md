# Geospatial Data Downloader
A user-friendly Streamlit application to download MSI (Sentinel-2 MultiSpectral Instrument), NDVI, and EVI geospatial datasets for your custom region of interest. Upload a region as a KML, GeoPackage, or GeoJSON, set your desired query dates, select vegetation indices, visualize interactively, and export results with one click.

## Features
- Upload ROI as KML, GeoPackage, or GeoJSON
- Automated download of Sentinel-2 imagery (MSI) for specified dates and clouds <5%
- Compute and visualize NDVI & EVI indices with interactive maps
- Download processed geotiff datasets for indices and composite bands
- Interactive mapping with Leafmap (folium)


**Acknowledgements**
1. Microsoft Planetary Computer
2. STAC API and stackstac
3. Leafmap and Streamlit community
