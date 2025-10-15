Geospatial Data Downloader
A user-friendly Streamlit application to download MSI (Sentinel-2 MultiSpectral Instrument), NDVI, and LULC (Dynamic World) geospatial datasets for your custom region of interest. Upload a region as a KML, GeoPackage, or GeoJSON, set your desired query dates, select vegetation indices, visualize interactively, and export results with one click.

Features
Upload ROI as KML, GeoPackage, or GeoJSON

Automated download of Sentinel-2 imagery (MSI) for specified dates and clouds <5%

Compute and visualize NDVI & EVI indices with interactive maps

Download processed geotiff datasets for indices and composite bands

Interactive mapping with Leafmap (folium)

Installation
Clone the Repository:

text
git clone <repo_url>
cd <repo_folder>
Create and Activate a Virtual Environment:

text
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
Install Dependencies:

text
pip install -r requirements.txt
Key packages required:

streamlit

pandas

numpy

geopandas

pystac-client

planetary-computer

stackstac

xarray

xrspatial

rasterio

rioxarray

leafmap

matplotlib

localtileserver

Usage
Run the app:

text
streamlit run app.py
Upload your region of interest:

Supported formats: .kml, .gpkg, .geojson

Select a date range for your query.

Choose a vegetation index (NDVI or EVI).

Visualize:

Interactive mapping with base layers.

Display ROI, true color composite, and indices.

Download outputs:

GeoTIFF of NDVI/EVI indices.

GeoTIFF of stacked MSI bands.

Example Workflow
Upload your AOI as a GeoJSON.

Choose your date range (e.g., 2024-06-01 to 2024-06-15).

Select 'NDVI' or 'EVI'.

Explore your region and indices on the interactive map.

Download the processed raster for use in any GIS tool.

How It Works
Takes spatial input from user-uploaded file, reprojects to EPSG:4326.

Queries Microsoft Planetary Computer STAC API for Sentinel-2 imagery with <5% cloud cover in the time range.

Stacks, composites, and scales relevant bands for the region.

Calculates selected vegetation indices.

Visualizes on a Leafmap (folium) interactive map.

Downloads results as GeoTIFF (compatible with QGIS, ArcGIS, etc.).

File Outputs
Output	Format	Description
Vegetation Index	GeoTIFF	NDVI/EVI clipped to AOI
Sentinel-2 MSI Bands	GeoTIFF	Multiband 10m composite
Notes
Requires internet connection for API queries and data download.

Works best with clear, well-bounded AOIs.

All processing is done in memory for efficient downloads.

License
Distributed under the MIT License.

Contact
For issues, feature requests, or contributions:

[Add your email/contact info here]

[Link to Issues/Discussions]

Acknowledgements
Microsoft Planetary Computer

STAC API and stackstac

Leafmap and Streamlit community