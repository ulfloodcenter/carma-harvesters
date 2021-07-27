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

    def __repr__(self) -> str:
        return ("CountyPopulation {\n"
                f"\tname: {self.name},\n"
                f"\tstate_fips: {self.state_fips},\n"
                f"\tcounty_fips: {self.county_fips},\n"
                f"\tlast_update: {self.last_update},\n"
                f"\tyear: {self.year},\n"
                f"\tpopulation: {self.population}\n"
                "}\n")


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


def query_population_for_counties(census_api_key: str, population_year: int, fips: dict) -> dict:
    county_pop = []
    # First query entire states
    if 'state' in fips:
        states = ','.join(s for s in fips['state'])
        if states != '':
            county_pop = county_pop + get_county_population(census_api_key, population_year, states)
    # Next query individual counties.
    counties_by_state = {}
    if 'state_county' in fips:
        for st_co in fips['state_county']:
            st = st_co[:2]
            co = st_co[2:]
            if st in counties_by_state:
                counties_by_state[st].append(co)
            else:
                counties_by_state[st] = [co]
    for st in counties_by_state:
        counties = ','.join(c for c in counties_by_state[st])
        county_pop = county_pop + get_county_population(census_api_key, population_year, st, counties)
    # Collate into dict with keys $state_fips+$county_fips
    pop_by_county = {}
    for co_pop in county_pop:
        fq_id = co_pop.state_fips + co_pop.county_fips
        if fq_id in pop_by_county:
            pop_by_county[fq_id].append(co_pop)
        else:
            pop_by_county[fq_id] = [co_pop]

    return pop_by_county


def get_county_population(api_key: str, year: int, state_fips: str, county_fips: str = None) -> List[CountyPopulation]:
    if year not in POPULATION_URL_TEMPLATES:
        return None

    url_template, population_type = POPULATION_URL_TEMPLATES[year]
    if county_fips is None:
        county_fips = '*'
    url = url_template.format(k=api_key, state=state_fips, county=county_fips)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Unable to read population data from Census API {url}, status was: {r.status_code}")
    try:
        response_data = r.json()
    except Exception as e:
        logger.error(f"Error parson JSON for response body: {r.text}")
        raise Exception(f"Unable to read population data from Census API {url}, JSON parse error.")

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
