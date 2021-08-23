import subprocess
import logging
import os

from shapely.geometry.base import BaseGeometry
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from shapely.geometry import mapping
from shapely.errors import TopologicalError

import geopandas as gpd
import pandas as pd

from pyproj import Geod


OGR_PREFIX = os.environ.get('OGR_PREFIX', '/usr')


logger = logging.getLogger(__name__)


class Geometry:
    """
    Wrap GeoJSON-like object so that it can be used in tools like Shapely, for example:
    ```
    from shapely.geometry import asShape
    s = asShape(Geometry(object))
    ```
    """
    def __init__(self, object):
        self.__geo_interface__ = object


def run_cmd(cmd: str, *args):
    cmd = [cmd]
    cmd.extend(args)
    cmd_str = ' '.join(cmd)
    logger.debug(f"Running {cmd_str}...")
    p = subprocess.Popen(cmd_str, shell=True)
    p.wait()
    logger.debug(f"Command {cmd_str} returned {p.returncode}")
    if p.returncode != 0:
        raise Exception(f"Command {cmd_str} failed with return code {p.returncode}")


def run_ogr2ogr(*args) -> int:
    return run_cmd(f"{OGR_PREFIX}/bin/ogr2ogr", *args)


def intersect_shapely_to_multipolygon(geom1: BaseGeometry, geom2: BaseGeometry) -> (dict, float):
    intersection = None
    area = 0.0
    try:
        isect = geom1.intersection(geom2)
        if isinstance(isect, Polygon):
            isect = MultiPolygon([isect])
        elif not isinstance(isect, MultiPolygon):
            raise ValueError(f"Intersection of geometries must be a polygon or multipolygon but is {type(isect)} instead.")

        # Calculate area in km2 using PROJ
        geod = Geod(ellps='WGS84')
        area = abs(geod.geometry_area_perimeter(isect)[0]) / (1000 * 1000)

        intersection = mapping(isect)
    except TopologicalError as e:
        logger.warning(f"Unable to intersect geometries due to error: {e}")

    return intersection, area


def select_points_contained_by_geometry(point_geom_path: str, geom: BaseGeometry) -> dict:
    pts = gpd.read_file(point_geom_path, bbox=geom.bounds)
    pts_clip = gpd.clip(pts, geom)
    return pts_clip.__geo_interface__


def select_csv_points_contained_by_geometry(csv_path: str, geom: BaseGeometry,
                                            delim:str = ',', encoding:str = 'utf-8',
                                            lon_col:str = 'longitude', lat_col:str = 'latitude',
                                            crs:str = 'EPSG:4326') -> dict:
    df = pd.read_csv(csv_path, sep=delim, encoding=encoding, low_memory=False)
    pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col], crs=crs))
    pts_clip = gpd.clip(pts, geom)
    return pts_clip.__geo_interface__
