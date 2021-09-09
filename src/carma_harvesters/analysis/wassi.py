from typing import List, Set
import copy
from uuid import UUID
from dataclasses import dataclass
import logging

from carma_schema.types import AnalysisWaSSI, WaterUseDataset, CountyDisaggregationWaSSI,\
    WassiValue, \
    WASSI_SECTOR_ALL, WASSI_SECTOR_IRR, WASSI_SECTOR_IND, WASSI_SECTOR_PUB, WASSI_SECTOR_PWR, WASSI_SECTOR_DOM,\
    WASSI_SECTOR_LVS, WASSI_SOURCE_ALL, WASSI_SOURCE_SURF, WASSI_SOURCE_GW
from carma_schema import CarmaItemNotFound
from carma_schema import get_wassi_analysis_by_id, update_wassi_analysis_instance

from carma_harvesters.common import get_huc12_wateruse_data, get_group_sum_value
from carma_harvesters.analysis.conversion import cfs_to_mgd, mm_per_km2_per_yr_to_mgd


logger = logging.getLogger(__name__)

SECTOR_VALUE_TO_PROPERTY_NAME = {
    'Public Supply': 'publicSupply',
    'Domestic': 'domestic',
    'Commercial': 'commercial',
    'Industrial': 'industrial',
    'Power Generation': 'powerGeneration',
    'Irrigation': 'irrigation',
    'Livestock': 'livestock',
    'Mining': 'mining'
}

GW_WEIGHT_KEY = 'gw1'


@dataclass
class HUC12Weight:
    huc12: str
    weight: float


@dataclass
class WeightDescriptor:
    county: str
    source: str
    sector: str
    huc12_weights: List[HUC12Weight]
    sum_weights: float


@dataclass
class SourceSector:
    source: str
    sector: str


def get_weight_descriptor_key(county: str, source: str, sector: str) -> str:
    return county + ':' + source + ':' + sector


def enumerate_source_sectors(wassi: AnalysisWaSSI) -> List[SourceSector]:
    source_sectors = []
    for sector_weights in wassi.sectorWeightFactorsSurface:
        source_sectors.append(SourceSector(WASSI_SOURCE_SURF, sector_weights.sector))
    for sector_weights in wassi.sectorWeightFactorsGroundwater:
        source_sectors.append(SourceSector(WASSI_SOURCE_GW, sector_weights.sector))
    return source_sectors


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


