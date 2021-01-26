import argparse
import logging
import sys
import pkg_resources
import os
import tempfile
import traceback
import shutil

from carma_schema import validate, get_county_ids

from .. common import verify_input, output_json
from .. geoconnex.census import County
from .. usgs.nwis_water_use import download_water_use_data, read_water_use_data, water_use_df_to_carma


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Download USGS NWIS water use data from '
                                                  'https://waterdata.usgs.gov/nwis/wu. Data are downloaded for '
                                                  'the counties defined in the specified CARMA data file in CARMA '
                                                  'schema format. Note: existing water use data for the specified year '
                                                  'will be overwritten if present.'))
    parser.add_argument('-c', '--carma_inpath', help=('Path of CARMA file containing definitions of counties '
                                                      'for which water use data should be downloaded. Resulting water '
                                                      'use data will be written to the the same file.'))
    parser.add_argument('-y', '--year', type=int, default=2015, help='Year for which water use data should be downloaded.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
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

    schema_path = pkg_resources.resource_filename('carma_schema', 'data/schema/CARMA-schema-20200709.json')
    logger.debug(f"Schema path: {schema_path}")

    valid, result = validate(schema_path, abs_carma_inpath)
    if not valid:
        sys.exit((f"Validation of {abs_carma_inpath} against schema {schema_path} failed due to the following errors: "
                  f"{result['errors']}"))

    logger.debug(f"Input {abs_carma_inpath} validated successfully against schema {schema_path}")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = result['document']
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
        logger.debug(f"Starting writing WaterUseDatasets to {abs_carma_inpath}...")
        document['WaterUseDatasets'] = water_use_objects
        output_json(abs_carma_inpath, temp_out, document, overwrite=True)
        logger.debug(f"Finished writing WaterUseDatasets to {abs_carma_inpath}.")
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        #shutil.rmtree(temp_out)
        pass