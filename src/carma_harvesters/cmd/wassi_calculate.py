import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import uuid
import math

from carma_schema import get_water_use_data_for_county, get_wassi_analysis_by_id
from carma_schema.types import get_wateruse_dataset_key

from carma_harvesters.common import open_existing_carma_document, verify_input, output_json
from carma_harvesters.analysis.wassi import get_sector_weights, convert_county_wateruse_data_to_huc, \
    SECTOR_VALUE_TO_PROPERTY_NAME, GW_WEIGHT_KEY
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
                        help='UUID representing the ID of WaSSI analysis to add these weights to.')
    parser.add_argument('-y', '--year', type=int, default=2015,
                        help='Year of water use data that should be disaggregated.')
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

        if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
            sys.exit(f"No HUC12 watersheds defined in {abs_carma_inpath}")

        if 'WaterUseDatasets' not in document or len(document['WaterUseDatasets']) < 1:
            sys.exit(f"No water use data defined in {abs_carma_inpath}")

        # Find WaSSI analysis specified by wassi_id
        wassi = get_wassi_analysis_by_id(document, wassi_id)
        if wassi is None:
            sys.exit(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        # TODO: Calculate WaSSI for each sector

        # Write document back out
        output_json(abs_carma_inpath, temp_out, document, True)

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)