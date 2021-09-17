# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import json
from collections import OrderedDict
from multiprocessing import Pool
from typing import List

from shapely.geometry import asShape

from .. exception import SchemaValidationException
from .. common import verify_raw_data, DEFAULT_NLCD_YEAR, DEFAULT_CDL_YEAR,\
    verify_input, open_existing_carma_document, write_objects_to_existing_carma_document
from .. nhd import get_geography_stream_characteristics
from .. util import Geometry, intersect_shapely_to_multipolygon
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land


logger = logging.getLogger(__name__)


def do_generate_subhuc12_definitions(data_result: dict, document: dict, huc: dict) -> List[dict]:
    sub_huc12s = []
    print(f"\tBegin processing HUC12 {huc['id']}.")
    huc_geom = Geometry(huc['geometry'])
    huc_shape = asShape(huc_geom)
    huc_geom_geojson = json.dumps(huc['geometry'])
    # Iterate over all counties, checking for an intersection
    for county in document['Counties']:
        county_geom = Geometry(county['geometry'])
        county_shape = asShape(county_geom)
        # HUC12 intersects with county, create sub HUC12 objects
        if huc_shape.intersects(county_shape):
            sub_huc_geom, area = intersect_shapely_to_multipolygon(huc_shape, county_shape)
            if not sub_huc_geom:
                logger.warning((f"Could not compute intersection of HUC12 {huc['id']} with county "
                                "{county['county']}, {county['state']} even though they appear to intersect. "
                                "Skipping..."))
                continue
            sub_huc = OrderedDict()
            sub_huc['huc12'] = huc['id']
            sub_huc['county'] = county['id']
            sub_huc['area'] = area
            sub_huc['crops'] = []
            sub_huc['developedArea'] = []
            sub_huc['maxStreamOrder'] = 1.0
            sub_huc['minStreamLevel'] = 0.0
            sub_huc['meanAnnualFlow'] = 0.0
            sub_huc['geometry'] = sub_huc_geom
            sub_huc12s.append(sub_huc)

            # Wrap sub-HUC12 geometry as a Geometry for zonal stats computation
            geom = Geometry(sub_huc_geom)

            # Compute zonal stats for crop cover
            cdl_year, cdl_path = data_result['paths']['cdl']
            total_crop_area, crop_areas = calculate_geography_crop_area(geom, cdl_path, sub_huc['area'])
            logger.debug(f"CDL total crop area: {total_crop_area}")
            logger.debug(f"CDL individual crop areas: {crop_areas}")
            sub_huc['crops'].append(OrderedDict([
                ('year', cdl_year),
                ('cropArea', total_crop_area),
                ('cropAreaDetail', crop_areas)
            ]))

            # Compute zonal stats for landcover
            nlcd_year, nlcd_path = data_result['paths']['nlcd']
            developed_nlcd_cells, total_nlcd_cells = get_percent_highly_developed_land(geom, nlcd_path)
            if total_nlcd_cells == 0:
                developed_proportion = 0.0
            else:
                developed_proportion = developed_nlcd_cells / total_nlcd_cells
            sub_huc['developedArea'].append(OrderedDict([
                ('year', nlcd_year),
                ('area', sub_huc['area'] * developed_proportion)
            ]))

            # Calculate stream order, stream level, mean annual flow
            logger.debug(
                f"Getting stream characteristics for sub-HUC12 {sub_huc['huc12']}:{sub_huc['county']}. This may take a while...")
            max_strm_ord, min_strm_lvl, max_mean_ann_flow = \
                get_geography_stream_characteristics(sub_huc['geometry'], data_result['paths']['flowline'],
                                                     huc_geom_geojson)
            logger.debug(
                f"Stream characteristics: max_strm_ord: {max_strm_ord}, min_strm_lvl: {min_strm_lvl}, max_mean_ann_flow: {max_mean_ann_flow}")
            if max_strm_ord:
                sub_huc['maxStreamOrder'] = max_strm_ord
            if min_strm_lvl:
                sub_huc['minStreamLevel'] = min_strm_lvl
            if max_mean_ann_flow:
                sub_huc['meanAnnualFlow'] = max_mean_ann_flow

    print(f"\tFinished processing HUC12 {huc['id']}.")
    return sub_huc12s


def main():
    parser = argparse.ArgumentParser(description=('Generate sub-HUC12 watersheds by intersecting HUC12 watershed '
                                                  'boundaries with county boundaries. A sub-HUC12 watershed is a '
                                                  'portion of a HUC12 that is entirely contained in a county. '
                                                  'If a HUC12 is entirely contained in a county, a single sub-HUC12 '
                                                  'watershed will be generated whose boundary corresponds to that of '
                                                  'the original HUC12 watershed.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watersheds '
                              'and county definitions. Resulting sub-HUC12 watersheds '
                              'will be written to the same file.'))
    parser.add_argument('-ly', '--landcover_year', required=False, type=int, default=DEFAULT_NLCD_YEAR,
                        help='Year of NLCD landcover data to use to derive developed area.')
    parser.add_argument('-cy', '--crop_year', required=False, type=int, default=DEFAULT_CDL_YEAR,
                        help='Year USDA Cropland Data Layer to use for crops data.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    success, data_result = verify_raw_data(args.datapath,
                                           nlcd_year=args.landcover_year,
                                           cdl_year=args.crop_year)
    if not success:
        for e in data_result['errors']:
            print(e)
        sys.exit("Invalid source data, exiting. Try running 'download-data.sh'.")

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
            sys.exit(f"No HUC12 watersheds defined in {abs_carma_inpath}")

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        # Build sub-HUC12 watersheds (i.e. parts of HUC12 watersheds that intersect a county)
        sub_huc12s = []

        # For each HUC12, determine which counties it intersects with
        num_huc12 = len(document['HUC12Watersheds'])
        results = []
        with Pool() as pool:
            for i, huc in enumerate(document['HUC12Watersheds']):
                print(f"Generating sub watersheds for HUC12 {i} of {num_huc12}")
                r = pool.apply_async(do_generate_subhuc12_definitions, (data_result, document, huc), callback=sub_huc12s.extend)
                results.append(r)
            for r in results:
                r.wait()

        # Save sub-HUC12 definitions
        write_objects_to_existing_carma_document(sub_huc12s, 'SubHUC12Watersheds',
                                                 document, abs_carma_inpath,
                                                 temp_out, args.overwrite)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)