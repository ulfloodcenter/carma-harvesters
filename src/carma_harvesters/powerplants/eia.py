import os
import pkg_resources
import logging

from shapely.geometry.base import BaseGeometry

from ..util import select_points_contained_by_geometry


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

    def get_plants_within_geometry(self, geom: BaseGeometry) -> dict:
        return select_points_contained_by_geometry(self.plant_loc_in_path, geom)
