# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import os
import logging
import tempfile
import shutil
import pkg_resources
from typing import List, Callable, TextIO
import sqlite3

import simplejson as json

from shapely.geometry.base import BaseGeometry
from shapely.geometry import asShape
from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union

import pandas as pd

import carma_schema
from carma_schema import get_water_use_data_for_huc12

from .. util import Geometry
from .. exception import SchemaValidationException


DATA_BASENAMES = {'wbd': 'WBDSnapshot_National.spatialite',
                  'flowline': 'NHDFlowline_Network.spatialite',
                  'counties': 'TIGER_2013_2017_counties.spatialite',
                  'nlcd': {
                      2011: 'nlcd_2011_land_cover_l48_20210604-WGS84.tif',
                      2016: 'NLCD_2016_Land_Cover_L48_20190424-WGS84.tif'
                    },
                  'cdl': {
                      2010: '2010_30m_cdls.tif',
                      2015: '2015_30m_cdls.tif',
                      2020: '2020_30m_cdls.tif'
                    },
                  'rech48grd': 'rech48grd.tif'
                  }
DEFAULT_NLCD_YEAR = 2016
DEFAULT_CDL_YEAR = 2015

CARMA_SCHEMA_RSRC_KEY = 'carma_schema'
CARMA_SCHEMA_REL_PATH = 'data/schema/CARMA-schema-20210908.json'

JSON_DEFAULT_INDENT = ' '
JSON_DEFAULT_SEPARATORS = (',', ':')


logger = logging.getLogger(__name__)


def almost_equal(x: float, y: float, tolerance=0.0000001) -> bool:
    return abs(x - y) < tolerance


def spatialite_to_geojson(spatialite_path: str, table_name: str, geojson_path: str) -> bool:
    conn = sqlite3.connect(spatialite_path)
    # Enable Spatialite extension (so that we can do spatial queries)
    os.environ["SPATIALITE_SECURITY"] = "relaxed"
    conn.enable_load_extension(True)
    conn.execute('SELECT load_extension("mod_spatialite")')
    conn.enable_load_extension(False)
    cur = conn.cursor()

    cur.execute("SELECT ExportGeoJSON2(?, 'geometry', ?, 12)",
                (table_name, geojson_path))
    result = cur.fetchone()
    if result is None:
        return False
    return True


def verify_raw_data(data_path: str,
                    nlcd_year=DEFAULT_NLCD_YEAR,
                    cdl_year=DEFAULT_CDL_YEAR) -> (bool, dict):
    errors = []
    data_ok = True

    if nlcd_year not in DATA_BASENAMES['nlcd']:
        data_ok = False
        errors.append(f"No NLCD data for year {nlcd_year}.")
        return data_ok, {'errors': errors, 'paths': {}}

    if cdl_year not in DATA_BASENAMES['cdl']:
        data_ok = False
        errors.append(f"No CropScape Cropland Data Layer data for year {cdl_year}.")
        return data_ok, {'errors': errors, 'paths': {}}

    # Verify water boundary dataset
    wbd_path = os.path.join(data_path, DATA_BASENAMES['wbd'])
    if not os.path.exists(wbd_path):
        data_ok = False
        errors.append(f"WBD should exist at {wbd_path} but does not.")
    elif not os.access(wbd_path, os.R_OK):
        data_ok = False
        errors.append(f"WBD dataset {wbd_path} is not readable.")

    # Verify Flowline dataset
    flowline_path = os.path.join(data_path, DATA_BASENAMES['flowline'])
    if not os.path.exists(flowline_path):
        data_ok = False
        errors.append(f"NHD Flowline dataset {flowline_path} does not exist.")
    elif not os.access(flowline_path, os.R_OK):
        data_ok = False
        errors.append(f"NHD Flowline dataset {flowline_path} is not readable.")

    # Verify NLCD dataset
    nlcd_path = os.path.join(data_path, DATA_BASENAMES['nlcd'][nlcd_year])
    if not os.path.exists(nlcd_path):
        data_ok = False
        errors.append(f"NLCD dataset {nlcd_path} does not exist.")
    elif not os.access(nlcd_path, os.R_OK):
        data_ok = False
        errors.append(f"NLCD dataset {nlcd_path} is not readable.")

    # Verify CropScape Cropland Data Layer (CDL) dataset
    cdl_path = os.path.join(data_path, DATA_BASENAMES['cdl'][cdl_year])
    if not os.path.exists(cdl_path):
        data_ok = False
        errors.append(f"CropScape Cropland Data Layer dataset {cdl_path} does not exist.")
    elif not os.access(cdl_path, os.R_OK):
        data_ok = False
        errors.append(f"CropScape Cropland Data Layer dataset {cdl_path} is not readable.")

    # Verify National Map/TIGER counties dataset
    counties_path = os.path.join(data_path, DATA_BASENAMES['counties'])
    if not os.path.exists(counties_path):
        data_ok = False
        errors.append(f"Counties dataset {counties_path} does not exist.")
    elif not os.access(counties_path, os.R_OK):
        data_ok = False
        errors.append(f"Counties dataset {counties_path} is not readable.")

    # Verify USGS groundwater recharge dataset
    rech48grd_path = os.path.join(data_path, DATA_BASENAMES['rech48grd'])
    if not os.path.exists(rech48grd_path):
        data_ok = False
        errors.append(f"USGS groundwater recharge dataset {rech48grd_path} does not exist.")
    elif not os.access(rech48grd_path, os.R_OK):
        data_ok = False
        errors.append(f"USGS groundwater recharge dataset {counties_path} is not readable.")

    paths = {'wbd': wbd_path,
             'flowline': flowline_path,
             'counties': counties_path,
             'nlcd': (nlcd_year, nlcd_path),
             'cdl': (cdl_year, cdl_path),
             'recharge': rech48grd_path}

    return data_ok, {'errors': errors, 'paths': paths}


