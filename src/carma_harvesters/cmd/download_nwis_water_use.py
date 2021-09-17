# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil

from carma_schema.geoconnex.census import County
from carma_schema import get_county_ids

from .. exception import SchemaValidationException
from .. common import verify_input, open_existing_carma_document, write_objects_to_existing_carma_document
from .. usgs.nwis_water_use import download_water_use_data, read_water_use_data, water_use_df_to_carma


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Download USGS NWIS water use data from '
                                                  'https://waterdata.usgs.gov/nwis/wu. Data are downloaded for '
                                                  'the counties defined in the specified CARMA data file in CARMA '
                                                  'schema format. Note: existing water use data for the specified year '
                                                  'will be overwritten if present.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of counties '
                              'for which water use data should be downloaded. Resulting water '
                              'use data will be written to the the same file.'))
    parser.add_argument('-y', '--year', type=int, default=2015, help='Year for which water use data should be downloaded.')
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

    try:
        document = open_existing_carma_document(abs_carma_inpath)

        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        fq_county_ids = get_county_ids(document)
        short_county_ids = [County.parse_fq_id(fq_id) for fq_id in fq_county_ids]
        logger.debug(f"County IDs to query...")
        for c in short_county_ids:
            logger.debug(f"\t{str(short_county_ids)}")

        # Collate county IDs by state
        county_ids_by_state_fips = {}
        for id in short_county_ids:
            county_list = None
            if id.state_fips not in county_ids_by_state_fips:
                county_list = set()
                county_ids_by_state_fips[id.state_fips] = county_list
            else:
                county_list = county_ids_by_state_fips[id.state_fips]
            county_list.add(id.county_fips)

        # Download water use data from NWIS for each state (since each state has a different endpoint)
        logger.debug(f"Counties to query by state:")
        water_use_objects = []
        for k in county_ids_by_state_fips.keys():
            logger.debug(f"State FIPS: {k}")
            logger.debug(f"{county_ids_by_state_fips[k]}")
            logger.debug("Downloading data NWIS water use data...")
            outfile_for_counties, url = download_water_use_data(year=args.year,
                                                                state_fips=k,
                                                                county_fips=county_ids_by_state_fips[k],
                                                                out_path=temp_out)
            logger.debug(f"Output saved to {outfile_for_counties}")
            water_use_df = read_water_use_data(outfile_for_counties)
            water_use_df_to_carma(water_use_df, url, water_use_objects)
        logger.debug(f"Marshalled {len(water_use_objects)} water use data instances")

        # Save CARMA water use data
        write_objects_to_existing_carma_document(water_use_objects, 'WaterUseDatasets',
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
