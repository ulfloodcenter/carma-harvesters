import json
import re
from datetime import datetime
from typing import List, Callable

from shapely.geometry.base import BaseGeometry

import pandas as pd

from carma_schema import types
from carma_harvesters.util import select_points_contained_by_geometry


YEAR_COMPLETED_ATTR = 'yearCompleted'
CURR_CENTURY = 2000


def _generate_four_digit_year(year: str) -> int:
    current_year = datetime.now().year
    current_year = current_year - CURR_CENTURY
    try:
        year_int = int(year)
        if year_int < 100:
            if year_int > current_year:
                # Assume year is in the 20th century
                year_int += 1900
            else:
                # Assume year is in the 21st century
                year_int += 2000
        return year_int
    except ValueError:
        return None


class WellAttributeMapper:
    def __init__(self, mapper_config_path: str, wells_inpath: str,
                 get_wells: Callable[[str, BaseGeometry], dict] = select_points_contained_by_geometry):
        self.wells_inpath = wells_inpath
        self.get_wells = get_wells
        with open(mapper_config_path, 'r') as f:
            self.config = json.load(f)

    def map_well_attributes(self, well_properties: dict) -> dict:
        """
        Map from native well attributes to CARMA-compliant attributes
        :param well_properties: Properties for a feature of a GeoJSON-like Python geo interface feature collection
        :return:
        """
        mapped_value = {}
        for carma_property, native_property in self.config['attributes'].items():
            carma_value = None
            native_value = well_properties[native_property]
            if native_value is None:
                continue
            if carma_property == YEAR_COMPLETED_ATTR:
                # Value entry will be a list of patterns
                for mapping in self.config['values'][carma_property][native_property]:
                    if isinstance(mapping, dict):
                        if native_value in mapping:
                            carma_value = _generate_four_digit_year(mapping[native_value])
                            break
                    elif isinstance(mapping, str):
                        if isinstance(native_value, float):
                            carma_value = _generate_four_digit_year(str(int(native_value)))
                            break
                        elif isinstance(native_value, str):
                            m = re.match(mapping, native_value)
                            if m:
                                carma_value = _generate_four_digit_year(m.group('year'))
                                break
            else:
                # Value entry will be dictionary whose keys are patterns to be used to attempt to classify inputs into
                # a valid CARMA, which is specified by the value of the key. Try to match one of these patterns
                value_mapping = self.config['values'][carma_property][native_property]
                for pattern, tmp_carma_value in value_mapping.items():
                    m = re.match(pattern, native_value)
                    if m:
                        carma_value = tmp_carma_value
                        break

            if carma_value:
                mapped_value[carma_property] = carma_value

        return mapped_value

    def count_wells_in_geography(self, geom: BaseGeometry, year_completed: int) -> List[dict]:
        well_counts = []

        # Read well data from data file
        well_data = pd.DataFrame(columns=('sector', 'status', 'yearCompleted'))
        wells = self.get_wells(self.wells_inpath, geom)
        for i, well in enumerate(wells['features']):
            carma_attr = self.map_well_attributes(well['properties'])
            well_data = well_data.append(carma_attr, ignore_index=True)

        # Count wells by sector and status
        for sector in types.WELL_SECTORS:
            for status in types.WELL_STATUS:
                wells_in_sector_status = \
                    well_data.query(f"sector=='{sector}' and status=='{status}' and yearCompleted<={year_completed}")
                num_wells = len(wells_in_sector_status)
                if num_wells > 0:
                    well_counts.append(
                        {'sector': sector,
                         'status': status,
                         'yearCompleted': year_completed,
                         'count': num_wells}
                    )

        return well_counts
