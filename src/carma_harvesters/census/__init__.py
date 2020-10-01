from typing import List
import logging

import requests


CENSUS_POPULATION_TYPE_PEP = 1
CENSUS_POPULATION_TYPE_PEP_OLD = 2
CENSUS_POPULATION_TYPE_DECENNIAL = 3

POPULATION_URL_TEMPLATES = {
    2000: ("https://api.census.gov/data/2000/dec/sf1?key={k}&get=NAME,P001001&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_DECENNIAL),
    2010: ("https://api.census.gov/data/2010/dec/sf1?key={k}&get=NAME,P001001&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_DECENNIAL),
    2015: ("https://api.census.gov/data/2015/pep/population?key={k}&get=GEONAME,POP,LASTUPDATE&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_PEP_OLD),
    2016: ("https://api.census.gov/data/2016/pep/population?key={k}&get=GEONAME,POP,LASTUPDATE&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_PEP_OLD),
    2017: ("https://api.census.gov/data/2017/pep/population?key={k}&get=GEONAME,POP,LASTUPDATE&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_PEP_OLD),
    2018: ("https://api.census.gov/data/2018/pep/population?key={k}&get=GEONAME,POP,LASTUPDATE&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_PEP_OLD),
    2019: ("https://api.census.gov/data/2019/pep/population?key={k}&get=NAME,POP,LASTUPDATE&for=county:{county}&in=state:{state}",
           CENSUS_POPULATION_TYPE_PEP)
}


logger = logging.getLogger(__name__)


class CountyPopulation:
    def __init__(self, name: str, state_fips: str, county_fips: str, last_update:str, year: int, population: int):
        self.name = name
        self.state_fips = state_fips
        self.county_fips = county_fips
        self.last_update = last_update
        self.year = year
        self.population = int(population)


def _deserialize_data_pep_old(year:int, d:list) -> CountyPopulation:
    return CountyPopulation(name=d[0],
                            state_fips=d[3],
                            county_fips=d[4],
                            last_update=d[2],
                            year=year,
                            population=d[1])


def _deserialize_data_pep(year:int, d:list) -> CountyPopulation:
    return CountyPopulation(name=d[0],
                            state_fips=d[3],
                            county_fips=d[4],
                            last_update=d[2],
                            year=year,
                            population=d[1])


def _deserialize_data_dec(year:int, d:list) -> CountyPopulation:
    return CountyPopulation(name=d[0],
                            state_fips=d[2],
                            county_fips=d[3],
                            last_update=None,
                            year=year,
                            population=d[1])


def get_county_population(api_key, year, state_fips, county_fips=None) -> List[CountyPopulation]:
    if year not in POPULATION_URL_TEMPLATES:
        return None

    url_template, population_type = POPULATION_URL_TEMPLATES[year]
    if county_fips is None:
        county_fips = '*'
    url = url_template.format(k=api_key, state=state_fips, county=county_fips)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Unable to read population data from Census API {url}, status was: {r.status_code}")
    response_data = r.json()
    if len(response_data) < 2:
        logger.warning(f"Census data from {url} did not return data, response was {r.text}.")
        return None

    pop_data = []
    for datum in response_data[1:]:
        if population_type == CENSUS_POPULATION_TYPE_PEP:
            pop_data.append(_deserialize_data_pep(year, datum))
        elif population_type == CENSUS_POPULATION_TYPE_PEP_OLD:
            pop_data.append(_deserialize_data_pep_old(year, datum))
        elif population_type == CENSUS_POPULATION_TYPE_DECENNIAL:
            pop_data.append(_deserialize_data_dec(year, datum))
    return pop_data
