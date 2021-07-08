import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import uuid

from carma_schema import CarmaItemNotFound

from carma_harvesters.common import open_existing_carma_document, verify_input, output_json
from carma_harvesters.analysis.wassi import calculate_wassi_for_huc12_watersheds
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Calculate water supply stress index (WaSSI; Sun et al. 2008) '
                                                  'as used in Eldardiry et al. 2016 (doi:10.1088/1748-9326/aa51dc). '
                                                  'Requires that WaSSI weights be present in the CARMA input file.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of WaSSI analysis and HUC12-level water '
                              'use data. HUC12-based WaSSI indices for each sector will be written to the same file.'))
    parser.add_argument('-i', '--wassi_id', required=True,
                        help='UUID representing the ID of WaSSI analysis to calculate values for.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    wassi_id = None
    try:
        wassi_id = uuid.UUID(args.wassi_id)
    except ValueError as e:
        sys.exit(f"Invalid WaSSI ID {args.wassi_id}.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        # Calculate WaSSI
        calculate_wassi_for_huc12_watersheds(abs_carma_inpath, document, wassi_id,
                                             args.overwrite)

        # Write document back out
        output_json(abs_carma_inpath, temp_out, document, True)

    except CarmaItemNotFound as cinf:
        logger.error(traceback.format_exc())
        sys.exit(cinf)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)