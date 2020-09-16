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

import rasterstats

from .. common import DATA_BASENAMES, verify_raw_data, verify_input, verify_outpath
from .. util import run_ogr2ogr
from .. nhd import get_huc12_mean_annual_flow, get_huc12_max_stream_order
from .. crops.cropscape import calculate_huc12_crop_area


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
    parser.add_argument('-d', '--datapath', help=('Directory containing the following data files/directories: '
                                                  'NHDPlusNationalData/NationalWBDSnapshot.gdb, '
                                                  'NHDFlowline_Network.sqlite, PlusFlow.sqlite'))
    parser.add_argument('-o', '--outpath', help='Directory where output should be stored.')
    parser.add_argument('-n', '--outname', help=('Name of file, stored in outpath, where CARMA-schema formatted output '
                                                'should be stored.'))
    parser.add_argument('-i', '--huc_path', help='Path to file containing one or more HUC12 identifiers, one per line.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

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

    success, input_result = verify_input(args.huc_path)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        # Read HUC12 IDs from input file
        huc12_ids = [id for id in _read_huc12_id(args.huc_path)]
        logger.debug(f"HUC12s: {huc12_ids}")

        carma_huc12s = []
        for id in huc12_ids:
            # First pull out HUC12 from WBD
            # e.g.  ogr2ogr -f GeoJSON 080403030102.geojson NHDPlusNationalData/WBDSnapshot_National.shp WBDSnapshot_National -where "HUC_12='080403030102'"
            tmp_huc12_geom = os.path.join(temp_out, 'tmp_huc12.geojson')
            where_clause = f"\"HUC_12='{id}'\""
            run_ogr2ogr('-f', 'GeoJSON', '-t_srs', 'EPSG:4326', tmp_huc12_geom, data_result['paths']['wbd'], 'WBDSnapshot_National',
                        '-where', where_clause)
            # Then extract NHDFlowlines for the HUC8 that the HUC12 is in...
            # e.g. ogr2ogr -f GeoJSON HUC8_08040303_streams.geojson NHDFlowline_Network.sqlite -where "reachcode LIKE '08040303%'"
            tmp_huc8_streams = os.path.join(temp_out, 'tmp_huc8_flowlines.geojson')
            where_clause = f"\"reachcode LIKE '{id[:8]}%'\""
            run_ogr2ogr('-f', 'GeoJSON', tmp_huc8_streams, data_result['paths']['flowline'], '-where', where_clause)

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

            # Read HUC12 geometry from GeoJSON
            with open(tmp_huc12_geom) as f:
                huc12_geom = json.load(f)
            features = huc12_geom['features']
            if len(features) != 1:
                raise Exception("More than one feature encountered for HUC12 {id} when only one was expected.")
            f = features[0]
            h12 = OrderedDict()
            logger.debug(f"HUC12 ID from GeoJSON {f['properties']['HUC_12']}")
            h12['id'] = f['properties']['HUC_12']
            h12['description'] = f['properties']['HU_12_NAME']
            h12['area'] = f['properties']['AreaHUC12']
            h12['maxStreamOrder'] = max_stream_order
            h12['meanAnnualFlow'] = mean_annual_flow

            # Compute zonal stats for crop cover
            total_crop_area, crop_areas = calculate_huc12_crop_area(f, data_result['paths']['cdl'], h12['area'])
            logger.debug(f"CDL total crop area: {total_crop_area}")
            logger.debug(f"CDL individual crop areas: {crop_areas}")
            h12['cropArea'] = total_crop_area
            h12['cropAreaDetail'] = crop_areas

            # Compute zonal stats for landcover
            stats = rasterstats.zonal_stats(f, data_result['paths']['nlcd'],
                                            categorical=True)[0]
            logger.debug(f"NLCD zonal stats: {stats}")
            total_nlcd_cells = sum(stats.values())
            # Should this also include NLCD medium-intensity?
            developed_nlcd_cells = stats.get(NLCD_HIGHLY_DEVELOPED_DN, 0.0)
            developed_proportion = developed_nlcd_cells / total_nlcd_cells
            h12['developedArea'] = h12['area'] * developed_proportion

            # Add geometry last so that other properties appear first
            h12['geometry'] = f

            carma_huc12s.append(h12)

        # Save CARMA HUC12 definitions
        carma_definition = {'HUC12Watersheds': carma_huc12s}
        with open(out_result['paths']['out_file_path'], 'w') as f:
            json.dump(carma_definition, f)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
