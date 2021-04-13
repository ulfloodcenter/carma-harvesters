import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil

from shapely.geometry import asShape

from carma_schema import get_crop_data_for_entity, get_developed_area_data_for_entity, get_wassi_analysis_by_id, \
    update_wassi_analysis_instance
from carma_schema.util import get_sub_huc12_id
from carma_schema.types import AnalysisWaSSI, SurfaceWeightsWaSSI, CountyDisaggregationWaSSI

from carma_harvesters.common import open_existing_carma_document, verify_input, output_json
from carma_harvesters.util import Geometry, select_points_contained_by_geometry
from carma_harvesters.wells import WellAttributeMapper
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Import groundwater well locations that intersect a HUC12 or '
                                                  'sub-HUC12 watersheds.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 or sub-HUC12 watersheds '
                              'and county definitions. Resulting WaSSI weights '
                              'will be written to the same file.'))
    parser.add_argument('-w', '--well_data_path', required=True,
                        help=('Point GIS dataset containing well locations along with the following attributes: '
                              'sector, status, and year completed.'))
    parser.add_argument('-a', '--attribute_map_path', required=True,
                        help=('Path to JSON file mapping well attributes and values onto those defined in CARMA '
                              'schema.'))
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

    abs_well_inpath = os.path.abspath(args.well_data_path)
    success, input_result = verify_input(abs_well_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid well input data, exiting.")

    abs_attr_inpath = os.path.abspath(args.attribute_map_path)
    success, input_result = verify_input(abs_attr_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid well attribute input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'SubHUC12Watersheds' not in document or len(document['SubHUC12Watersheds']) < 1:
            sys.exit(f"No sub-HUC12 watersheds defined in {abs_carma_inpath}")

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        # Open well attribute map
        well_attr_mapper = WellAttributeMapper(abs_attr_inpath)

        # Foreach county...
        for county in document['Counties']:
            county_geom = Geometry(county['geometry'])
            county_shape = asShape(county_geom)

            # 1. Select wells in the county
            import pdb; pdb.set_trace()
            wells = select_points_contained_by_geometry(abs_well_inpath, county_shape)
            for well in wells['features']:
                pass
                # 2. Extract CARMA attributes for each well
                # 3. Sum wells in each CARMA catagory and write to document

        # TODO: Foreach sub-HUC12...
        # 1. Select wells in the sub-HUC12
        # 2. Extract CARMA attributes for each well
        # 3. Sum wells in each CARMA catagory and write to document

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
