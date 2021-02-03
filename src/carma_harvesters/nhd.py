import sqlite3
import json


def get_huc12_mean_annual_flow(huc12_flowline_db: str):
    flowline_conn = sqlite3.connect(huc12_flowline_db)
    flowline = flowline_conn.cursor()

    query = 'select max(qe_ma) from nhdflowline_network'
    flowline.execute(query)
    r = flowline.fetchone()
    if r is None:
        return None
    return r[0]


def get_huc12_max_stream_order(huc12_flowline_db: str):
    flowline_conn = sqlite3.connect(huc12_flowline_db)
    flowline = flowline_conn.cursor()

    query = 'select max(streamorde) from nhdflowline_network'
    flowline.execute(query)
    r = flowline.fetchone()
    if r is None:
        return None
    return r[0]


def get_county_stream_characteristics(county_geometry: dict, flowline_db: str) -> (float, float, float):
    """
    Query NHD flowlines that intersect a county, returning the following attributes:
    max(stream order), min(stream level), and max(mean annual streamflow).
    :param county_geometry: A Python object that represents a GeoJSON geometry representing the county boundary
    :param flowline_db: File path to NHDFlowline Spatialite database
    :return: Tuple consisting of: max(stream order), min(stream level), and max(mean annual streamflow)
    """
    conn = sqlite3.connect(flowline_db)
    # Enable Spatialite extension (so that we can do spatial queries)
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite")')
    conn.enable_load_extension(False)
    cur = conn.cursor()

    # Query NHD Flowlines that intersect with the county geometry
    county_geometry_str = json.dumps(county_geometry)
    cur.execute(
        "select max(streamorde), min(streamleve), max(qe_ma) from nhdflowline_network where ST_Intersects(shape, GeomFromGeoJSON(?))",
        (county_geometry_str,))
    record = cur.fetchone()
    max_stream_order = 0.0
    min_stream_level = 0.0
    max_mean_ann_flow = 0.0
    if record:
        max_stream_order, min_stream_level, max_mean_ann_flow = record
    return max_stream_order, min_stream_level, max_mean_ann_flow
