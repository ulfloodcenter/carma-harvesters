# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import tempfile
from typing import Set, List
import decimal
import logging

import requests
import pandas as pd

from carma_schema.geoconnex.census import County

from . nwis_water_user_constants import CATEGORY_DESCRIPTORS


logger = logging.getLogger(__name__)


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

NWIS_TO_CARMA_ATTR = {
    'sector': 'sector',
    'entity_type': 'entityType',
    'water_source': 'waterSource',
    'water_type': 'waterType',
    'description': 'description',
    'unit': 'unit'
}

NWIS_EMPTY_VALUE = '-'
ZERO = decimal.Decimal('0.0')

URL_PROTO = "https://waterdata.usgs.gov/{state_abbrev}/nwis/water_use?format=rdb&rdb_compression=file&wu_area=County&wu_year={year}&wu_county={county_fips}"


def download_water_use_data(year: int, state_fips: str, county_fips: Set[str], out_path: str) -> (str, str):
    """
    Download USGS NWIS water use data for a single county in a single state for a single year.
    :param year: Year of data to download. Must be one of VALID_YEARS.
    :param state_fips: FIPS code of state to download data for. Must a key in STATE_FIPS_TO_ABBREV.
    :param county_fips: Set of one or more FIPS codes of the counties to download data for.
    :param out_path: Path in which downloaded data file should be stored.
    :return: Tuple containing: absolute path of the file containing the downloaded data, original URL of data queried.
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
    return out_file_name, url


def read_water_use_data(input_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv_path, sep='\t', comment='#', skiprows=1)
    # Remove first row, which contains field widths for some reason even though
    # the file is tab delimited
    df = df.drop(0)
    return df


def water_use_df_to_carma(water_use_df: pd.DataFrame, url: str, water_use_objects: List):
    for i in range(len(water_use_df)):
        row = water_use_df.iloc[i].to_dict()
        county_id_short = f"{row['state_cd']}{row['county_cd']}"
        county_id = County.generate_fq_id(county_id_short)
        year = int(row['year'])
        for k, cat_desc in CATEGORY_DESCRIPTORS.items():
            try:
                value = row[k]
                if value == NWIS_EMPTY_VALUE:
                    value = ZERO
                else:
                    try:
                        value = decimal.Decimal(value)
                    except decimal.InvalidOperation:
                        logger.warning(f"Unable to convert value {value} to decimal type, using 0.0.")
                        value = ZERO
                datum = {'county': county_id,
                         NWIS_TO_CARMA_ATTR['entity_type']: cat_desc['entity_type'],
                         NWIS_TO_CARMA_ATTR['water_source']: cat_desc['water_source'],
                         NWIS_TO_CARMA_ATTR['water_type']: cat_desc['water_type'],
                         NWIS_TO_CARMA_ATTR['sector']: cat_desc['sector'],
                         NWIS_TO_CARMA_ATTR['description']: cat_desc['description'],
                         'sourceData': url,
                         'year': year,
                         'value': value,
                         NWIS_TO_CARMA_ATTR['unit']: cat_desc['unit']}
                water_use_objects.append(datum)

            except KeyError:
                logger.warning(f"Water use variable {k} not found in USGS data, but should be")
    return water_use_objects
