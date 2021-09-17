# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import sqlite3
import json
import logging


logger = logging.getLogger(__name__)


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


def get_huc12_min_stream_level(huc12_flowline_db: str):
    flowline_conn = sqlite3.connect(huc12_flowline_db)
    flowline = flowline_conn.cursor()

    query = 'select min(streamleve) from nhdflowline_network'
    flowline.execute(query)
    r = flowline.fetchone()
    if r is None:
        return None
    return r[0]


def get_geography_stream_characteristics(geometry: dict, flowline_db: str,
                                         huc_geometry_str: str=None) -> (float, float, float):
    """
    Query NHD flowlines that intersect a geometry, returning the following attributes:
    max(stream order), min(stream level), and max(mean annual streamflow).
    :param geometry: A Python object that represents a GeoJSON geometry
    :param flowline_db: File path to NHDFlowline Spatialite database
    :param huc_geometry_str: A string that represents a GeoJSON HUC12 geometry
    :return: Tuple consisting of: max(stream order), min(stream level), and max(mean annual streamflow)
    """
    max_stream_order = 0.0
    min_stream_level = 0.0
    max_mean_ann_flow = 0.0

    conn = sqlite3.connect(flowline_db)
    # Enable Spatialite extension (so that we can do spatial queries)
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite")')
    conn.enable_load_extension(False)
    cur = conn.cursor()

    # Query NHD Flowlines that intersect with the county geometry
    geometry_str = json.dumps(geometry)
    cur.execute(
        "select max(streamorde), min(streamleve), max(qe_ma) from nhdflowline_network where ST_Intersects(GeomFromGeoJSON(?), shape)",
        (geometry_str,))
    record = cur.fetchone()
    if record[0]:
        max_stream_order, min_stream_level, max_mean_ann_flow = record
    elif huc_geometry_str:
        logger.debug("No stream flowline found in sub-HUC12 boundary, looking for nearest flowline in the HUC12...")
        # No stream was found in sub-HUC12 polygon.
        # Use stream stats from flowline inside of HUC12 nearest to the sub-HUC12 polygon.
        # Define view of flowlines in the HUC12 boundary (can't use parameters with views so we are doing unsafe things)
        cur.execute(f"create temporary view huc12flow as select * from nhdflowline_network where ST_Intersects(GeomFromGeoJSON('{huc_geometry_str}'), shape)")
        # Select the flowline in the HUC12 boundary nearest to the sub-HUC12 boundary
        cur.execute(
            "select streamorde, streamleve, qe_ma, min(st_distance(shape, GeomFromGeoJSON(?))) from huc12flow",
            (geometry_str,))
        record = cur.fetchone()
        if record[0]:
            max_stream_order, min_stream_level, max_mean_ann_flow, _ = record
        else:
            logger.warning("No stream flowline found in or near sub-HUC12 boundary. This should never happen.")

    return max_stream_order, min_stream_level, max_mean_ann_flow


def get_huc12_stream_characteristics(huc_geometry: dict, flowline_db: str) -> (float, float, float):
    """
    Query NHD flowlines that intersect a HUC12 geometry, returning the following attributes:
    max(stream order), min(stream level), and max(mean annual streamflow).
    :param geometry: A Python object that represents a GeoJSON geometry
    :param flowline_db: File path to NHDFlowline Spatialite database
    :return: Tuple consisting of: max(stream order), min(stream level), and max(mean annual streamflow)
    """
    max_stream_order = None
    min_stream_level = None
    max_mean_ann_flow = None

    conn = sqlite3.connect(flowline_db)
    # Enable Spatialite extension (so that we can do spatial queries)
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite")')
    conn.enable_load_extension(False)
    cur = conn.cursor()

    # Query NHD Flowlines that intersect with the county geometry
    geometry_str = json.dumps(huc_geometry)
    cur.execute(
        "select max(streamorde), min(streamleve), max(qe_ma) from nhdflowline_network where ST_Intersects(GeomFromGeoJSON(?), shape)",
        (geometry_str,))
    record = cur.fetchone()
    if record[0]:
        max_stream_order, min_stream_level, max_mean_ann_flow = record
    else:
        logger.warning("No stream flowline found in or near HUC12 boundary.")

    return max_stream_order, min_stream_level, max_mean_ann_flow
