import os
import pkg_resources
from typing import List
import logging

import pandas as pd

from carma_schema.types import PowerPlantDataset
from carma_schema.types import ConsumptionOrWithdrawalDatum

from carma_harvesters.usgs.nwis_water_use import NWIS_TO_CARMA_ATTR


logger = logging.getLogger(__name__)

CARMA_HARVESTERS_RSRC_KEY = 'carma_harvesters'
USGS_POWERPLANT_WATER_USE_2010_PATH = 'data/sir20145184_Appendix_1_UPDATED_20141107.xlsx'
USGS_2010_EIA_PLANT_CODE_KEY = 'PLANT CODE'
USGS_2010_WATER_SOURCE_KEY = 'USGS WATER SOURCE CODE'
USGS_2010_WATER_TYPE_KEY = 'USGS WATER TYPE CODE'
USGS_2010_WITHDRAWAL_KEY = 'USGS-Estimated Annual Withdrawal (Mgal/d)'
# Yes, there is a space in the Excel column heading for consumption
USGS_2010_CONSUMPTION_KEY = ' USGS-Estimated Annual Consumption (Mgal/d)'

USGS_POWERPLANT_WATER_USE_2015_PATH = 'data/2015_TE_Model_Estimates.xlsx'
USGS_2015_EIA_PLANT_CODE_KEY = 'EIA_PLANT_ID'
USGS_2015_WATER_SOURCE_KEY = 'WATER_SOURCE_CODE'
USGS_2015_WATER_TYPE_KEY = 'WATER_TYPE_CODE'
USGS_2015_WITHDRAWAL_KEY = 'WITHDRAWAL'
USGS_2015_CONSUMPTION_KEY = 'CONSUMPTION'

USGS_POWER_PLANT_DATA_SRC_URLS = {2010: 'https://pubs.er.usgs.gov/publication/sir20145184',
                                  2015: 'https://pubs.er.usgs.gov/publication/sir20195103'}
USGS_POWER_PLANT_WATER_USE_UNIT = {
  "name": "Mgal/d",
  "primaryDimension": "Million",
  "secondaryDimension": "Gallon",
  "tertiaryDimension": "Day"
}
USGS_POWER_PLANT_FACILITIES_UNIT = {
    "name": "",
    "primaryDimension": "One"
}

USGS_THERMO_POWER_WATER_SOURCE_MAP = {
    'Surface Water': 'surface-water',
    'Groundwater': 'groundwater'
}
USGS_THERMO_POWER_WATER_TYPE_MAP = {
    'Fresh': 'fresh',
    'Saline': 'saline'
}

USGS_THERMO_POWER_CONSUMPTION_DESC_TEMPLATE = "Total Thermoelectric Power consumptive use, {water_type}, in Mgal/d"
USGS_THERMA_POWER_CONSUMPTION_DESC_ALL = "Total Thermoelectric Power total consumptive use, in Mgal/d"
USGS_THERMO_POWER_WITHDRAWAL_DESC_TEMPLATE = "Total Thermoelectric Power self-supplied {water_source} withdrawals, {water_type}, in Mgal/d"
USGS_THERMO_POWER_WITHDRAWAL_SUMMARY = "Total Thermoelectric Power total self-supplied withdrawals, {summary}, in Mgal/d"
USGS_THERMO_POWER_WITHDRAWAL_TOTAL = "Total Thermoelectric Power total self-supplied withdrawals, total, in Mgal/d"
USGS_THERMO_POWER_FACILITIES = "Total Thermoelectric Power number of facilities"

def get_consumption_label(water_type: str) -> str:
    if water_type == 'Any':
        return USGS_THERMA_POWER_CONSUMPTION_DESC_ALL
    return USGS_THERMO_POWER_CONSUMPTION_DESC_TEMPLATE.format(
        water_type=USGS_THERMO_POWER_WATER_TYPE_MAP[water_type]
    )


def get_withdrawal_label(water_source: str = None, water_type: str = None) -> str:
    if water_source and water_type:
        return USGS_THERMO_POWER_WITHDRAWAL_DESC_TEMPLATE.format(
            water_source=USGS_THERMO_POWER_WATER_SOURCE_MAP[water_source],
            water_type=USGS_THERMO_POWER_WATER_TYPE_MAP[water_type]
        )
    elif water_source:
        return USGS_THERMO_POWER_WITHDRAWAL_SUMMARY.format(
            summary=USGS_THERMO_POWER_WATER_SOURCE_MAP[water_source]
        )
    elif water_type:
        return USGS_THERMO_POWER_WITHDRAWAL_SUMMARY.format(
            summary=USGS_THERMO_POWER_WATER_TYPE_MAP[water_type]
        )
    else:
        return USGS_THERMO_POWER_WITHDRAWAL_TOTAL


