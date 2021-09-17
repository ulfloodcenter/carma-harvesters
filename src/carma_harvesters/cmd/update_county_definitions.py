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
import json
from collections import OrderedDict

from tqdm import tqdm

from carma_schema.geoconnex.census import County

from .. common import verify_raw_data, DEFAULT_NLCD_YEAR, DEFAULT_CDL_YEAR, \
    verify_input, open_existing_carma_document, output_json
from .. util import Geometry
from .. census import query_population_for_counties, POPULATION_URL_TEMPLATES
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land


ST_PATT = re.compile('^\s*([0-9]{2}),*\s*$')
ST_CO_PATT = re.compile('^\s*([0-9]{5}),*\s*$')

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Update county definitions in CARMA format by adding additional '
                                                  'year of: population, crop, and landcover data.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watersheds '
                              'to be updated with additional year of crop and landcover data.'))
    parser.add_argument('-y', '--population_year', type=int, default=2015,
                        help='Year for which county population should be queried from US Census.')
    parser.add_argument('--census_api_key', required=True,
                        help='Census API key obtained from https://api.census.gov/data/key_signup.html')
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

    if args.population_year not in POPULATION_URL_TEMPLATES:
        sys.exit(f"Population year must be one of: {list(POPULATION_URL_TEMPLATES.keys())}")

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

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        counties = document['Counties']

        # First get list of county short IDs and query census for population
        fips = {'state_county': [County.get_short_id(c['id']) for c in counties]}
        pop_by_county = query_population_for_counties(args.census_api_key, args.population_year, fips)

        progress_bar = tqdm(counties)
        for county in progress_bar:
            progress_bar.set_description(f"Updating {county['id']}")
            short_id = County.get_short_id(county['id'])

            # Wrap HUC12 geometry as a Geometry for zonal stats computation
            geom = Geometry(county['geometry'])

            # Add new population data
            pops = county['population']
            pop_years = {p['year'] for p in pops}
            pop_for_county = pop_by_county[short_id]
            for p in pop_for_county:
                if p.year not in pop_years:
                    pops.append(OrderedDict([
                        ('year', p.year),
                        ('count', p.population)
                    ]))

            # Compute zonal stats for crop cover (if needed)
            crops = county['crops']
            crop_years = {c['year'] for c in crops}
            if cdl_year not in crop_years:
                total_crop_area, crop_areas = calculate_geography_crop_area(geom, cdl_path, county['area'])
                logger.debug(f"CDL total crop area: {total_crop_area}")
                logger.debug(f"CDL individual crop areas: {crop_areas}")
                crops.append(OrderedDict([
                    ('year', cdl_year),
                    ('cropArea', total_crop_area),
                    ('cropAreaDetail', crop_areas)
                ]))

            # Compute zonal stats for landcover (if needed)
            developed_area = county['developedArea']
            developed_area_years = {d['year'] for d in developed_area}
            if nlcd_year not in developed_area_years:
                developed_nlcd_cells, total_nlcd_cells = get_percent_highly_developed_land(geom, nlcd_path)
                developed_proportion = developed_nlcd_cells / total_nlcd_cells
                developed_area.append(OrderedDict([
                    ('year', nlcd_year),
                    ('area', county['area'] * developed_proportion)
                ]))

        # Save updated CARMA document (always overwrite because we are updating)
        output_json(abs_carma_inpath, temp_out, document, overwrite=True)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        else:
            shutil.rmtree(temp_out)
