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

from carma_schema.geoconnex.usgs import HydrologicUnit

from .. common import verify_raw_data, DEFAULT_NLCD_YEAR, DEFAULT_CDL_YEAR, \
    verify_input, verify_outpath, output_json
from .. util import run_ogr2ogr
from .. nhd import get_huc12_mean_annual_flow, get_huc12_max_stream_order, get_huc12_min_stream_level
from .. crops.cropscape import calculate_geography_crop_area
from .. usgs.recharge import calculate_huc12_mean_recharge
from .. nlcd import get_percent_highly_developed_land


HUC12_PATT = re.compile('^\s*([0-9]{12}),*\s*$')
NLCD_HIGHLY_DEVELOPED_DN = 24

logger = logging.getLogger(__name__)


def _read_huc12_id(huc_path: str) -> set:
    huc_ids = set()
    with open(huc_path) as f:
        for l in f:
            m = HUC12_PATT.match(l)
            if m:
                huc_ids.add(m.group(1))
    return huc_ids


def main():
    parser = argparse.ArgumentParser(description='Extract HUC12 definitions in CARMA format from NHDPlus datasets')
    parser.add_argument('-d', '--datapath', required=True,
                        help=('Directory containing data downloaded/extracted from '
                              'bin/download-data.sh.'))
    parser.add_argument('-o', '--outpath', required=True,
                        help='Directory where output should be stored.')
    parser.add_argument('-n', '--outname', required=True,
                        help=('Name of file, stored in outpath, where CARMA-schema formatted output '
                              'should be stored.'))
    parser.add_argument('-i', '--huc_path', required=True,
                        help='Path to file containing one or more HUC12 identifiers, one per line.')
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
        logging.basicConfig(stream=sys.stdout, level=logging.WARNING)

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

    success, input_result = verify_input(args.huc_path)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    error = False

    huc8_streams = {}

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        # Read HUC12 IDs from input file
        huc12_ids = [id for id in _read_huc12_id(args.huc_path)]
        logger.debug(f"HUC12s: {huc12_ids}")

        carma_huc12s = []
        progress_bar = tqdm(huc12_ids)
        for id in progress_bar:
            progress_bar.set_description(f"Extracting HUC12 {id}")
            # First pull out HUC12 from WBD
            # e.g.  ogr2ogr -f GeoJSON 080403030102.geojson NHDPlusNationalData/WBDSnapshot_National.shp WBDSnapshot_National -where "huc_12='080403030102'"
            tmp_huc12_geom = os.path.join(temp_out, f"tmp_huc12_{id}.geojson")
            where_clause = f"\"huc_12='{id}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_huc12_geom, data_result['paths']['wbd'], 'WBDSnapshot_National',
                        '-where', where_clause)

            # Then extract NHDFlowlines for the HUC8 that the HUC12 is in...
            # e.g. ogr2ogr -f GeoJSON HUC8_08040303_streams.geojson NHDFlowline_Network.sqlite -where "reachcode LIKE '08040303%'"
            huc8_id = id[:8]
            if huc8_id in huc8_streams:
                # See if we have already extracted streams for the HUC8
                tmp_huc8_streams = huc8_streams[huc8_id]
            else:
                # Cache HUC8 streams as their can be many HUC12s in a given HUC8
                tmp_huc8_streams = os.path.join(temp_out, f"tmp_huc8_{huc8_id}_flowlines.spatialite")
                where_clause = f"\"reachcode LIKE '{huc8_id}%'\""
                run_ogr2ogr('-f', 'SQLite', tmp_huc8_streams, data_result['paths']['flowline'], '-where', where_clause)
                huc8_streams[huc8_id] = tmp_huc8_streams

            # Then extract HUC8 NHDFlowlines that fall within HUC12 boundary (use HUC8 flowlines instead of national data as
            # this will be much faster).
            # e.g. ogr2ogr -f SQLite 080403030102_streams.sqlite HUC8_08040303_streams.geojson -clipsrc 080403030102.geojson
            tmp_huc12_streams = os.path.join(temp_out, f'tmp_huc12_{id}_flowlines.sqlite')
            run_ogr2ogr('-f', 'SQLite', tmp_huc12_streams, tmp_huc8_streams, '-clipsrc', tmp_huc12_geom)

            # Extract some information from the NHD flowline
            mean_annual_flow = get_huc12_mean_annual_flow(tmp_huc12_streams)
            logger.debug(f"Mean annual flow for HUC12 {id} was {mean_annual_flow}")
            max_stream_order = get_huc12_max_stream_order(tmp_huc12_streams)
            logger.debug(f"Max stream order for HUC12 {id} was {max_stream_order}")
            min_stream_level = get_huc12_min_stream_level(tmp_huc12_streams)
            logger.debug(f"Min stream level for HUC12 {id} was {min_stream_level}")

            # Read HUC12 geometry from GeoJSON
            with open(tmp_huc12_geom) as f:
                huc12_geom = json.load(f)
            features = huc12_geom['features']
            if len(features) != 1:
                raise Exception("More than one feature encountered for HUC12 {id} when only one was expected.")
            f = features[0]
            h12 = OrderedDict()
            short_id = f['properties']['huc_12']
            logger.debug(f"HUC12 ID from GeoJSON {short_id}")
            h12['id'] = HydrologicUnit.generate_fq_id(short_id)
            if f['properties']['hu_12_name']:
                h12['description'] = f['properties']['hu_12_name']
            else:
                h12['description'] = short_id
            h12['area'] = f['properties']['areahuc12']
            if max_stream_order:
                h12['maxStreamOrder'] = max_stream_order
            if min_stream_level:
                h12['minStreamLevel'] = min_stream_level
            if mean_annual_flow:
                h12['meanAnnualFlow'] = mean_annual_flow

            # Compute zonal stats for crop cover
            cdl_year, cdl_path = data_result['paths']['cdl']
            total_crop_area, crop_areas = calculate_geography_crop_area(f, cdl_path, h12['area'])
            logger.debug(f"CDL total crop area: {total_crop_area}")
            logger.debug(f"CDL individual crop areas: {crop_areas}")
            h12['crops'] = [OrderedDict([
                ('year', cdl_year),
                ('cropArea', total_crop_area),
                ('cropAreaDetail', crop_areas)
            ])]

            # Compute zonal stats for landcover
            nlcd_year, nlcd_path = data_result['paths']['nlcd']
            developed_nlcd_cells, total_nlcd_cells = get_percent_highly_developed_land(f, nlcd_path)
            developed_proportion = developed_nlcd_cells / total_nlcd_cells
            h12['developedArea'] = [OrderedDict([
                ('year', nlcd_year),
                ('area', h12['area'] * developed_proportion)
            ])]

            # Compute zonal stats for groundwater recharge
            recharge_path = data_result['paths']['recharge']
            recharge = calculate_huc12_mean_recharge(f, recharge_path)
            if recharge:
                h12['recharge'] = recharge

            # Add geometry last so that other properties appear first
            h12['geometry'] = f['geometry']

            carma_huc12s.append(h12)

        # Save CARMA HUC12 definitions
        carma_definition = {'HUC12Watersheds': carma_huc12s}
        output_json(out_result['paths']['out_file_path'], temp_out, carma_definition, args.overwrite)
    except Exception as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        else:
            shutil.rmtree(temp_out)
