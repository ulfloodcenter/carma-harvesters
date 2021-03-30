import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil

from carma_schema import get_crop_data_for_entity, get_developed_area_data_for_entity
from carma_schema.util import get_sub_huc12_id

from carma_harvesters.common import open_existing_carma_document, verify_input, verify_raw_data
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Generate weights W1 through W4 required to calculate the water '
                                                  'supply stress index (WaSSI; Sun et al. 2008) as used in Eldardiry '
                                                  'et al. 2016 (doi:10.1088/1748-9326/aa51dc). The WaSSI weights are '
                                                  'used to disaggregate county-level water use data to the HUC12 '
                                                  'scale.'))
    # parser.add_argument('-d', '--datapath', required=True,
    #                     help=('Directory containing data downloaded/extracted from '
    #                           'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of sub-HUC12 watersheds '
                              'and county definitions. Resulting WaSSI weights '
                              'will be written to the same file.'))
    parser.add_argument('-cy', '--crop_year', type=int, default=2019,
                        help='Year of crop data to use to generate WaSSI weights.')
    parser.add_argument('-dy', '--developed_area_year', type=int, default=2016,
                        help='Year of developed area data to use to generate WaSSI weights.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    # success, data_result = verify_raw_data(args.datapath)
    # if not success:
    #     for e in data_result['errors']:
    #         print(e)
    #     sys.exit("Invalid source data, exiting. Try running 'download-data.sh'.")

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

        if 'SubHUC12Watersheds' not in document or len(document['SubHUC12Watersheds']) < 1:
            sys.exit(f"No sub-HUC12 watersheds defined in {abs_carma_inpath}")

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        # Foreach county...
        for county in document['Counties']:
            logger.debug(f"Calculating weights for HUC12s in county {county['id']}")
            # 1. Find county crop area for specified year, report error if none
            county_crops_for_year = get_crop_data_for_entity(county, args.crop_year)
            if county_crops_for_year is None:
                sys.exit(f"County {county['id']} does not have crop data for year {args.crop_year}.")
            # 2. Find county developed area for specified year, report error if none
            county_devel_area_for_year = get_developed_area_data_for_entity(county, args.developed_area_year)
            if county_devel_area_for_year is None:
                sys.exit(f"County {county['id']} does not have developed area data for "
                         f"year {args.developed_area_year}.")

            # Initialize accumulator variables for weights to check that each weight sums to 1
            # for a given county
            sum_w1 = sum_w2 = sum_w4 = denom_w3 = 0.0

            w1 = {}
            w2 = {}
            w3 = {}
            w4 = {}

            # 3. Foreach sub-HUC12 in county...
            for sub_huc12 in filter(lambda s: s['county'] == county['id'], document['SubHUC12Watersheds']):
                sub_huc_id = get_sub_huc12_id(sub_huc12)
                # 1. Find sub-HUC12 crop area for specified year, report error if none
                sub_huc12_crops_for_year = get_crop_data_for_entity(sub_huc12, args.crop_year)
                if sub_huc12_crops_for_year is None:
                    sys.exit((f"Sub-HUC12 {sub_huc_id} does not have crop data for "
                              f"year {args.crop_year}."))
                # 2. Find sub-HUC12 developed area for specified year, report error if none
                sub_huc12_devel_area_for_year = get_developed_area_data_for_entity(sub_huc12, args.developed_area_year)
                if sub_huc12_devel_area_for_year is None:
                    sys.exit(f"Sub-HUC12 {sub_huc_id} does not have developed area "
                             f"data for year {args.developed_area_year}.")

                # 3. Calculate weights:
                # Calculate W1 (A): sub-HUC12 area / county
                w1[sub_huc_id] = sub_huc12['area'] / county['area']
                logger.debug(f"Weight W1 (A) for Sub-HUC12 {sub_huc_id} = {w1[sub_huc_id]}")
                sum_w1 += w1[sub_huc_id]

                # Calculate W2 (CA): sub-HUC12 crop area / county crop area
                w2[sub_huc_id] = sub_huc12_crops_for_year.crop_area / county_crops_for_year.crop_area
                logger.debug(f"Weight W2 (CA) for Sub-HUC12 {sub_huc_id} = {w2[sub_huc_id]}")
                sum_w2 += w2[sub_huc_id]

                w3[sub_huc_id] = sub_huc12['maxStreamOrder']
                # Sum(Max SO) in county so that W3 can later be calculated
                denom_w3 += sub_huc12['maxStreamOrder']

                # Calculate W4 (HD): Highly devel. area in sub-HUC12 / Highly devel. area in county
                w4[sub_huc_id] = sub_huc12_devel_area_for_year.area / county_devel_area_for_year.area
                logger.debug(f"Weight W4 (HD) for Sub-HUC12 {sub_huc_id} = {w4[sub_huc_id]}")
                sum_w4 += w4[sub_huc_id]

            # Now calculate w3 for each sub-HUC12
            sum_w3 = 0.0
            for sub_huc_id in w3:
                w3[sub_huc_id] = w3[sub_huc_id] / denom_w3
                logger.debug(f"Weight W3 (SO) for Sub-HUC12 {sub_huc_id} = {w3[sub_huc_id]}")
                sum_w3 += w3[sub_huc_id]

            # TODO: 4. Write AnalysisWaSSI entry to document for this HUC-12, county combination
            logger.debug(f"Sum of weight W1 for county {county['id']} = {sum_w1}")
            logger.debug(f"Sum of weight W2 for county {county['id']} = {sum_w2}")
            logger.debug(f"Sum of weight W3 for county {county['id']} = {sum_w3}")
            logger.debug(f"Sum of weight W4 for county {county['id']} = {sum_w4}")

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
