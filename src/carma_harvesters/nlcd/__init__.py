# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

from typing import Tuple
import logging

import rasterstats


NLCD_HIGHLY_DEVELOPED_DN = 24


logger = logging.getLogger(__name__)


def get_percent_highly_developed_land(zone_features: dict,
                                      nlcd_raster_path: str) -> Tuple[float, float]:
    stats = rasterstats.zonal_stats(zone_features, nlcd_raster_path,
                                    categorical=True)[0]
    logger.debug(f"NLCD zonal stats: {stats}")
    total_nlcd_cells = sum(stats.values())
    # Should this also include NLCD medium-intensity?
    developed_nlcd_cells = stats.get(NLCD_HIGHLY_DEVELOPED_DN, 0.0)
    return developed_nlcd_cells, total_nlcd_cells
