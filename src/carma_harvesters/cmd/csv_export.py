import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
from collections import OrderedDict
import uuid
import csv

from carma_schema import CarmaItemNotFound, get_wassi_analysis_by_id, join_wassi_values_to_huc12

from .. analysis.conversion import *
from .. analysis.wassi import get_huc12_wateruse_data
from .. exception import SchemaValidationException
from .. common import verify_input, verify_output, open_existing_carma_document


logger = logging.getLogger(__name__)


def _entity_to_dict(entity):
    """
    Excludes geometry property
    :param entity:
    :return:
    """
    properties = OrderedDict()
    for k in filter(lambda k: k != 'geometry', entity.keys()):
        properties[k] = entity[k]
    return properties


def main():
    parser = argparse.ArgumentParser(description=('Export HUC12, definitions from a CARMA data '
                                                  'file into CSV file.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions HUC12, county, and '
                              'sub-HUC12 definitions that should be export to GeoJSON.'))
    parser.add_argument('-o', '--csv_out', required=True,
                        help=('Name of file to contain CSV representations of CARMA '
                              'HUC12 data'))
    parser.add_argument('-i', '--wassi_id', required=True,
                        help='UUID representing the ID of WaSSI analysis to export HUC12 values for.')
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

    success, out_result = verify_output(args.csv_out, args.overwrite)
    if not success:
        for e in out_result['errors']:
            print(e)
        sys.exit("Invalid output path, exiting.")

    wassi_id = None
    if args.wassi_id:
        try:
            wassi_id = uuid.UUID(args.wassi_id)
        except ValueError as e:
            sys.exit(f"Invalid WaSSI ID {args.wassi_id}.")

    try:
        document = open_existing_carma_document(abs_carma_inpath)

        wassi = None
        if wassi_id:
            wassi = get_wassi_analysis_by_id(document, wassi_id)
            if wassi is None:
                raise CarmaItemNotFound(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        with open(out_result['paths']['out_file_path'], 'w') as csvfile:
            field_names = ['HUC12', 'Area_of_HUC12_(m2)', 'Area_of_HUC12_(km2)', 'Area_of_HUC12_(Acres)',
                           'SW-NHDPLUS_(CFS)', 'SW-NHDPLUS_(Acres.Feet/Year)', 'GW-USGS_(mm/year/km2)',
                           'GW-USGS_(Acres.Feet/Year)', 'Agriculture', 'Industrial', 'Power_Generation',
                           'Public_Supply', 'Agriculture', 'Industrial', 'Power_Generation', 'Public_Supply',
                           'Total_SW_Use_(MGD)', 'Total_SW_Use_(Acres.Feet/Year)', 'Agriculture', 'Industrial',
                           'Power_Generation', 'Public_Supply', 'Livestock', 'Rural_Domestic', 'Agriculture',
                           'Industrial', 'Power_Generation', 'Public_Supply', 'Livestock', 'Rural_Domestic',
                           'Total_GW_Use_(MGD)', 'Total_GW_Use_(Acres.Feet/Year)', 'Withdrawal', 'Available',
                           'Stress', 'Balance']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            if 'HUC12Watersheds' in document:
                for h12 in document['HUC12Watersheds']:
                    row = {}
                    huc12_id = h12['id']
                    h12_wassi = join_wassi_values_to_huc12(wassi, _entity_to_dict(h12))
                    huc_wu = get_huc12_wateruse_data(document, huc12_id, wassi.waterUseYear)
                    row['HUC12'] = huc12_id
                    area = h12['area']
                    row['Area_of_HUC12_(m2)'] = area * 1000000
                    row['Area_of_HUC12_(km2)'] = area
                    row['Area_of_HUC12_(Acres)'] = km2_to_acre(area)
                    maf = h12['meanAnnualFlow']
                    row['SW-NHDPLUS_(CFS)'] = maf
                    row['SW-NHDPLUS_(Acres.Feet/Year)'] = cfs_to_acre_ft_per_yr(maf)
                    recharge = h12['recharge']
                    row['GW-USGS_(mm/year/km2)'] = recharge
                    row['GW-USGS_(Acres.Feet/Year)'] = mm_per_km2_per_yr_to_acre_ft_per_year(recharge)
                    # TODO: The rest of the fields ...

                    writer.writerow(row)

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