class USGSPowerPlantWaterUse:
    def __init__(self):
        self.water_use_2010_path = pkg_resources.resource_filename(CARMA_HARVESTERS_RSRC_KEY,
                                                                   USGS_POWERPLANT_WATER_USE_2010_PATH)
        self.water_use_2015_path = pkg_resources.resource_filename(CARMA_HARVESTERS_RSRC_KEY,
                                                                   USGS_POWERPLANT_WATER_USE_2015_PATH)

        if not os.path.exists(self.water_use_2010_path) or not os.access(self.water_use_2010_path, os.R_OK):
            raise Exception("USGS Withdrawal and Consumption of Water by Thermoelectric Power Plants in the United States, 2010 data file cannot be found or cannot be read.")
        logger.debug(f"Plant location input path: {self.water_use_2010_path}")

        if not os.path.exists(self.water_use_2015_path) or not os.access(self.water_use_2015_path, os.R_OK):
            raise Exception("USGS Withdrawal and Consumption of Water by Thermoelectric Power Plants in the United States, 2015 data file cannot be found or cannot be read.")
        logger.debug(f"Plant location input path: {self.water_use_2015_path}")

    def get_huc12_powerplant_water_use(self, huc12: str,
                                       plants_in_huc12: List[PowerPlantDataset]) -> List[PowerPlantDataset]:
        plants = []
        # Take a list of PowerPlantDataset instances with only plant_id and geometry and
        #  return a list of PowerPlantDataset entities with all data supplied. Only power plants in
        #  the water use dataset will be in the list of returned entities
        u2010 = pd.read_excel(io=self.water_use_2010_path, header=3, usecols='A,H,I,K,L')
        u2015 = pd.read_excel(io=self.water_use_2015_path, header=0, usecols='A,H,I,J,K')

        # Get a list of the EIA power plant IDs
        huc12_plant_ids = [p.eiaPlantCode for p in plants_in_huc12]
        # Filter USGS data based on list of power plants (likely taken from EIA location data)
        # plants in plants_in_ids but not in the USGS power plant water use data will be ignored,
        # which is fine because only a subset of the EIA plants are in the USGS data
        u2010 = u2010.query("`PLANT CODE` in @huc12_plant_ids")
        u2015 = u2015.query("EIA_PLANT_ID in @huc12_plant_ids")

        # Now iterate over plants_in, filling in water use data for 2010 and 2015
        for p in plants_in_huc12:
            data_2010 = u2010[u2010['PLANT CODE'] == p.eiaPlantCode]
            data_2015 = u2015[u2015['EIA_PLANT_ID'] == p.eiaPlantCode]
            # Update values in p and add to list (first refactor data model to make water
            # source and type unique for each year.
            consumption_data = []
            withdrawal_data = []
            # Get 2010 water use data
            if len(data_2010) > 0:
                # Take the first value if there are more than one
                wu = data_2010.iloc[0]
                water_source = wu[USGS_2010_WATER_SOURCE_KEY]
                water_type = wu[USGS_2010_WATER_TYPE_KEY]
                consumption_data.append(
                    ConsumptionOrWithdrawalDatum(2010,
                                                 wu[USGS_2010_CONSUMPTION_KEY],
                                                 water_source,
                                                 water_type)
                )
                withdrawal_data.append(
                    ConsumptionOrWithdrawalDatum(2010,
                                                 wu[USGS_2010_WITHDRAWAL_KEY],
                                                 water_source,
                                                 water_type)
                )
            # Get 2015 water use data
            if len(data_2015) > 0:
                # Take the first value if there are more than one
                wu = data_2015.iloc[0]
                water_source = wu[USGS_2015_WATER_SOURCE_KEY]
                water_type = wu[USGS_2015_WATER_TYPE_KEY]
                consumption_data.append(
                    ConsumptionOrWithdrawalDatum(2015,
                                                 wu[USGS_2015_CONSUMPTION_KEY],
                                                 water_source,
                                                 water_type)
                )
                withdrawal_data.append(
                    ConsumptionOrWithdrawalDatum(2015,
                                                 wu[USGS_2015_WITHDRAWAL_KEY],
                                                 water_source,
                                                 water_type)
                )

            # Update PowerPlantDataset with USGS water use data (if present)
            if len(consumption_data) > 0 or len(withdrawal_data) > 0:
                p.huc12 = huc12
                p.usgsConsumption = consumption_data
                p.usgsWithdrawal = withdrawal_data
                plants.append(p)

        return plants


