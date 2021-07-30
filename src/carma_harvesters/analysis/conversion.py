
# SECONDS_PER_DAY = 60 * 60 * 24
SECONDS_PER_DAY = 86400
# DAYS_PER_YEAR_INV = 1 / 365.25
DAYS_PER_YEAR_INV = 0.002737850787132

GALLONS_PER_FT3 = 7.480543
GALLONS_PER_M3 = 264.172052
ACRE_FT_YEAR_PER_CFS = 724.44792344617
ACRE_FT_YEAR_PER_MGD = 1120.8866

# MILLION_INV = 1 / (1000 * 1000)
MILLION_INV = 0.000001
# BILLION = 1000 * 1000 * 1000
BILLION = 1000000000

CFS_TO_MGD_FACTORS = SECONDS_PER_DAY * GALLONS_PER_FT3 * MILLION_INV
MM_PER_KM2_PER_YR_TO_MGD_FACTORS = MILLION_INV * BILLION * GALLONS_PER_M3 * MILLION_INV * DAYS_PER_YEAR_INV


def cfs_to_mgd(value_cfs: float) -> float:
    return value_cfs * CFS_TO_MGD_FACTORS


def mgd_to_acre_ft_per_year(value_mgd: float) -> float:
    return value_mgd * ACRE_FT_YEAR_PER_MGD


def mm_per_km2_per_yr_to_mgd(value_mm: float, geom_area_km2: float) -> float:
    # Expanded conversion factors: return value_mm * MILLION_INV * geom_area_km2 * BILLION * GALLONS_PER_M3 * MILLION_INV * DAYS_PER_YEAR_INV
    return value_mm * geom_area_km2 * MM_PER_KM2_PER_YR_TO_MGD_FACTORS


def mm_per_km2_per_yr_to_acre_ft_per_year(value_mm: float, geom_area_km2: float) -> float:
    return mgd_to_acre_ft_per_year(mm_per_km2_per_yr_to_mgd(value_mm, geom_area_km2))


def km2_to_acre(value_km2: float) -> float:
    return value_km2 * 247.105381


def cfs_to_acre_ft_per_yr(value_cfs: float) -> float:
    return value_cfs * ACRE_FT_YEAR_PER_CFS