def verify_outpath(out_path: str, out_name: str, overwrite=False) -> (bool, dict):
    errors = []
    success = True

    if not os.path.exists(out_path) or not os.path.isdir(out_path) or not os.access(out_path, os.W_OK):
        success = False
        errors.append(f"Output path {out_path} must be an existing writable directory, but is not.")

    out_file_path = os.path.join(out_path, out_name)
    paths = {'out_file_path': out_file_path}

    return success, {'errors': errors, 'paths': paths}


def verify_output(out_name: str, overwrite=False) -> (bool, dict):
    errors = []
    success = True

    out_file_path = os.path.abspath(out_name)
    if not overwrite:
        if os.path.exists(out_file_path):
            success = False
            errors.append(f"Output file {out_file_path} already exists but overwrite is false.")

    paths = {'out_file_path': out_file_path}

    return success, {'errors': errors, 'paths': paths}


def verify_input(input_path: str) -> (bool, dict):
    errors = []
    success = True

    if not os.path.exists(input_path) or not os.path.isfile(input_path) or not os.access(input_path, os.R_OK):
        success = False
        errors.append(f"Input file {input_path} must be an existing readable file, but is not.")

    return success, {'errors': errors}


def _carma_schema_validate(tmp_out_path: str) -> bool:
    schema_path = pkg_resources.resource_filename(CARMA_SCHEMA_RSRC_KEY, CARMA_SCHEMA_REL_PATH)
    logger.debug(f"Schema path: {schema_path}")
    valid, result = carma_schema.validate(schema_path, tmp_out_path)
    if not valid:
        raise SchemaValidationException((f"Validation of {tmp_out_path} against schema {schema_path} "
                                         "failed due to the following errors: "
                                         f"{result['errors']}"))
    return True


