import os
import pkg_resources
from typing import List
import logging

import pandas as pd

from carma_schema.types import PowerPlantDataset
from carma_schema.types import ConsumptionOrWithdrawalDatum

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