def calculate_wassi_for_huc12_watersheds(abs_carma_inpath: str, document: dict, wassi_id: UUID,
                                         env_flow=0.5,
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
        huc12_id = huc12['id']
        if 'meanAnnualFlow' not in huc12:
            logger.warning(f"HUC12 {huc12_id} does not have meanAnnualFlow data, so WaSSI cannot be calculated.")
            continue
        mean_annual_flow_mgd = cfs_to_mgd(huc12['meanAnnualFlow'])
        if 'recharge' not in huc12:
            logger.warning(f"HUC12 {huc12_id} does not have recharge data, so WaSSI cannot be calculated.")
            continue
        recharge_mgd = mm_per_km2_per_yr_to_mgd(huc12['recharge'], huc12['area'])
        huc_wu = get_huc12_wateruse_data(document, huc12_id, wassi.waterUseYear)
        total_gw_withdrawal = huc_wu.query('is_consumptive == False and water_type != "Any" and water_source == "Groundwater"').sum()['value']
        total_surf_withdrawal = huc_wu.query('is_consumptive == False and water_type != "Any" and water_source == "Surface Water"').sum()['value']
        total_withdrawal = total_gw_withdrawal + total_surf_withdrawal
        grouped = huc_wu.groupby(['sector', 'is_consumptive', 'water_source', 'water_type'])
        group_sum = grouped.sum()
        domestic_withdrawal = get_group_sum_value(group_sum, 'is_consumptive == False and sector == "Domestic" and water_type != "Any" and water_source != "All"')
        domestic_surf_withdrawal = get_group_sum_value(group_sum,
                                                        'is_consumptive == False and sector == "Domestic" and water_type != "Any" and water_source == "Surface Water"')
        industrial_withdrawal = get_group_sum_value(group_sum, 'is_consumptive == False and (sector == "Industrial" or sector == "Mining") and water_type != "Any" and water_source != "All"')
        industrial_surf_withdrawal = get_group_sum_value(group_sum,
                                                         'is_consumptive == False and (sector == "Industrial" or sector == "Mining") and water_type != "Any" and water_source == "Surface Water"')
        irrigation_withdrawal = get_group_sum_value(group_sum, 'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source != "All"')
        irrigation_surf_withdrawal = get_group_sum_value(group_sum,
                                                         'is_consumptive == False and sector == "Irrigation" and water_type != "Any" and water_source == "Surface Water"')
        public_supply_withdrawal = get_group_sum_value(group_sum, 'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source != "All"')
        public_supply_surf_withdrawal = get_group_sum_value(group_sum,
                                                             'is_consumptive == False and sector == "Public Supply" and water_type != "Any" and water_source == "Surface Water"')
        thermo_electric_withdrawal = get_group_sum_value(group_sum, 'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source != "All"')
        thermo_electric_surf_withdrawal = get_group_sum_value(group_sum,
                                                               'is_consumptive == False and sector == "Total Thermoelectric Power" and water_type != "Any" and water_source == "Surface Water"')
        livestock_withdrawal = get_group_sum_value(group_sum,
                                                   'is_consumptive == False and sector == "Livestock" and water_type != "Any" and water_source != "All"')
        livestock_surf_withdrawal = get_group_sum_value(group_sum,
                                                        'is_consumptive == False and sector == "Livestock" and water_type != "Any" and water_source == "Surface Water"')

        # Calculate various WaSSI values and store in WassiValue objects
        env_flow_scalar = (1 - env_flow)
        # Main WaSSI
        total_wassi = total_withdrawal / (
                (env_flow_scalar * (mean_annual_flow_mgd + total_surf_withdrawal)) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_ALL,
                       WASSI_SOURCE_ALL,
                       total_wassi)
        )
        # Surface water vs. groundwater stress
        # Surface WaSSI: Eliminate GW demand and availability
        surface_wassi = total_surf_withdrawal / (env_flow_scalar * (mean_annual_flow_mgd + total_surf_withdrawal))
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_ALL,
                       WASSI_SOURCE_SURF,
                       surface_wassi)
        )
        # GW WaSSI: Eliminate surface demand and availability
        gw_wassi = total_gw_withdrawal / recharge_mgd
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_ALL,
                       WASSI_SOURCE_GW,
                       gw_wassi)
        )
        # Irrigation WaSSI
        irrigation_wassi = irrigation_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + irrigation_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_IRR,
                       WASSI_SOURCE_ALL,
                       irrigation_wassi)
        )
        # Industrial WaSSI
        industrial_wassi = industrial_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + industrial_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_IND,
                       WASSI_SOURCE_ALL,
                       industrial_wassi)
        )
        # Public supply WaSSI
        public_supply_wassi = public_supply_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + public_supply_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_PUB,
                       WASSI_SOURCE_ALL,
                       public_supply_wassi)
        )
        # Thermoelectric generation WaSSI
        thermo_electric_wassi = thermo_electric_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + thermo_electric_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_PWR,
                       WASSI_SOURCE_ALL,
                       thermo_electric_wassi)
        )
        # Domestic WaSSI
        domestic_wassi = domestic_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + domestic_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_DOM,
                       WASSI_SOURCE_ALL,
                       domestic_wassi)
        )
        # Livestock WaSSI
        livestock_wassi = livestock_withdrawal / (
                env_flow_scalar * (mean_annual_flow_mgd + livestock_surf_withdrawal) + recharge_mgd)
        wassi_values.append(
            WassiValue(huc12_id,
                       WASSI_SECTOR_LVS,
                       WASSI_SOURCE_ALL,
                       livestock_wassi)
        )

    # Write WaSSI values to AnalysisWaSSI object
    if overwrite or wassi.wassiValues is None:
        wassi.wassiValues = wassi_values
    else:
        wassi.wassiValues = wassi.wassiValues + wassi_values

    update_wassi_analysis_instance(document, wassi)


def get_county_ids_in_county_disaggregations(wassi: AnalysisWaSSI) -> Set[str]:
    county_ids = set()
    for cd in wassi.countyDisaggregations:
        county_ids.add(cd.county)
    return county_ids


def get_county_disaggregations_for_county(wassi: AnalysisWaSSI, county: str) -> List[CountyDisaggregationWaSSI]:
    disags = []
    for cd in wassi.countyDisaggregations:
        if cd.county == county:
            disags.append(cd)
    return disags
