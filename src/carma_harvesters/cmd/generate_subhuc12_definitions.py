import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import math
from collections import OrderedDict

from shapely.geometry import asShape, mapping

from carma_schema import get_county_ids, get_huc12_ids

from .. exception import SchemaValidationException
from .. common import verify_input, output_json, open_existing_carma_document, write_objects_to_existing_carma_document
from .. geoconnex.usgs import HydrologicUnit
from .. util import Geometry


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Generate sub-HUC12 watersheds by intersecting HUC12 watershed '
                                                  'boundaries with county boundaries. A sub-HUC12 watershed is a '
                                                  'portion of a HUC12 that is entirely contained in a county. '
                                                  'If a HUC12 is entirely contained in a county, a single sub-HUC12 '
                                                  'watershed will be generated whose boundary corresponds to that of '
                                                  'the original HUC12 watershed.'))
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

        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
            sys.exit(f"No HUC12 watersheds defined in {abs_carma_inpath}")

        # Build sub-HUC12 watersheds (i.e. parts of HUC12 watersheds that intersect a county)
        sub_huc12s = []

        # For each HUC12, determine which counties it intersects with
        for huc in document['HUC12Watersheds']:
            huc_geom = Geometry(huc['geometry'])
            huc_shape = asShape(huc_geom)
            # Iterate over all counties, checking for an intersection
            for county in document['Counties']:
                county_geom = Geometry(county['geometry'])
                county_shape = asShape(county_geom)
                # HUC12 intersects with county, create sub HUC12 objects
                if huc_shape.intersects(county_shape):
                    sub_huc = OrderedDict()
                    sub_huc['huc12'] = huc['id']
                    sub_huc['county'] = county['id']
                    sub_huc['area'] = 0.0
                    sub_huc['crops'] = 0.0
                    sub_huc['developedArea'] = 0.0
                    sub_huc['maxStreamOrder'] = 0.0
                    sub_huc['minStreamLevel'] = 0.0
                    sub_huc['meanAnnualFlow'] = 0.0
                    sub_huc['geometry'] = mapping(huc_shape.intersection(county_shape))
                    sub_huc12s.append(sub_huc)

        # For each sub-HUC12, save intersection geometry

        # Use intersection geometry to calculate WaSSI weights: W1, W2, W3, W4

        # Save sub-HUC12 definitions
        write_objects_to_existing_carma_document(sub_huc12s, 'SubHUC12Watersheds',
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