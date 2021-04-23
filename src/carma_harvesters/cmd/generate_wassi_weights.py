import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import uuid

from carma_schema import get_crop_data_for_entity, get_developed_area_data_for_entity, get_well_counts_for_entity, \
    get_wassi_analysis_by_id, update_wassi_analysis_instance
from carma_schema.util import get_sub_huc12_id
from carma_schema.types import SurfaceWeightsWaSSI, GroundwaterWeightsWaSSI, CountyDisaggregationWaSSI

from carma_harvesters.common import open_existing_carma_document, verify_input, output_json
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Generate weights W1 through W4 required to calculate the water '
                                                  'supply stress index (WaSSI; Sun et al. 2008) as used in Eldardiry '
                                                  'et al. 2016 (doi:10.1088/1748-9326/aa51dc). The WaSSI weights are '
                                                  'used to disaggregate county-level water use data to the HUC12 '
                                                  'scale.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of sub-HUC12 watersheds '
                              'and county definitions. Resulting WaSSI weights '
                              'will be written to the same file.'))
    parser.add_argument('-i', '--wassi_id', required=True,
                        help='UUID representing the ID of WaSSI analysis to add these weights to.')
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

        # Find WaSSI analysis specified by wassi_id
        wassi = get_wassi_analysis_by_id(document, wassi_id)
        if wassi is None:
            sys.exit(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        if 'SubHUC12Watersheds' not in document or len(document['SubHUC12Watersheds']) < 1:
            sys.exit(f"No sub-HUC12 watersheds defined in {abs_carma_inpath}")

        if 'Counties' not in document or len(document['Counties']) < 1:
            sys.exit(f"No counties defined in {abs_carma_inpath}")

        analysis_wassi_entries = []

        # Foreach county...
        for county in document['Counties']:
            logger.debug(f"Calculating weights for HUC12s in county {county['id']}")
            # 1. Find county crop area for specified year, report error if none
            county_crops_for_year = get_crop_data_for_entity(county, wassi.cropYear)
            if county_crops_for_year is None:
                sys.exit(f"County {county['id']} does not have crop data for year {wassi.cropYear}.")
            # 2. Find county developed area for specified year, report error if none
            county_devel_area_for_year = get_developed_area_data_for_entity(county, wassi.developedAreaYear)
            if county_devel_area_for_year is None:
                sys.exit(f"County {county['id']} does not have developed area data for "
                         f"year {wassi.developedAreaYear}.")
            # 3. Get county groundwater well counts for specified year, report error if none
            county_wells_for_year = get_well_counts_for_entity(county, wassi.groundwaterWellsCompletedYear)
            if len(county_wells_for_year) == 0:
                sys.exit(f"County {county['id']} does not have groundwater well counts for "
                         f"year {wassi.groundwaterWellsCompletedYear}.")
            county_well_counts = {}
            for wc in county_wells_for_year:
                if wc.status == 'Active':
                    county_well_counts[wc.sector] = wc.count

            # Initialize accumulator variables for weights to check that each weight sums to 1
            # for a given county
            sum_w1 = sum_w2 = sum_w4 = denom_w3 = 0.0
            sum_gw1 = GroundwaterWeightsWaSSI()

            w1 = {}
            w2 = {}
            w3 = {}
            w4 = {}
            gw1 = {}
            sub_huc12s = []

            # 3. Foreach sub-HUC12 in county...
            for sub_huc12 in filter(lambda s: s['county'] == county['id'], document['SubHUC12Watersheds']):
                sub_huc12s.append(sub_huc12)
                huc12_id = sub_huc12['huc12']
                sub_huc_id = get_sub_huc12_id(sub_huc12)
                # 1. Find sub-HUC12 crop area for specified year, report error if none
                sub_huc12_crops_for_year = get_crop_data_for_entity(sub_huc12, wassi.cropYear)
                if sub_huc12_crops_for_year is None:
                    sys.exit((f"Sub-HUC12 {sub_huc_id} does not have crop data for "
                              f"year {wassi.cropYear}."))
                # 2. Find sub-HUC12 developed area for specified year, report error if none
                sub_huc12_devel_area_for_year = get_developed_area_data_for_entity(sub_huc12, wassi.developedAreaYear)
                if sub_huc12_devel_area_for_year is None:
                    sys.exit(f"Sub-HUC12 {sub_huc_id} does not have developed area "
                             f"data for year {wassi.developedAreaYear}.")

                # 3. Get sub-HUC12 groundwater well counts for specified year, report error if none
                sub_huc12_wells_for_year = get_well_counts_for_entity(sub_huc12, wassi.groundwaterWellsCompletedYear)
                sub_huc12_well_counts = {}
                for wc in sub_huc12_wells_for_year:
                    if wc.status == 'Active':
                        sub_huc12_well_counts[wc.sector] = wc.count

                # 4. Calculate weights:
                # Calculate W1 (A): sub-HUC12 area / county
                w1[huc12_id] = sub_huc12['area'] / county['area']
                logger.debug(f"Weight W1 (A) for Sub-HUC12 {sub_huc_id} = {w1[huc12_id]}")
                sum_w1 += w1[huc12_id]

                # Calculate W2 (CA): sub-HUC12 crop area / county crop area
                w2[huc12_id] = sub_huc12_crops_for_year.crop_area / county_crops_for_year.crop_area
                logger.debug(f"Weight W2 (CA) for Sub-HUC12 {sub_huc_id} = {w2[huc12_id]}")
                sum_w2 += w2[huc12_id]

                w3[huc12_id] = sub_huc12['maxStreamOrder']
                # Sum(Max SO) in county so that W3 can later be calculated
                denom_w3 += sub_huc12['maxStreamOrder']

                # Calculate W4 (HD): Highly devel. area in sub-HUC12 / Highly devel. area in county
                w4[huc12_id] = sub_huc12_devel_area_for_year.area / county_devel_area_for_year.area
                logger.debug(f"Weight W4 (HD) for Sub-HUC12 {sub_huc_id} = {w4[huc12_id]}")
                sum_w4 += w4[huc12_id]

                # Calculate GW1: number of groundwater wells in sub-HUC12 / number of groundwater wells in county
                sub_huc12_gw1 = GroundwaterWeightsWaSSI()
                for sector, sub_huc12_count in sub_huc12_well_counts.items():
                    sub_huc12_gw1[sector] = sub_huc12_count / county_well_counts[sector]
                gw1[huc12_id] = sub_huc12_gw1
                sum_gw1.accum(sub_huc12_gw1)

            # Now calculate w3 for each sub-HUC12
            sum_w3 = 0.0
            for huc12_id in w3:
                w3[huc12_id] = w3[huc12_id] / denom_w3
                logger.debug(f"Weight W3 (SO) for Sub-HUC12 {huc12_id} = {w3[huc12_id]}")
                sum_w3 += w3[huc12_id]

            # 4. Save as AnalysisWaSSI object instance for this HUC-12, county combination
            logger.debug(f"Sum of weight W1 for county {county['id']} = {sum_w1}")
            logger.debug(f"Sum of weight W2 for county {county['id']} = {sum_w2}")
            logger.debug(f"Sum of weight W3 for county {county['id']} = {sum_w3}")
            logger.debug(f"Sum of weight W4 for county {county['id']} = {sum_w4}")
            logger.debug(f"Sum of weight GW1 for county {county['id']} = {sum_gw1}")

            county_disaggs = []
            for sub_huc12 in sub_huc12s:
                huc12_id = sub_huc12['huc12']
                ca = CountyDisaggregationWaSSI(huc12_id, sub_huc12['county'],
                                               SurfaceWeightsWaSSI(w1[huc12_id],
                                                                   w2[huc12_id],
                                                                   w3[huc12_id],
                                                                   w4[huc12_id]),
                                               gw1[huc12_id])
                county_disaggs.append(ca)
            if args.overwrite or wassi.countyDisaggregations is None:
                wassi.countyDisaggregations = county_disaggs
            else:
                wassi.countyDisaggregations = wassi.countyDisaggregations + county_disaggs

        # Write updated AnalysisWaSSI instance back to document (always overwrite because we merged
        # county disaggregation entries above if args.overwrite==True).
        update_wassi_analysis_instance(document, wassi)
        output_json(abs_carma_inpath, temp_out, document, True)

    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
