# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import rasterstats


def calculate_huc12_mean_recharge(zone_features: dict,
                                  recharge_raster_path: str) -> float:
    stats = rasterstats.zonal_stats(zone_features,
                                    recharge_raster_path)[0]
    return stats['mean']
