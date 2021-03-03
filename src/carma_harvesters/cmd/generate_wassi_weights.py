import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil

from carma_harvesters.common import open_existing_carma_document, verify_input, verify_raw_data
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Generate weights W1 through W4 required to calculate the water '
                                                  'supply stress index (WaSSI; Sun et al. 2008) as used in Eldardiry '
                                                  'et al. 2016 (doi:10.1088/1748-9326/aa51dc). The WaSSI weights are '
                                                  'used to disaggregate county-level water use data to the HUC12 '
                                                  'scale.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of sub-HUC12 watersheds '
                              'and county definitions. Resulting WaSSI weights '
                              'will be written to the same file.'))
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

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
