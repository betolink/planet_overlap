import geopandas as gpd
from shapely.geometry import shape
from typing import List, Dict


def create_gdf(features: List[Dict]) -> gpd.GeoDataFrame:
    """
    Convert Planet features into GeoDataFrame.
    """

    geometries = [shape(f["geometry"]) for f in features]
    properties = [f["properties"] for f in features]

    gdf = gpd.GeoDataFrame(properties, geometry=geometries)
    gdf.set_crs(epsg=4326, inplace=True)
    return gdf
