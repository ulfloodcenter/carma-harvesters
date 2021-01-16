import argparse
import logging
import sys
import pkg_resources
import os

from carma_schema import validate, get_county_ids

from .. common import verify_input
from .. geoconnex.census import County


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

    document = result['document']
    fq_county_ids = get_county_ids(document)
    short_county_ids = [County.parse_fq_id(fq_id) for fq_id in fq_county_ids]
    logger.debug(f"County IDs to query {short_county_ids}")
