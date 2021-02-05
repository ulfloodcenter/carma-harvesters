import argparse
import logging
import sys
import os
import traceback

from carma_schema import get_county_ids

from .. exception import SchemaValidationException
from .. common import verify_input, output_json, open_existing_carma_document


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Generate sub-HUC12 watersheds by intersecting HUC12 watershed '
                                                  'boundaries with county boundaries. A sub-HUC12 watershed is a '
                                                  'portion of a HUC12 that is entirely contained in a county. '
                                                  'If a HUC12 is entirely contained in a county, a single sub-HUC12 '
                                                  'watershed will be generated whose boundary corresponds to that of '
                                                  'the original HUC12 watershed.')),
    parser.add_argument('-c', '--carma_inpath', help=('Path of CARMA file containing definitions of HUC12 watersheds '
                                                      'and county definitions. Resulting sub-HUC12 watersheds '
                                                      'will be written to the the same file.'))
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

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        pass