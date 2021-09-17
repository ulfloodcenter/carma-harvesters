# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
from functools import partial

from tqdm import tqdm

from shapely.geometry import asShape

from carma_harvesters.common import open_existing_carma_document, verify_input, add_to_existing_object, output_json
from carma_harvesters.util import Geometry, select_csv_points_contained_by_geometry
from carma_harvesters.wells import WellAttributeMapper
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


DEFAULT_DELIM = ','
DEFAULT_ENCODING = 'utf-8'
DEFAULT_LONG_COL = 'longitude'
DEFAULT_LAT_COL = 'latitude'
DEFAULT_CRS = 'EPSG:4326'


def main():
    parser = argparse.ArgumentParser(description=('Count groundwater wells that intersect Counties or '
                                                  'sub-HUC12 watersheds.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of sub-HUC12 watersheds '
                              'and counties. Resulting groundwater well counts '
                              'will be written to the same file.'))
    parser.add_argument('-w', '--well_data_path', required=True,
                        help=('CSV dataset containing well locations along with the following attributes: '
                              'sector, status, and year completed.'))
    parser.add_argument('--delimiter', type=str, default=DEFAULT_DELIM,
                        help=f"Record delimiter to use. Defaults to '{DEFAULT_DELIM}'.")
    parser.add_argument('--encoding', type=str, default=DEFAULT_ENCODING,
                        help=f"Character encoding of input CSV file. Defaults to '{DEFAULT_ENCODING}'.")
    parser.add_argument('--longitude', type=str, default=DEFAULT_LONG_COL,
                        help=f"Name of column to use for longitude values. Defaults to {DEFAULT_LONG_COL}.")
    parser.add_argument('--latitude', type=str, default=DEFAULT_LAT_COL,
                        help=f"Name of column to use for latitude values. Defaults to {DEFAULT_LAT_COL}.")
    parser.add_argument('--crs', type=str, default=DEFAULT_CRS,
                        help=('Coordinate reference system to use for longitude & latitude coordinates. '
                              f"Defaults to {DEFAULT_CRS}")
                        )
    parser.add_argument('-a', '--attribute_map_path', required=True,
                        help=('Path to JSON file mapping well attributes and values onto those defined in CARMA '
                              'schema.'))
    parser.add_argument('-y', '--year_completed', required=True, type=int,
                        help=('Include wells completed during or before this year in count of wells by sector '
                              'and status.'))
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    abs_well_inpath = os.path.abspath(args.well_data_path)
    success, input_result = verify_input(abs_well_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid well input data, exiting.")

    abs_attr_inpath = os.path.abspath(args.attribute_map_path)
    success, input_result = verify_input(abs_attr_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid well attribute input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'SubHUC12Watersheds' not in document or len(document['SubHUC12Watersheds']) < 1:
            sys.exit(f"No sub-HUC12 watersheds defined in {abs_carma_inpath}")

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        # Open well attribute map
        get_wells = partial(select_csv_points_contained_by_geometry,
                            delim=args.delimiter,
                            encoding=args.encoding,
                            lon_col=args.longitude,
                            lat_col=args.latitude,
                            crs=args.crs)
        mapper = WellAttributeMapper(abs_attr_inpath, abs_well_inpath,
                                     get_wells=get_wells)

        # Foreach county...
        progress_bar = tqdm(document['Counties'])
        for county in progress_bar:
            progress_bar.set_description(f"Summing wells in county {county['county']}")
            county_geom = Geometry(county['geometry'])
            county_shape = asShape(county_geom)
            county_wells = mapper.count_wells_in_geography(county_shape, args.year_completed)
            add_to_existing_object(county_wells, 'groundwaterWells',
                                   county, overwrite=args.overwrite)
        # Foreach sub-HUC12...
        progress_bar = tqdm(document['SubHUC12Watersheds'])
        for sub_huc12 in progress_bar:
            progress_bar.set_description(f"Summing wells in sub-HUC12 watersheds")
            sub_huc12_geom = Geometry(sub_huc12['geometry'])
            sub_huc12_shape = asShape(sub_huc12_geom)
            sub_huc12_wells = mapper.count_wells_in_geography(sub_huc12_shape, args.year_completed)
            add_to_existing_object(sub_huc12_wells, 'groundwaterWells',
                                   sub_huc12, overwrite=args.overwrite)
        # Write updated CARMA file
        output_json(abs_carma_inpath, temp_out, document, args.overwrite)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
