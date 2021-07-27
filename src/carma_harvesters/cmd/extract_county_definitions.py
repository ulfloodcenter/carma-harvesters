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

from tqdm import tqdm

from carma_schema.geoconnex.census import County

from .. common import verify_raw_data, DEFAULT_NLCD_YEAR, DEFAULT_CDL_YEAR, \
    verify_input, verify_outpath, output_json
from .. util import run_ogr2ogr
from .. census import query_population_for_counties, POPULATION_URL_TEMPLATES
from .. nhd import get_geography_stream_characteristics
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land


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


def main():
    parser = argparse.ArgumentParser(description=('Extract county definitions in CARMA format from TIGER/Census\n'
                                                  'datasets. Note: If your OGR installation is not in /usr/local, '
                                                  'set the environment variable OGR_PREFIX appropriately.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-o', '--outpath', required=True,
                        help='Directory where output should be stored.')
    parser.add_argument('-n', '--outname', required=True,
                        help=('Name of file, stored in outpath, where CARMA-schema formatted output '
                              'should be stored.'))
    parser.add_argument('-i', '--county_path', required=True,
                        help='Path to file containing one or more state or county FIPS code, one per line.')
    parser.add_argument('-y', '--population_year', type=int, default=2015,
                        help='Year for which county population should be queried from US Census.')
    parser.add_argument('-c', '--census_api_key', required=True,
                        help='Census API key obtained from https://api.census.gov/data/key_signup.html')
    parser.add_argument('-ly', '--landcover_year', required=False, type=int, default=DEFAULT_NLCD_YEAR,
                        help='Year of NLCD landcover data to use to derive developed area.')
    parser.add_argument('-cy', '--crop_year', required=False, type=int, default=DEFAULT_CDL_YEAR,
                        help='Year USDA Cropland Data Layer to use for crops data.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    if args.population_year not in POPULATION_URL_TEMPLATES:
        sys.exit(f"Population year must be one of: {list(POPULATION_URL_TEMPLATES.keys())}")

    success, data_result = verify_raw_data(args.datapath,
                                           nlcd_year=args.landcover_year,
                                           cdl_year=args.crop_year)
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
        progress_bar = tqdm(fips['state'])
        for state in progress_bar:
            progress_bar.set_description(f"Extracting counties for state {state}")
            tmp_geojson = os.path.join(temp_out, f"tmp_counties_{state}.geojson")
            county_geojson.append(tmp_geojson)
            where_clause = f"\"state_fipscode='{state}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_geojson, data_result['paths']['counties'],
                        'gu_countyorequivalent', '-where', where_clause)

        # Export counties as GeoJSON: 2nd individual counties
        progress_bar = tqdm(fips['state_county'])
        for county in progress_bar:
            progress_bar.set_description(f"Extracting county {county}")
            tmp_geojson = os.path.join(temp_out, f"tmp_county_{county}.geojson")
            county_geojson.append(tmp_geojson)
            where_clause = f"\"stco_fipscode='{county}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_geojson,
                        data_result['paths']['counties'],
                        'gu_countyorequivalent', '-where', where_clause)

        # Read county attributes and geometries write to CARMA format
        county_ids = []
        progress_bar = tqdm(county_geojson)
        for geojson in progress_bar:
            with open(geojson) as f:
                feat_coll = json.load(f)
            features = feat_coll['features']
            for f in features:
                progress_bar.set_description(f"Building attributes for county {f['properties']['stco_fipscode']}")
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
        pop_by_county = query_population_for_counties(args.census_api_key, args.population_year, fips)
        logger.debug(f"Population by county: {pop_by_county}")

        # Do county-by-county processing
        progress_bar = tqdm(carma_counties)
        for c in progress_bar:
            short_id = County.get_short_id(c['id'])
            progress_bar.set_description(f"Adding ancillary data for county {short_id}")
            # Add population data to county definitions
            pops_for_county = pop_by_county[short_id]
            for p in pops_for_county:
                pop_entry = {'year': p.year,
                             'count': p.population}
                c['population'].append(pop_entry)

            # Get stream characteristics
            logger.debug(f"Getting stream characteristics for county {c['id']}. This may take a while...")
            max_strm_ord, min_strm_lvl, max_mean_ann_flow = \
                get_geography_stream_characteristics(c['geometry'], data_result['paths']['flowline'])
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
