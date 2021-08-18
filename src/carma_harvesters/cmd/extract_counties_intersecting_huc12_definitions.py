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
    verify_input, dissolve_huc12_geometries, geom_to_shapely, open_existing_carma_document, write_objects_to_existing_carma_document
from .. util import run_ogr2ogr
from .. census import query_population_for_counties, POPULATION_URL_TEMPLATES
from .. nhd import get_geography_stream_characteristics
from .. crops.cropscape import calculate_geography_crop_area
from .. nlcd import get_percent_highly_developed_land


ST_PATT = re.compile('^\s*([0-9]{2}),*\s*$')
ST_CO_PATT = re.compile('^\s*([0-9]{5}),*\s*$')

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description=('Extract counties intersecting CARMA HUC12 definitions from '
                                                  'datasets. Note: If your OGR installation is not in /usr/local, '
                                                  'set the environment variable OGR_PREFIX appropriately.'))
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watershed '
                              'definitions. Counties intersecting HUC12 watersheds '
                              'will be written to the same file.'))
    parser.add_argument('-y', '--population_year', type=int, default=2015,
                        help='Year for which county population should be queried from US Census.')
    parser.add_argument('-a', '--census_api_key', required=True,
                        help='Census API key obtained from https://api.census.gov/data/key_signup.html')
    parser.add_argument('-ly', '--landcover_year', required=False, type=int, default=DEFAULT_NLCD_YEAR,
                        help='Year of NLCD landcover data to use to derive developed area.')
    parser.add_argument('-cy', '--crop_year', required=False, type=int, default=DEFAULT_CDL_YEAR,
                        help='Year USDA Cropland Data Layer to use for crops data.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--debug', help='Debug mode: do not delete output if there is an exception',
                        action='store_true', default=False)
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

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    error = False

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        huc12_dissolve_file = tempfile.NamedTemporaryFile(mode='w', suffix='.geojson',
                                                          dir=temp_out,
                                                          delete=False)
        logger.debug(f"Dissolving CARMA HUC12 geometries to {huc12_dissolve_file.name}...")
        huc12_dissolve = dissolve_huc12_geometries(document)
        xmin, ymin, xmax, ymax = huc12_dissolve.bounds

        # '-nlt', 'PROMOTE_TO_MULTI',
        counties_for_huc12_path = os.path.join(temp_out, f"counties_for_huc12s.geojson")
        run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326',
                    counties_for_huc12_path, data_result['paths']['counties'], 'gu_countyorequivalent',
                    '-spat', str(xmin), str(ymin), str(xmax), str(ymax))

        # Read county attributes and geometries write to CARMA format
        carma_counties = []
        fips_stco = []
        fips = {'state_county': fips_stco}

        # counties = fiona.open(counties_for_huc12_path, 'r')
        with open(counties_for_huc12_path, 'r') as f:
            counties = json.load(f)

        progress_bar = tqdm(counties['features'])
        for county in progress_bar:
            progress_bar.set_description(f"Building attributes for county {county['properties']['stco_fipscode']}")
            if huc12_dissolve.intersects((geom_to_shapely(county['geometry']))):
                c = OrderedDict()

                short_id = county['properties']['stco_fipscode']
                # Record county ID so that we can later query Census web service
                fips_stco.append(short_id)
                logger.debug(f"County ID from GeoJSON {short_id}")
                c['id'] = County.generate_fq_id(short_id)
                c['state'] = county['properties']['state_name']
                c['county'] = county['properties']['county_name']
                c['area'] = county['properties']['areasqkm']
                # Get population from Census web service so just store an empty array right now
                c['population'] = []
                c['geometry'] = county['geometry']

                carma_counties.append(c)
            else:
                logger.debug(f"Omitting county {county['properties']['stco_fipscode']} outside of HUC12 boundaries.")

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
        write_objects_to_existing_carma_document(carma_counties, 'Counties',
                                                 document, abs_carma_inpath,
                                                 temp_out, args.overwrite)
    except Exception as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        else:
            shutil.rmtree(temp_out)
