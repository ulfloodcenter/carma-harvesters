from typing import List
import copy

from carma_schema.types import AnalysisWaSSI, WaterUseDataset


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
