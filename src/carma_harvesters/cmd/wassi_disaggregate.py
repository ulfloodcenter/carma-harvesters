import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
import uuid
import math

from tqdm import tqdm

from carma_schema import get_water_use_data_for_county, get_wassi_analysis_by_id
from carma_schema.types import get_wateruse_dataset_key

from carma_harvesters.common import open_existing_carma_document, verify_input, output_json
from carma_harvesters.analysis.wassi import get_sector_weights, convert_county_wateruse_data_to_huc, \
    SECTOR_VALUE_TO_PROPERTY_NAME, GW_WEIGHT_KEY
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Disaggregate surface and groundwater water use data from county '
                                                  'level to HUC12 scale for use in water supply stress index '
                                                  '(WaSSI; Sun et al. 2008) calculations as used in Eldardiry '
                                                  'et al. 2016 (doi:10.1088/1748-9326/aa51dc). Requires that WaSSI '
                                                  'weights be present in the CARMA input file.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of WaSSI analysis and county-level water '
                              'use data. Disaggregated HUC12-scale water use data will be written to the same file.'))
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

        if 'WaterUseDatasets' not in document or len(document['WaterUseDatasets']) < 1:
            sys.exit(f"No water use data defined in {abs_carma_inpath}")

        # Find WaSSI analysis specified by wassi_id
        wassi = get_wassi_analysis_by_id(document, wassi_id)
        if wassi is None:
            sys.exit(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        if wassi.countyDisaggregations is None:
            sys.exit(f"No county disaggregations in WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        # Foreach county disaggregation in WaSSI analysis
        huc12_wuds = {}
        progress_bar = tqdm(wassi.countyDisaggregations)
        for disag in progress_bar:
            progress_bar.set_description(f"{disag.huc12}:{disag.county}")
            for wud in get_water_use_data_for_county(document, disag.county, wassi.waterUseYear):
                sector_weights = get_sector_weights(wassi, wud.waterSource, wud.sector)
                if len(sector_weights) == 0:
                    logger.warning((f"Unable to find sector weights for water source {wud.waterSource} "
                                    f"& sector {wud.sector}. Skipping..."))
                    continue

                # Calculate weight
                w_huc = None
                if wud.waterSource == 'Surface Water':
                    # Set to identity function so we can just multiply and avoid complicated logic
                    w_huc = 1.0
                    for w in sector_weights:
                        w_huc *= disag.surfaceWeights[w]
                    w_huc = math.pow(w_huc, (1 / len(sector_weights)))
                elif wud.waterSource == 'Groundwater':
                    if wud.sector not in SECTOR_VALUE_TO_PROPERTY_NAME:
                        logger.warning(f"Unknown sector {wud.sector}, skipping...")
                        continue
                    sector_property = SECTOR_VALUE_TO_PROPERTY_NAME[wud.sector]
                    w_huc = disag.groundwaterWeights[GW_WEIGHT_KEY][sector_property]

                # Disaggregate datum using weight and store in HUC12 copy of the water use data
                huc_wud_key = get_wateruse_dataset_key(wud, override_huc12=disag.huc12)
                if huc_wud_key not in huc12_wuds:
                    huc_wud = convert_county_wateruse_data_to_huc(wud, disag.huc12, w_huc)
                    huc12_wuds[huc_wud_key] = huc_wud
                else:
                    huc12_wuds[huc_wud_key].value += wud.value * w_huc

        # Update "WaterUseDatasets" in CARMA document to include new HUC12-scale water use data
        for huc_wud in huc12_wuds.values():
            document['WaterUseDatasets'].append(huc_wud.asdict())

        # DEBUG: search for duplicates
        for i, curr in enumerate(document['WaterUseDatasets'], start=1):
            for j, other in enumerate(document['WaterUseDatasets'], start=1):
                if i != j:
                    if curr == other:
                        logger.warning(f"WaterUseDataset: {curr} is duplicated at indices {i} and {j}.")

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