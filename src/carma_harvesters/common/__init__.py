import os
import logging
import tempfile
import shutil
import pkg_resources

import simplejson as json

from carma_schema import validate

from .. exception import SchemaValidationException


DATA_BASENAMES = {'wbd': 'NHDPlusNationalData/WBDSnapshot_National.shp',
                  'flowline': 'NHDFlowline_Network.spatialite',
                  'counties': 'TIGER_2013_2017_counties.spatialite',
                  'nlcd': {
                      2016: 'NLCD_2016_Land_Cover_L48_20190424-WGS84.tif'
                    },
                  'cdl': {
                      2019: '2019_30m_cdls.tif'
                    },
                  'rech48grd': 'rech48grd.tif'
                  }
DEFAULT_NLCD_YEAR = 2016
DEFAULT_CDL_YEAR = 2019

CARMA_SCHEMA_RSRC_KEY = 'carma_schema'
CARMA_SCHEMA_REL_PATH = 'data/schema/CARMA-schema-20210204.json'


logger = logging.getLogger(__name__)


def verify_raw_data(data_path: str, year=None) -> (bool, dict):
    errors = []
    data_ok = True

    if year is None:
        nlcd_year = DEFAULT_NLCD_YEAR
        cdl_year = DEFAULT_CDL_YEAR
    else:
        nlcd_year = year
        cdl_year = year

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


def verify_input(input_path: str) -> (bool, dict):
    errors = []
    success = True

    if not os.path.exists(input_path) or not os.path.isfile(input_path) or not os.access(input_path, os.R_OK):
        success = False
        errors.append(f"Input file {input_path} must be an existing readable file, but is not.")

    return success, {'errors': errors}


def output_json(out_file_path: str, temp_out: str, new_data: dict, overwrite: bool = False) -> bool:
    success = True
    if overwrite:
        # Output new_data to a temporary file
        f = tempfile.NamedTemporaryFile(dir=temp_out, mode='w', delete=False)
        tmp_out_path = f.name
        try:
            json.dump(new_data, f, use_decimal=True)
        except TypeError as e:
            logger.error(f"Unable to output JSON data to temporary file {tmp_out_path} due to error: {e}")
            success = False
        finally:
            f.close()
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
            json.dump(existing_data, f, use_decimal=True)
        except TypeError as e:
            logger.error(f"Unable to output JSON data to temporary file {tmp_out_path} due to error: {e}")
            success = False
        finally:
            f.close()

        # Finally, overwrite existing file with updated file, delete temporary file
        shutil.copy(tmp_out_path, out_file_path)
        os.unlink(tmp_out_path)
    return success


def open_existing_carma_document(document_path: str) -> dict:
    schema_path = pkg_resources.resource_filename(CARMA_SCHEMA_RSRC_KEY, CARMA_SCHEMA_REL_PATH)
    logger.debug(f"Schema path: {schema_path}")

    valid, result = validate(schema_path, document_path)
    if not valid:
        raise SchemaValidationException((f"Validation of {document_path} against schema {schema_path} "
                                         "failed due to the following errors: "
                                         f"{result['errors']}"))

    logger.debug(f"Input {document_path} validated successfully against schema {schema_path}")
    return result['document']
