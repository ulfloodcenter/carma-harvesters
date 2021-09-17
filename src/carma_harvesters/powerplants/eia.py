# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import os
import pkg_resources
import logging
from typing import List

from shapely.geometry.base import BaseGeometry

from ..util import select_points_contained_by_geometry
from carma_schema.types import PowerPlantDataset


logger = logging.getLogger(__name__)

CARMA_HARVESTERS_RSRC_KEY = 'carma_harvesters'
EIA_FORM_860_SCHEDULE_2_PATH = 'data/2___Plant_Y2019.gpkg'


class PowerPlantLocations:
    def __init__(self):
        self.plant_loc_in_path = pkg_resources.resource_filename(CARMA_HARVESTERS_RSRC_KEY,
                                                                 EIA_FORM_860_SCHEDULE_2_PATH)
        if not os.path.exists(self.plant_loc_in_path) or not os.access(self.plant_loc_in_path, os.R_OK):
            raise Exception("EIA FORM 860 schedule 2 power plant location file cannot be found or cannot be read.")
        logger.debug(f"Plant location input path: {self.plant_loc_in_path}")

    def get_plants_within_geometry(self, geom: BaseGeometry) -> List[PowerPlantDataset]:
        plants = []
        points = select_points_contained_by_geometry(self.plant_loc_in_path, geom)
        if 'features' in points:
            for p in points['features']:
                c = p['geometry']['coordinates']
                plant = PowerPlantDataset(eiaPlantCode=p['properties']['Plant Code'],
                                          eiaLongitude=c[0],
                                          eiaLatitude=c[1])
                plants.append(plant)
        return plants
