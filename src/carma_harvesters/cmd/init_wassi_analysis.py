# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import uuid
from dataclasses import asdict

from carma_schema.types import AnalysisWaSSI,\
    SectorWeightFactorGroundwaterWaSSI, SectorWeightFactorSurfaceWaSSI

from carma_harvesters.common import open_existing_carma_document, verify_input, write_objects_to_existing_carma_document
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Initialize water supply stress index (WaSSI; Sun et al. 2008) '
                                                  'analysis object as used in Eldardiry et al. 2016 '
                                                  '(doi:10.1088/1748-9326/aa51dc).'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of sub-HUC12 watersheds '
                              'and county definitions. Resulting WaSSI analysis header '
                              'will be written to the same file.'))
    parser.add_argument('-uy', '--water_use_year', type=int, default=2015,
                        help='Year of water use data to use in WaSSI analysis.')
    parser.add_argument('-cy', '--crop_year', type=int, default=2015,
                        help='Year of crop data to use in WaSSI analysis.')
    parser.add_argument('-dy', '--developed_area_year', type=int, default=2016,
                        help='Year of developed area data to use in WaSSI analysis.')
    parser.add_argument('-wy', '--well_year_completed', type=int, default=2015,
                        help='Year during or before which wells were completed.')
    parser.add_argument('-d', '--description', help=('Description to be added to description field of WaSSI analysis '
                                                     'object.'))
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

        wassi_id = str(uuid.uuid4())
        analysis_wassi = AnalysisWaSSI(wassi_id,
                                       args.water_use_year,
                                       args.crop_year,
                                       args.developed_area_year,
                                       args.well_year_completed,
                                       description=args.description)

        # Write AnalysisWaSSI object to document
        analyses = [{'WaSSI': [analysis_wassi.asdict()]}]
        write_objects_to_existing_carma_document(analyses, 'Analyses',
                                                 document, abs_carma_inpath,
                                                 temp_out, args.overwrite)
        print(f"New WaSSI analysis created with ID {wassi_id}")

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