def summarize_powerplant_data_by_huc12(power_plant_datasets: List[dict]) -> List[dict]:
    # First, make a Pandas dataframe, loop over power plants by HUC12, add them to the dataframe
    plants = pd.DataFrame(columns=['year', 'plant_id', 'huc12', 'data_type', 'water_source', 'water_type', 'value'])
    for plant in power_plant_datasets:
        huc12 = plant['huc12']
        # consumption
        cons = plant['usgsConsumption']
        for c in cons:
            # For now, take first water source and type
            plants = plants.append({'year': c['year'], 'plant_id': plant['eiaPlantCode'], 'huc12': huc12,
                                    'data_type': 'consumption',
                                    'water_source': c['waterSource'][0],
                                    'water_type': c['waterType'][0],
                                    'value': c['value']},
                                   ignore_index=True)
        # withdrawal
        withdrawal = plant['usgsWithdrawal']
        for w in withdrawal:
            # For now, take first water source and type
            plants = plants.append({'year': w['year'], 'plant_id': plant['eiaPlantCode'], 'huc12': huc12,
                                    'data_type': 'withdrawal',
                                    'water_source': w['waterSource'][0],
                                    'water_type': w['waterType'][0],
                                    'value': w['value']},
                                   ignore_index=True)

    # Now summarize powerplant water use data by various aspects
    water_use_objects = []
    huc12s = plants['huc12'].unique()
    years = plants['year'].unique()
    for h in huc12s:
        # Count the number of plants
        huc12_data = plants.query('huc12 == @h')
        for year in years:
            num_plants = len(huc12_data.query(
                'year == @year')['plant_id'].unique())
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Facility',
                NWIS_TO_CARMA_ATTR['water_source']: 'N/A',
                NWIS_TO_CARMA_ATTR['water_type']: 'N/A',
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: 'Total Thermoelectric Power number of facilities',
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': num_plants,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_FACILITIES_UNIT
            }
            water_use_objects.append(datum)

        # Get consumption data by year and water type
        huc12_cons = plants.query('huc12 == @h and data_type == "consumption"')
        grouped = huc12_cons.groupby(['year', 'water_source', 'water_type'])
        group_sum = grouped.sum()
        for year in years:
            val = group_sum.query(
                'year == @year')['value']
            if len(val) == 0:
                continue
            consumption = val.iloc[0]
            water_source = 'All'
            water_type = val.index[0][2]
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_consumption_label(water_type),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': consumption,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get consumption data by year for all water types
        grouped = huc12_cons.groupby(['year'])
        group_sum = grouped.sum()
        for year in years:
            val = group_sum.query(
                'year == @year')['value']
            if len(val) == 0:
                continue
            consumption = val.iloc[0]
            water_source = 'All'
            water_type = 'Any'
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_consumption_label(water_type),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': consumption,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year, water source, and type
        huc12_withd = plants.query('huc12 == @h and data_type == "withdrawal"')
        grouped = huc12_withd.groupby(['year', 'data_type', 'water_source', 'water_type'])
        group_sum = grouped.sum()
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = val.index[0][2]
            water_type = val.index[0][3]
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(water_source,
                                                                        water_type),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year for surface-water
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal" and water_source == "Surface Water"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = val.index[0][2]
            water_type = 'Any'
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(water_source=water_source),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year for groundwater
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal" and water_source == "Groundwater"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = val.index[0][2]
            water_type = 'Any'
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(water_source=water_source),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year for freshwater
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal" and water_type == "Fresh"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = 'All'
            water_type = val.index[0][3]
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(water_type=water_type),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year for saline
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal" and water_type == "Saline"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = 'All'
            water_type = val.index[0][3]
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(water_type=water_type),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

        # Get withdrawal data by year
        grouped = huc12_withd.groupby(['year', 'data_type'])
        group_sum = grouped.sum()
        for year in years:
            val = group_sum.query(
                'year == @year and data_type == "withdrawal"')['value']
            if len(val) == 0:
                continue
            withdrawal = val.iloc[0]
            water_source = 'All'
            water_type = 'Any'
            datum = {
                'huc12': h,
                NWIS_TO_CARMA_ATTR['entity_type']: 'Water',
                NWIS_TO_CARMA_ATTR['water_source']: water_source,
                NWIS_TO_CARMA_ATTR['water_type']: water_type,
                NWIS_TO_CARMA_ATTR['sector']: 'Total Thermoelectric Power',
                NWIS_TO_CARMA_ATTR['description']: get_withdrawal_label(),
                'sourceData': USGS_POWER_PLANT_DATA_SRC_URLS[year],
                'year': year,
                'value': withdrawal,
                NWIS_TO_CARMA_ATTR['unit']: USGS_POWER_PLANT_WATER_USE_UNIT
            }
            water_use_objects.append(datum)

    return water_use_objects
