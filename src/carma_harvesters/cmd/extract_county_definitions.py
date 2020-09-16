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

from .. common import verify_raw_data, verify_input, verify_outpath
from .. util import run_ogr2ogr


ST_PATT = re.compile('^\s*([0-9]{2}),*\s*$')
ST_CO_PATT = re.compile('^\s*([0-9]{5}),*\s*$')

logger = logging.getLogger(__name__)


def _parse_county_fips(input_path: str) -> dict:
    state_fips = set()
    state_county_fips = set()
    fips = {'state': state_fips,
            'state_county': state_county_fips}
    with open(input_path) as f:
        for l in f:
            m = ST_PATT.match(l)
            if m:
                state_fips.add(m.group(1))
                continue
            m = ST_CO_PATT.match(l)
            if m:
                state_county_fips.add(m.group(1))
                continue

    # Scan state+county FIPS to make sure they are not covered by state FIPS
    # Copy list to set so that we can mutate set as we iterate
    state_county_fips_list = [f for f in state_county_fips]
    for st_co_fip in state_county_fips_list:
        if st_co_fip[:2] in state_fips:
            try:
                state_county_fips.remove(st_co_fip)
            except KeyError:
                # Ignore: may have already been removed from set in previous iteration over list copy of set.
                pass

    return fips


def main():
    parser = argparse.ArgumentParser(description='Extract county definitions in CARMA format from TIGER/Census datasets')
    parser.add_argument('-d', '--datapath', help=('Directory containing data downloaded/extracted from '
                                                  'bin/download-data.sh.'))
    parser.add_argument('-o', '--outpath', help='Directory where output should be stored.')
    parser.add_argument('-n', '--outname', help=('Name of file, stored in outpath, where CARMA-schema formatted output '
                                                'should be stored.'))
    parser.add_argument('-i', '--county_path', help='Path to file containing one or more state or county FIPS code, one per line.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    success, data_result = verify_raw_data(args.datapath)
    if not success:
        for e in data_result['errors']:
            print(e)
        sys.exit("Invalid source data, exiting. Try running 'download-data.sh'.")

    success, out_result = verify_outpath(args.outpath, args.outname, args.overwrite)
    if not success:
        for e in out_result['errors']:
            print(e)
        sys.exit("Output path or name errors, exiting.")

    success, input_result = verify_input(args.county_path)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        # Read county FIPS from input file
        fips = _parse_county_fips(args.county_path)
        logger.debug(f"FIPS to extract: {fips}")

        carma_counties = []
        # First, entire states
        for state in fips['state']:
            pass

    except Exception as e:
        print(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
