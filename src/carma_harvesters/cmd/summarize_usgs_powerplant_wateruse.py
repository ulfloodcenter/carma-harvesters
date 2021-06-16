import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil

from carma_harvesters.common import open_existing_carma_document, verify_input, write_objects_to_existing_carma_document
from carma_harvesters.powerplants.usgs import summarize_powerplant_data_by_huc12

from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Summarize USGS water use data for thermoelectric power plants '
                                                  'located in each HUC12 watershed; summarize by water source, and '
                                                  'water type.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watersheds and individual powerplant '
                              'water use data that needs to be summarized by water source, type, and sector for each '
                              'HUC12.'))
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
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'PowerPlantDatasets' not in document or len(document['PowerPlantDatasets']) < 1:
            sys.exit(f"No powerplant datasets defined in {abs_carma_inpath}")

        water_use_objects = summarize_powerplant_data_by_huc12(document['PowerPlantDatasets'])

        # Write updated CARMA file
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
