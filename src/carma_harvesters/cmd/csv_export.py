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
from carma_schema.geoconnex.usgs import HydrologicUnit

from .. analysis.conversion import *
from .. analysis.wassi import get_huc12_wateruse_data, get_group_sum_value
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
    parser.add_argument('--debug', help='Debug mode: do not delete output if there is an exception',
                        action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    temp_out = None

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

    error = False

    try:
        document = open_existing_carma_document(abs_carma_inpath)

        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        wassi = None
        if wassi_id:
            wassi = get_wassi_analysis_by_id(document, wassi_id)
            if wassi is None:
                raise CarmaItemNotFound(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")
            # Make sure there are WaSSI values
            if wassi.wassiValues is None or len(wassi.wassiValues) == 0:
                sys.exit(f"WaSSI analysis {wassi_id} contains no WaSSI values")

        with open(out_result['paths']['out_file_path'], 'w') as csvfile:
            field_names = ['HUC12', 'Area_of_HUC12_(m2)', 'Area_of_HUC12_(km2)', 'Area_of_HUC12_(Acres)',
                           'SW-NHDPLUS_(CFS)', 'SW-NHDPLUS_(Acres.Feet/Year)', 'GW-USGS_(mm/year/km2)',
                           'GW-USGS_(Acres.Feet/Year)', 'Irrigation_SW', 'Industrial_SW', 'Power_Generation_SW',
                           'Public_Supply_SW', 'Irrigation_SW_(Acres.Feet/Year)', 'Industrial_SW_(Acres.Feet/Year)',
                           'Power_Generation_SW_(Acres.Feet/Year)', 'Public_Supply_SW_(Acres.Feet/Year)',
                           'Total_SW_Use_(MGD)', 'Total_SW_Use_(Acres.Feet/Year)', 'Irrigation_GW', 'Industrial_GW',
                           'Power_Generation_GW', 'Public_Supply_GW', 'Livestock_GW', 'Rural_Domestic_GW',
                           'Irrigation_GW_(Acres.Feet/Year)', 'Industrial_GW_(Acres.Feet/Year)',
                           'Power_Generation_GW_(Acres.Feet/Year)', 'Public_Supply_GW_(Acres.Feet/Year)',
                           'Livestock_GW_(Acres.Feet/Year)', 'Rural_Domestic_GW_(Acres.Feet/Year)',
                           'Total_GW_Use_(MGD)', 'Total_GW_Use_(Acres.Feet/Year)', 'Withdrawal', 'Available',
                           'Stress', 'Balance', 'SW_Stress']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            if 'HUC12Watersheds' in document:
                for h12 in document['HUC12Watersheds']:
                    row = {}
                    huc12_id = h12['id']
                    h12_wassi = join_wassi_values_to_huc12(wassi, _entity_to_dict(h12))
                    huc_wu = get_huc12_wateruse_data(document, huc12_id, wassi.waterUseYear)
                    row['HUC12'] = HydrologicUnit.parse_fq_id(huc12_id)
                    area = h12['area']
                    row['Area_of_HUC12_(m2)'] = area * 1000000
                    row['Area_of_HUC12_(km2)'] = area
                    row['Area_of_HUC12_(Acres)'] = km2_to_acre(area)
                    if 'meanAnnualFlow' in h12:
                        maf = h12['meanAnnualFlow']
                    else:
                        maf = 0.0
                    row['SW-NHDPLUS_(CFS)'] = maf
                    row['SW-NHDPLUS_(Acres.Feet/Year)'] = cfs_to_acre_ft_per_yr(maf)
                    if 'recharge' in h12:
                        recharge = h12['recharge']
                    else:
                        recharge = 0.0
                    row['GW-USGS_(mm/year/km2)'] = recharge
                    row['GW-USGS_(Acres.Feet/Year)'] = mm_per_km2_per_yr_to_acre_ft_per_year(recharge, area)
                    # Water use fields ...
                    grouped = huc_wu.groupby(['sector', 'is_consumptive', 'water_source', 'water_type'])
                    group_sum = grouped.sum()
                    # Surface water
                    irrigation_surf_withdrawal = get_group_sum_value(group_sum,
                                                                     'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source == "Surface Water"')
                    row['Irrigation_SW'] = irrigation_surf_withdrawal
                    row['Irrigation_SW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(irrigation_surf_withdrawal)

                    industrial_surf_withdrawal = get_group_sum_value(group_sum,
                                                                     'is_consumptive == False and sector == "Industrial" and water_type != "Any" and water_source == "Surface Water"')
                    row['Industrial_SW'] = industrial_surf_withdrawal
                    row['Industrial_SW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(industrial_surf_withdrawal)

                    thermo_electric_surf_withdrawal = get_group_sum_value(group_sum,
                                                                          'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source == "Surface Water"')
                    row['Power_Generation_SW'] = thermo_electric_surf_withdrawal
                    row['Power_Generation_SW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(thermo_electric_surf_withdrawal)

                    public_supply_surf_withdrawal = get_group_sum_value(group_sum,
                                                                        'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source == "Surface Water"')
                    row['Public_Supply_SW'] = public_supply_surf_withdrawal
                    row['Public_Supply_SW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(public_supply_surf_withdrawal)

                    # Sum surface water
                    row['Total_SW_Use_(MGD)'] = irrigation_surf_withdrawal + industrial_surf_withdrawal + \
                                                thermo_electric_surf_withdrawal + public_supply_surf_withdrawal
                    row['Total_SW_Use_(Acres.Feet/Year)'] = row['Irrigation_SW_(Acres.Feet/Year)'] + \
                                                            row['Industrial_SW_(Acres.Feet/Year)'] + \
                                                            row['Power_Generation_SW_(Acres.Feet/Year)'] + \
                                                            row['Public_Supply_SW_(Acres.Feet/Year)']

                    # Groundwater
                    irrigation_gw_withdrawal = get_group_sum_value(group_sum,
                                                                   'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source == "Groundwater"')
                    row['Irrigation_GW'] = irrigation_gw_withdrawal
                    row['Irrigation_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(irrigation_gw_withdrawal)

                    industrial_gw_withdrawal = get_group_sum_value(group_sum,
                                                                   'is_consumptive == False and (sector == "Industrial" or sector == "Mining") and water_type != "Any" and water_source == "Groundwater"')
                    row['Industrial_GW'] = industrial_gw_withdrawal
                    row['Industrial_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(industrial_gw_withdrawal)

                    thermo_electric_gw_withdrawal = get_group_sum_value(group_sum,
                                                                        'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source == "Groundwater"')
                    row['Power_Generation_GW'] = thermo_electric_gw_withdrawal
                    row['Power_Generation_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(thermo_electric_gw_withdrawal)

                    public_supply_gw_withdrawal = get_group_sum_value(group_sum,
                                                                     'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source == "Groundwater"')
                    row['Public_Supply_GW'] = public_supply_gw_withdrawal
                    row['Public_Supply_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(public_supply_gw_withdrawal)

                    livestock_gw_withdrawal = get_group_sum_value(group_sum,
                                                                  'is_consumptive == False and sector == "Livestock" and water_type != "Any" and water_source == "Groundwater"')
                    row['Livestock_GW'] = livestock_gw_withdrawal
                    row['Livestock_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(livestock_gw_withdrawal)

                    rural_domestic_gw_withdrawal = get_group_sum_value(group_sum,
                                                                       'is_consumptive == False and sector == "Domestic" and water_type != "Any" and water_source == "Groundwater"')
                    row['Rural_Domestic_GW'] = rural_domestic_gw_withdrawal
                    row['Rural_Domestic_GW_(Acres.Feet/Year)'] = mgd_to_acre_ft_per_year(rural_domestic_gw_withdrawal)

                    # Sum groundwater
                    row['Total_GW_Use_(MGD)'] = irrigation_gw_withdrawal + industrial_gw_withdrawal + \
                                                thermo_electric_gw_withdrawal + public_supply_gw_withdrawal + \
                                                livestock_gw_withdrawal + rural_domestic_gw_withdrawal
                    row['Total_GW_Use_(Acres.Feet/Year)'] = row['Irrigation_GW_(Acres.Feet/Year)'] + \
                                                            row['Industrial_GW_(Acres.Feet/Year)'] + \
                                                            row['Power_Generation_GW_(Acres.Feet/Year)'] + \
                                                            row['Public_Supply_GW_(Acres.Feet/Year)'] + \
                                                            row['Livestock_GW_(Acres.Feet/Year)'] + \
                                                            row['Rural_Domestic_GW_(Acres.Feet/Year)']

                    # Total and calculate balance and stress
                    row['Withdrawal'] = row['Total_SW_Use_(Acres.Feet/Year)'] + row['Total_GW_Use_(Acres.Feet/Year)']
                    row['Available'] = row['SW-NHDPLUS_(Acres.Feet/Year)'] + row['GW-USGS_(Acres.Feet/Year)']
                    if 'wassi_sector_All_source_All' in h12_wassi:
                        row['Stress'] = h12_wassi['wassi_sector_All_source_All']
                    else:
                        row['Stress'] = 0.0
                    row['Balance'] = row['Available'] - row['Withdrawal']
                    if 'wassi_sector_All_source_SurfaceWater' in h12_wassi:
                        row['SW_Stress'] = h12_wassi['wassi_sector_All_source_SurfaceWater']
                    else:
                        row['SW_Stress'] = 0.0

                    writer.writerow(row)

    except KeyError as ke:
        logger.error(traceback.format_exc())
        logger.error(f"Datum was: {h12}")
        error = True
        sys.exit(ke)
    except CarmaItemNotFound as cinf:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(cinf)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        elif temp_out:
            shutil.rmtree(temp_out)
