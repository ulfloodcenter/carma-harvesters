import os
import logging

DATA_BASENAMES = {'wbd': 'NHDPlusNationalData/WBDSnapshot_National.shp',
                  'flowline': 'NHDFlowline_Network.sqlite',
                  'counties': 'TIGER_2013_2017_counties.sqlite',
                  'nlcd': 'NLCD_2016_Land_Cover_L48_20190424-WGS84.tif',
                  'cdl': '2019_30m_cdls.tif'}

logger = logging.getLogger(__name__)


def verify_raw_data(data_path: str) -> (bool, dict):
    errors = []
    data_ok = True

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
    nlcd_path = os.path.join(data_path, DATA_BASENAMES['nlcd'])
    if not os.path.exists(nlcd_path):
        data_ok = False
        errors.append(f"NLCD dataset {nlcd_path} does not exist.")
    elif not os.access(nlcd_path, os.R_OK):
        data_ok = False
        errors.append(f"NLCD dataset {nlcd_path} is not readable.")

    # Verify CropScape Cropland Data Layer (CDL) dataset
    cdl_path = os.path.join(data_path, DATA_BASENAMES['cdl'])
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

    paths = {'wbd': wbd_path,
             'flowline': flowline_path,
             'counties': counties_path,
             'nlcd': nlcd_path,
             'cdl': cdl_path}

    return data_ok, {'errors': errors, 'paths': paths}


def verify_outpath(out_path: str, out_name: str, overwrite=False) -> (bool, dict):
    errors = []
    success = True

    if not os.path.exists(out_path) or not os.path.isdir(out_path) or not os.access(out_path, os.W_OK):
        success = False
        errors.append(f"Output path {out_path} must be an existing writable directory, but is not.")

    out_file_path = os.path.join(out_path, out_name)
    if not overwrite and os.path.exists(out_file_path):
        success = False
        errors.append(f"Output file {out_file_path} exists.")

    paths = {'out_file_path': out_file_path}

    return success, {'errors': errors, 'paths': paths}


def verify_input(input_path: str) -> (bool, dict):
    errors = []
    success = True

    if not os.path.exists(input_path) or not os.path.isfile(input_path) or not os.access(input_path, os.R_OK):
        success = False
        errors.append(f"Input file {input_path} must be an existing readable file, but is not.")

    return success, {'errors': errors}