def output_json(out_file_path: str, temp_out: str, new_data: dict, overwrite: bool = False,
                indent=JSON_DEFAULT_INDENT, separators=JSON_DEFAULT_SEPARATORS,
                validate: Callable[[str], bool]=_carma_schema_validate) -> bool:
    success = True
    if overwrite:
        # Output new_data to a temporary file
        f = tempfile.NamedTemporaryFile(dir=temp_out, mode='w', delete=False)
        tmp_out_path = f.name
        try:
            json.dump(new_data, f, indent=indent, separators=separators, use_decimal=True)
        except TypeError as e:
            logger.error(f"Unable to output JSON data to temporary file {tmp_out_path} due to error: {e}")
            success = False
        finally:
            f.close()
        if success:
            if validate:
                logger.debug(f"Validating temporary CARMA file {tmp_out_path} before attempting to overwrite file {out_file_path}.")
                success = validate(tmp_out_path)
            if success:
                # Overwrite previous file with new file
                shutil.copy(tmp_out_path, out_file_path)
                os.unlink(tmp_out_path)
    else:
        # Attempt to merge new_data with JSON already in file
        # First, read in existing file contents (which should be JSON)
        existing_data = {}
        try:
            with open(out_file_path, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            # File does not exist, but overwrite was specified. Ignore. The file will
            # be created below
            pass
        except json.JSONDecodeError:
            raise Exception(f"Expected file {out_file_path} to be valid JSON, but it is not.")

        # Second, combine new_data with existing data, overwriting extant keys
        existing_data.update(new_data)

        # Next, output combined output to temporary file
        f = tempfile.NamedTemporaryFile(dir=temp_out, mode='w', delete=False)
        tmp_out_path = f.name
        try:
            json.dump(existing_data, f, indent=indent, separators=separators, use_decimal=True)
        except TypeError as e:
            logger.error(f"Unable to output JSON data to temporary file {tmp_out_path} due to error: {e}")
            success = False
        finally:
            f.close()

        if validate:
            logger.debug(f"Validating temporary CARMA file {tmp_out_path} before attempting to overwrite file {out_file_path}.")
            success = validate(tmp_out_path)
        if success:
            # Finally, overwrite existing file with updated file, delete temporary file
            shutil.copy(tmp_out_path, out_file_path)
            os.unlink(tmp_out_path)
    return success


def open_existing_carma_document(document_path: str) -> dict:
    schema_path = pkg_resources.resource_filename(CARMA_SCHEMA_RSRC_KEY, CARMA_SCHEMA_REL_PATH)
    logger.debug(f"Schema path: {schema_path}")

    valid, result = carma_schema.validate(schema_path, document_path)
    if not valid:
        raise SchemaValidationException((f"Validation of {document_path} against schema {schema_path} "
                                         "failed due to the following errors: "
                                         f"{result['errors']}"))

    logger.debug(f"Input {document_path} validated successfully against schema {schema_path}")
    return result['document']


def add_to_existing_object(objects_to_add: List[dict], object_type: str,
                           object: dict, overwrite: bool = False):
    if object_type not in object or overwrite:
        object[object_type] = objects_to_add
    else:
        object[object_type].extend(objects_to_add)


def add_objects_to_existing_carma_document(objects: List[dict], object_type: str,
                                           document: dict, overwrite: bool = False):
    if object_type not in carma_schema.DEFINITION_TYPES and object_type not in carma_schema.DATASET_TYPES:
        raise ValueError(f"Object type {object_type} is not a known type in CARMA schema.")
    if object_type not in document or overwrite:
        document[object_type] = objects
    else:
        document[object_type].extend(objects)


def write_objects_to_existing_carma_document(objects: List[dict], object_type: str,
                                             document: dict, document_path: str,
                                             temp_out: str, overwrite: bool = False):
    logger.debug(f"Starting to write {object_type} to {document_path}...")
    add_objects_to_existing_carma_document(objects, object_type, document, overwrite)
    # We always pass overwrite=True in to output_json because we collated JSON data
    # above before outputting.
    output_json(document_path, temp_out, document, overwrite=True)
    logger.debug(f"Finished writing WaterUseDatasets to {document_path}.")


def get_geometries_for_entities_in_document(document: dict, entity_key: str) -> List[BaseGeometry]:
    geoms = []
    if entity_key in document:
        for e in document[entity_key]:
            geoms.append(asShape(Geometry(e['geometry'])))
    return geoms


def dissolve_geometries(geometries: List[dict]) -> Polygon:
    return unary_union(geometries)


def dissolve_huc12_geometries(document: dict) -> Polygon:
    return dissolve_geometries(get_geometries_for_entities_in_document(document, 'HUC12Watersheds'))


def geom_to_shapely(geom: dict) -> BaseGeometry:
    return asShape(Geometry(geom))


def shapely_to_geojson(geom: BaseGeometry, out_file: TextIO):
    json.dump(geom.__geo_interface__, out_file)
    out_file.close()


def get_huc12_wateruse_data(document: dict, huc12_id: str, year: int) -> pd.DataFrame:
    """
    Fetch water use data for this HUC12 and store in Pandas dataframe for analysis
    :param document:
    :param huc12_id:
    :param year:
    :return:
    """
    huc_wu = pd.DataFrame(columns=['water_source', 'water_type', 'sector', 'is_consumptive', 'value'])
    for wud in get_water_use_data_for_huc12(document, huc12_id, year):
        huc_wu = huc_wu.append({'water_source': wud['waterSource'],
                                'water_type': wud['waterType'],
                                'sector': wud['sector'],
                                'is_consumptive': 'consumptive' in wud['description'],
                                'value': wud['value']},
                               ignore_index=True)
    return huc_wu


def get_group_sum_value(group_sum: pd.DataFrame, query: str) -> float:
    if group_sum.empty:
        return 0.0
    sum_val = group_sum.query(query)
    if len(sum_val) >= 1:
        return float(sum_val.sum())
    else:
        return 0.0


def join_wateruse_data_to_huc12_geojson(document: dict, huc12_geojson: dict, year: int) -> dict:
    p = huc12_geojson['properties']
    huc_wu = get_huc12_wateruse_data(document, p['id'], year)

    grouped = huc_wu.groupby(['sector', 'is_consumptive', 'water_source', 'water_type'])
    group_sum = grouped.sum()
    # Surface water
    irrigation_surf_withdrawal = get_group_sum_value(group_sum,
                                                     'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source == "Surface Water"')
    p['irrigation_sw_mgd'] = irrigation_surf_withdrawal
    industrial_surf_withdrawal = get_group_sum_value(group_sum,
                                                     'is_consumptive == False and (sector == "Industrial" or sector == "Mining") and water_type != "Any" and water_source == "Surface Water"')
    p['industrial_sw_mgd'] = industrial_surf_withdrawal
    thermo_electric_surf_withdrawal = get_group_sum_value(group_sum,
                                                          'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source == "Surface Water"')
    p['power_generation_sw_mgd'] =  thermo_electric_surf_withdrawal
    public_supply_surf_withdrawal = get_group_sum_value(group_sum,
                                                        'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source == "Surface Water"')
    p['public_sector_sw_mgd'] = public_supply_surf_withdrawal
    p['total_sw_use_mgd'] = irrigation_surf_withdrawal + industrial_surf_withdrawal + \
                            thermo_electric_surf_withdrawal + public_supply_surf_withdrawal
    # Groundwater
    irrigation_gw_withdrawal = get_group_sum_value(group_sum,
                                                   'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source == "Groundwater"')
    p['irrigation_gw_mgd'] = irrigation_gw_withdrawal
    industrial_gw_withdrawal = get_group_sum_value(group_sum,
                                                   'is_consumptive == False and (sector == "Industrial" or sector == "Mining") and water_type != "Any" and water_source == "Groundwater"')
    p['industrial_gw_mgd'] = industrial_gw_withdrawal
    thermo_electric_gw_withdrawal = get_group_sum_value(group_sum,
                                                        'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source == "Groundwater"')
    p['power_generation_gw_mgd'] = thermo_electric_gw_withdrawal
    public_supply_gw_withdrawal = get_group_sum_value(group_sum,
                                                      'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source == "Groundwater"')
    p['public_supply_gw_mgd'] = public_supply_gw_withdrawal
    livestock_gw_withdrawal = get_group_sum_value(group_sum,
                                                  'is_consumptive == False and sector == "Livestock" and water_type != "Any" and water_source == "Groundwater"')
    p['livestock_gw_mgd'] = livestock_gw_withdrawal
    rural_domestic_gw_withdrawal = get_group_sum_value(group_sum,
                                                       'is_consumptive == False and sector == "Domestic" and water_type != "Any" and water_source == "Groundwater"')
    p['rural_domestic_gw_mgd'] = rural_domestic_gw_withdrawal
    p['total_gw_use_mgd'] = irrigation_gw_withdrawal + industrial_gw_withdrawal + \
                            thermo_electric_gw_withdrawal + public_supply_gw_withdrawal + \
                            livestock_gw_withdrawal + rural_domestic_gw_withdrawal
    p['total_use_withdrawal_mgd'] = p['total_sw_use_mgd'] + p['total_gw_use_mgd']

    return huc12_geojson
