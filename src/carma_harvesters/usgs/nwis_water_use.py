import tempfile
from typing import Set

import requests

import pandas as pd


VALID_YEARS = [1985, 1990, 1995, 2000, 2005, 2010, 2015]

STATE_FIPS_TO_ABBREV = {
    '01': 'al',
    '02': 'ak',
    '04': 'az',
    '05': 'ar',
    '06': 'ca',
    '08': 'co',
    '09': 'ct',
    '10': 'de',
    '11': 'dc',
    '12': 'fl',
    '13': 'ga',
    '15': 'hi',
    '16': 'id',
    '17': 'il',
    '18': 'in',
    '19': 'ia',
    '20': 'ks',
    '21': 'ky',
    '22': 'la',
    '23': 'me',
    '24': 'md',
    '25': 'ma',
    '26': 'mi',
    '27': 'mn',
    '28': 'ms',
    '29': 'mo',
    '30': 'mt',
    '31': 'ne',
    '32': 'nv',
    '33': 'nh',
    '34': 'nj',
    '35': 'nm',
    '36': 'ny',
    '37': 'nc',
    '38': 'nd',
    '39': 'oh',
    '40': 'ok',
    '41': 'or',
    '42': 'pa',
    '44': 'ri',
    '45': 'sc',
    '46': 'sd',
    '47': 'tn',
    '48': 'tx',
    '49': 'ut',
    '50': 'vt',
    '51': 'va',
    '53': 'wa',
    '54': 'wv',
    '55': 'wi',
    '56': 'wy',
}

URL_PROTO = "https://waterdata.usgs.gov/{state_abbrev}/nwis/water_use?format=rdb&rdb_compression=file&wu_area=County&wu_year={year}&wu_county={county_fips}"


def download_water_use_data(year: int, state_fips: str, county_fips: Set[str], out_path: str) -> str:
    """
    Download USGS NWIS water use data for a single county in a single state for a single year.
    :param year: Year of data to download. Must be one of VALID_YEARS.
    :param state_fips: FIPS code of state to download data for. Must a key in STATE_FIPS_TO_ABBREV.
    :param county_fips: Set of one or more FIPS codes of the counties to download data for.
    :param out_path: Path in which downloaded data file should be stored.
    :return: Absolute path of the file containing the downloaded data.
    """
    if year not in VALID_YEARS:
        raise ValueError(f"Year {year} is not among valid years {VALID_YEARS}")
    if state_fips not in STATE_FIPS_TO_ABBREV:
        raise ValueError(f"State FIPS code {state_fips} is not valid.")

    state_abbrev = STATE_FIPS_TO_ABBREV[state_fips]

    county_fips_arg = ','.join(county_fips)

    # Create file to store data in
    f = tempfile.NamedTemporaryFile(dir=out_path, prefix=f"nwis_water_use_data_{state_abbrev}", suffix='.csv',
                                    delete=False)
    out_file_name = f.name

    # Query NWIS water use data using requests
    url = URL_PROTO.format(state_abbrev=state_abbrev, year=year, county_fips=county_fips_arg)
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Exception(f"Error: Response code {r.status_code} when downloading water use data from {url}.")
    for chunk in r.iter_content(chunk_size=4096):
        f.write(chunk)
    f.close()

    # Return absolute path of file containing downloaded data
    return out_file_name


def read_water_use_data(input_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv_path, sep='\t', comment='#', skiprows=1)
    # Remove first row, which contains field widths for some reason even though
    # the file is tab delimited
    df = df.drop(0)
    return df
