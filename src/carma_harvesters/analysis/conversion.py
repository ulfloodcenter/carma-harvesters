
# SECONDS_PER_DAY = 60 * 60 * 24
SECONDS_PER_DAY = 86400
# DAYS_PER_YEAR_INV = 1 / 365
DAYS_PER_YEAR_INV = 0.002739726027397

GALLONS_PER_FT3 = 7.480543
GALLONS_PER_M3 = 264.172052

# MILLION_INV = 1 / (1000 * 1000)
MILLION_INV = 0.000001
# BILLION = 1000 * 1000 * 1000
BILLION = 1000000000


def cfs_to_mgd(value_cfs: float) -> float:
    return value_cfs * SECONDS_PER_DAY * GALLONS_PER_FT3 * MILLION_INV


def mm_per_km2_per_yr_to_mgd(value_mm: float, geom_area_km2: float) -> float:
    return value_mm * MILLION_INV * geom_area_km2 * BILLION * GALLONS_PER_M3 * MILLION_INV * DAYS_PER_YEAR_INV
