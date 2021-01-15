import argparse
import logging
import sys
import pkg_resources

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Download USGS NWIS water use data from '
                                                  'https://waterdata.usgs.gov/nwis/wu. Data are downloaded for '
                                                  'the counties defined in the specified CARMA data file in CARMA '
                                                  'schema format. Note: existing water use data for the specified year '
                                                  'will be overwritten if present.'))
    parser.add_argument('-c', '--carma_inpath', help=('Absolute path of CARMA file containing definitions of counties '
                                                      'for which water use data should be downloaded. Resulting water '
                                                      'use data will be written to the the same file.'))
    parser.add_argument('-y', '--year', type=int, default=2015, help='Year for which water use data should be downloaded.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    schema_path = pkg_resources.resource_string('carma_schema', 'data/schema/CARMA-schema-20200709.json')
    print(f"TEST Schema: {schema_path}")
