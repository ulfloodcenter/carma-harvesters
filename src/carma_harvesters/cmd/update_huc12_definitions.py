# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import os
import argparse
import tempfile
import shutil
import re
import logging
import sys
import traceback
from collections import OrderedDict

from tqdm import tqdm

from .. common import verify_raw_data, DEFAULT_NLCD_YEAR, DEFAULT_CDL_YEAR, \
    verify_input, open_existing_carma_document, output_json
from .. util import Geometry
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land


HUC12_PATT = re.compile('^\s*([0-9]{12}),*\s*$')
NLCD_HIGHLY_DEVELOPED_DN = 24

logger = logging.getLogger(__name__)


def _read_huc12_id(huc_path: str) -> set:
    huc_ids = set()
    with open(huc_path) as f:
        for l in f:
            m = HUC12_PATT.match(l)
            if m:
                huc_ids.add(m.group(1))
    return huc_ids


def main():
    parser = argparse.ArgumentParser(description=('Update HUC12 definitions in CARMA format by adding additional '
                                                  'year of crop and landcover data.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watersheds '
                              'to be updated with additional year of crop and landcover data.'))
    parser.add_argument('-ly', '--landcover_year', required=False, type=int, default=DEFAULT_NLCD_YEAR,
                        help='Year of NLCD landcover data to use to derive developed area.')
    parser.add_argument('-cy', '--crop_year', required=False, type=int, default=DEFAULT_CDL_YEAR,
                        help='Year USDA Cropland Data Layer to use for crops data.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--debug', help='Debug mode: do not delete output if there is an exception',
                        action='store_true', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

    success, data_result = verify_raw_data(args.datapath,
                                           nlcd_year=args.landcover_year,
                                           cdl_year=args.crop_year)
    if not success:
        for e in data_result['errors']:
            print(e)
        sys.exit("Invalid source data, exiting. Try running 'download-data.sh'.")

    cdl_year, cdl_path = data_result['paths']['cdl']
    nlcd_year, nlcd_path = data_result['paths']['nlcd']

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    error = False

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
            sys.exit(f"No HUC12 watersheds defined in {abs_carma_inpath}")

        huc12s = document['HUC12Watersheds']
        progress_bar = tqdm(huc12s)
        for h12 in progress_bar:
            progress_bar.set_description(f"Updating {h12['id']}")

            # Wrap HUC12 geometry as a Geometry for zonal stats computation
            geom = Geometry(h12['geometry'])

            # Compute zonal stats for crop cover (if needed)
            crops = h12['crops']
            crop_years = {c['year'] for c in crops}
            if cdl_year not in crop_years:
                total_crop_area, crop_areas = calculate_geography_crop_area(geom, cdl_path, h12['area'])
                logger.debug(f"CDL total crop area: {total_crop_area}")
                logger.debug(f"CDL individual crop areas: {crop_areas}")
                crops.append(OrderedDict([
                    ('year', cdl_year),
                    ('cropArea', total_crop_area),
                    ('cropAreaDetail', crop_areas)
                ]))

            # Compute zonal stats for landcover (if needed)
            developed_area = h12['developedArea']
            developed_area_years = {d['year'] for d in developed_area}
            if nlcd_year not in developed_area_years:
                developed_nlcd_cells, total_nlcd_cells = get_percent_highly_developed_land(geom, nlcd_path)
                if total_nlcd_cells == 0:
                    developed_proportion = 0
                else:
                    developed_proportion = developed_nlcd_cells / total_nlcd_cells
                developed_area.append(OrderedDict([
                    ('year', nlcd_year),
                    ('area', h12['area'] * developed_proportion)
                ]))

        # Save updated CARMA document (always overwrite because we are updating)
        output_json(abs_carma_inpath, temp_out, document, overwrite=True)
    except Exception as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        else:
            shutil.rmtree(temp_out)
