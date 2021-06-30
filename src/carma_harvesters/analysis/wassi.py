from typing import List
import copy
from uuid import UUID
import logging

import pandas as pd

from carma_schema.types import AnalysisWaSSI, WaterUseDataset
from carma_schema import CarmaItemNotFound
from carma_schema import get_water_use_data_for_huc12, get_wassi_analysis_by_id

from carma_harvesters.common import almost_equal
from carma_harvesters.analysis.conversion import cfs_to_mgd, mm_per_km2_per_yr_to_mgd


logger = logging.getLogger(__name__)

SECTOR_VALUE_TO_PROPERTY_NAME = {
    'Public Supply': 'publicSupply',
    'Domestic': 'domestic',
    'Commercial': 'commercial',
    'Industrial': 'industrial',
    'Power Generation': 'powerGeneration',
    'Irrigation': 'irrigation',
    'Livestock': 'livestock'
}

GW_WEIGHT_KEY = 'gw1'


def get_sector_weights(wassi: AnalysisWaSSI, source: str, sector: str) -> List[str]:
    weights = []
    if source == 'Surface Water':
        for sector_weights in wassi.sectorWeightFactorsSurface:
            if sector_weights.sector == sector:
                weights.extend(sector_weights.factors)
                break
    elif source == 'Groundwater':
        for sector_weights in wassi.sectorWeightFactorsGroundwater:
            if sector_weights.sector == sector:
                weights.extend(sector_weights.factors)
                break

    return weights


def convert_county_wateruse_data_to_huc(county_wu: WaterUseDataset, huc_id, scalar=1.0) -> WaterUseDataset:
    huc_wud = copy.deepcopy(county_wu)
    huc_wud.county = None
    huc_wud.huc12 = huc_id
    huc_wud.value *= scalar
    return huc_wud


def _get_group_sum_value(group_sum: pd.DataFrame, query: str, value_field='value') -> float:
    sum_val = group_sum.query(query)
    if len(sum_val) == 1:
        return float(sum_val[value_field][0])
    else:
        return 0.0


def calculate_wassi_for_huc12_watersheds(abs_carma_inpath: str, document: dict, wassi_id: UUID,
                                         overwrite=False):
    if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
        raise CarmaItemNotFound(f"No HUC12 watersheds defined in {abs_carma_inpath}")

    if 'WaterUseDatasets' not in document or len(document['WaterUseDatasets']) < 1:
        raise CarmaItemNotFound(f"No water use data defined in {abs_carma_inpath}")

    # Find WaSSI analysis specified by wassi_id
    wassi = get_wassi_analysis_by_id(document, wassi_id)
    if wassi is None:
        raise CarmaItemNotFound(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

    wassi_values = []

    for huc12 in document['HUC12Watersheds']:
        if 'meanAnnualFlow' not in huc12:
            logger.warning(f"HUC12 {huc12['id']} does not have meanAnnualFlow data, so WaSSI cannot be calculated.")
            continue
        mean_annual_flow_mgd = cfs_to_mgd(huc12['meanAnnualFlow'])
        if 'recharge' not in huc12:
            logger.warning(f"HUC12 {huc12['id']} does not have recharge data, so WaSSI cannot be calculated.")
            continue
        recharge_mgd = mm_per_km2_per_yr_to_mgd(huc12['recharge'], huc12['area'])
        # TODO: Fetch water use data for this HUC12 and store in Pandas dataframe for analysis
        huc_wu = pd.DataFrame(columns=['water_source', 'sector', 'value'])
        for wud in get_water_use_data_for_huc12(document, huc12['id'], wassi.waterUseYear):
            huc_wu = huc_wu.append({'water_source': wud['waterSource'],
                                   'sector': wud['sector'],
                                   'value': wud['value']},
                                   ignore_index=True)
        # Calculate terms for WaSSI
        total_withdrawal = huc_wu.sum()['value']
        total_no_gw_withdrawal = huc_wu.query('water_source != "Groundwater"').sum()['value']
        total_no_surf_withdrawal = huc_wu.query('water_source != "Surface Water"').sum()['value']
        assert almost_equal(total_withdrawal, total_no_gw_withdrawal + total_no_surf_withdrawal)
        grouped = huc_wu.groupby(['sector'])
        group_sum = grouped.sum()
        domestic_withdrawal = _get_group_sum_value(group_sum, 'sector == "Domestic"')
        industrial_withdrawal = _get_group_sum_value(group_sum, 'sector == "Industrial"')
        irigation_withdrawal = _get_group_sum_value(group_sum, 'sector == "Irrigation"')
        public_supply_withdrawal = _get_group_sum_value(group_sum, 'sector == "Public Supply"')
        thermo_electric_withdrawal = _get_group_sum_value(group_sum, 'sector == "Total Thermoelectric Power"')

        # TODO: Calculate various WaSSI values and store in WassiValue objects


    # TODO: Write WaSSI values to AnalysisWaSSI object
    if overwrite or wassi.wassiValues is None:
        wassi.wassiValues = wassi_values
    else:
        wassi.wassiValues = wassi.wassiValues + wassi_values
