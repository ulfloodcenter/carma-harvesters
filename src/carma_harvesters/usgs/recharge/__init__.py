import rasterstats


def calculate_huc12_mean_recharge(zone_features: dict,
                                  recharge_raster_path: str) -> float:
    stats = rasterstats.zonal_stats(zone_features,
                                    recharge_raster_path)[0]
    return stats['mean']
