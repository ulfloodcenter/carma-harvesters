import os
import argparse
import tempfile
import shutil
import re
import logging
import sys
import traceback
import json
from collections import OrderedDict

from .. common import verify_raw_data, verify_input, verify_outpath, output_json
from .. util import run_ogr2ogr
from .. census import get_county_population, POPULATION_URL_TEMPLATES
from .. nhd import get_county_stream_characteristics
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land
from .. geoconnex.census import County


ST_PATT = re.compile('^\s*([0-9]{2}),*\s*$')
ST_CO_PATT = re.compile('^\s*([0-9]{5}),*\s*$')

logger = logging.getLogger(__name__)


def _parse_county_fips(input_path: str) -> dict:
    state_fips = set()
    state_county_fips = set()
    fips = {'state': state_fips,
            'state_county': state_county_fips}
    with open(input_path) as f:
        for l in f:
            m = ST_PATT.match(l)
            if m:
                state_fips.add(m.group(1))
                continue
            m = ST_CO_PATT.match(l)
            if m:
                state_county_fips.add(m.group(1))
                continue

    # Scan state+county FIPS to make sure they are not covered by state FIPS
    # Copy list to set so that we can mutate set as we iterate
    state_county_fips_list = [f for f in state_county_fips]
    for st_co_fip in state_county_fips_list:
        if st_co_fip[:2] in state_fips:
            try:
                state_county_fips.remove(st_co_fip)
            except KeyError:
                # Ignore: may have already been removed from set in previous iteration over list copy of set.
                pass

    return fips


def _query_population_by_county(census_api_key, population_year, fips) -> dict:
    county_pop = []
    # First query entire states
    states = ','.join(s for s in fips['state'])
    if states != '':
        county_pop = county_pop + get_county_population(census_api_key, population_year, states)
    # Next query individual counties.
    counties_by_state = {}
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


def main():
    parser = argparse.ArgumentParser(description=('Extract county definitions in CARMA format from TIGER/Census\n'
                                                  'datasets. Note: If your OGR installation is not in /usr/local, '
                                                  'set the environment variable OGR_PREFIX appropriately.'))
    parser.add_argument('-d', '--datapath', help=('Directory containing data downloaded/extracted from '
                                                  'bin/download-data.sh.'))
    parser.add_argument('-o', '--outpath', help='Directory where output should be stored.')
    parser.add_argument('-n', '--outname', help=('Name of file, stored in outpath, where CARMA-schema formatted output '
                                                'should be stored.'))
    parser.add_argument('-i', '--county_path', help='Path to file containing one or more state or county FIPS code, one per line.')
    parser.add_argument('-y', '--population_year', type=int, default=2015, help='Year for which county population should be queried from US Census.')
    parser.add_argument('-c', '--census_api_key', help='Census API key obtained from https://api.census.gov/data/key_signup.html')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    if args.population_year not in POPULATION_URL_TEMPLATES:
        sys.exit(f"Population year must be one of: {list(POPULATION_URL_TEMPLATES.keys())}")

    success, data_result = verify_raw_data(args.datapath)
    if not success:
        for e in data_result['errors']:
            print(e)
        sys.exit("Invalid source data, exiting. Try running 'download-data.sh'.")

    success, out_result = verify_outpath(args.outpath, args.outname, args.overwrite)
    if not success:
        for e in out_result['errors']:
            print(e)
        sys.exit("Output path or name errors, exiting.")

    success, input_result = verify_input(args.county_path)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        # Read county FIPS from input file
        fips = _parse_county_fips(args.county_path)
        logger.debug(f"FIPS to extract: {fips}")

        carma_counties = []

        county_geojson = []
        # Export counties as GeoJSON: 1st entire states
        for state in fips['state']:
            tmp_geojson = os.path.join(temp_out, f"tmp_counties_{state}.geojson")
            county_geojson.append(tmp_geojson)
            where_clause = f"\"state_fipscode='{state}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_geojson, data_result['paths']['counties'],
                        'gu_countyorequivalent', '-where', where_clause)

        # Export counties as GeoJSON: 2nd individual counties
        for county in fips['state_county']:
            tmp_geojson = os.path.join(temp_out, f"tmp_county_{county}.geojson")
            county_geojson.append(tmp_geojson)
            where_clause = f"\"stco_fipscode='{county}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_geojson,
                        data_result['paths']['counties'],
                        'gu_countyorequivalent', '-where', where_clause)

        # Read county attributes and geometries write to CARMA format
        county_ids = []
        for geojson in county_geojson:
            with open(geojson) as f:
                feat_coll = json.load(f)
            features = feat_coll['features']
            for f in features:
                c = OrderedDict()
                short_id = f['properties']['stco_fipscode']
                logger.debug(f"County ID from GeoJSON {short_id}")
                c['id'] = County.generate_fq_id(short_id)
                c['state'] = f['properties']['state_name']
                c['county'] = f['properties']['county_name']
                c['area'] = f['properties']['areasqkm']
                # Get population from Census web service so just store an empty array right now
                c['population'] = []
                # Record county ID so that we can later query Census web service
                county_ids.append(short_id[2:])
                c['geometry'] = f['geometry']

                carma_counties.append(c)

        # Query Census web service for population data
        pop_by_county = _query_population_by_county(args.census_api_key, args.population_year, fips)
        logger.debug(f"Population by county: {pop_by_county}")

        # Do county-by-county processing
        for c in carma_counties:
            # Add population data to county definitions
            pops_for_county = pop_by_county[short_id]
            for p in pops_for_county:
                pop_entry = {'year': p.year,
                             'count': p.population}
                c['population'].append(pop_entry)

            # Get stream characteristics
            logger.debug(f"Getting stream characteristics for county {c['id']}. This may take a while...")
            max_strm_ord, min_strm_lvl, max_mean_ann_flow = \
                get_county_stream_characteristics(c['geometry'], data_result['paths']['flowline'])
            logger.debug(f"Stream characteristics: max_strm_ord: {max_strm_ord}, min_strm_lvl: {min_strm_lvl}, max_mean_ann_flow: {max_mean_ann_flow}")
            c['maxStreamOrder'] = max_strm_ord
            c['minStreamLevel'] = min_strm_lvl
            c['meanAnnualFlow'] = max_mean_ann_flow

            # Compute zonal stats for crop cover
            cdl_year, cdl_path = data_result['paths']['cdl']
            total_crop_area, crop_areas = calculate_geography_crop_area(c['geometry'], cdl_path, c['area'])
            logger.debug(f"CDL total crop area: {total_crop_area}")
            logger.debug(f"CDL individual crop areas: {crop_areas}")
            c['crops'] = [OrderedDict([
                ('year', cdl_year),
                ('cropArea', total_crop_area),
                ('cropAreaDetail', crop_areas)
            ])]

            # Compute zonal stats for landcover
            nlcd_year, nlcd_path = data_result['paths']['nlcd']
            developed_nlcd_cells, total_nlcd_cells = get_percent_highly_developed_land(c['geometry'], nlcd_path)
            developed_proportion = developed_nlcd_cells / total_nlcd_cells
            c['developedArea'] = [OrderedDict([
                ('year', nlcd_year),
                ('area', c['area'] * developed_proportion)
            ])]

        # Save CARMA county definitions
        carma_definition = {'Counties': carma_counties}
        output_json(out_result['paths']['out_file_path'], temp_out, carma_definition, args.overwrite)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
