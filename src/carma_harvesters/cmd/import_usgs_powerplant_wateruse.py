import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
from dataclasses import asdict

from shapely.geometry import asShape

from carma_harvesters.common import open_existing_carma_document, verify_input, write_objects_to_existing_carma_document, output_json
from carma_harvesters.util import Geometry
from carma_harvesters.powerplants.eia import PowerPlantLocations
from carma_harvesters.powerplants.usgs import USGSPowerPlantWaterUse
from carma_harvesters.exception import SchemaValidationException


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description=('Import USGS water use data for thermoelectric power plants located in '
                                                  'each HUC12 watershed. Water use data for 2010 and 2015 from the '
                                                  'following USGS reports are used: '
                                                  '2010 (https://pubs.usgs.gov/sir/2014/5184/pdf/sir20145184.pdf) '
                                                  '2015 (https://pubs.er.usgs.gov/publication/sir20195103). '
                                                  'Power plant location data is from 2019 EIA Form 860 data available '
                                                  'here: https://www.eia.gov/electricity/data/eia860/. Note: All data are '
                                                  'bundled with CARMA and are not downloaded.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions of HUC12 watersheds. Resulting power plants '
                              'found in each HUC12 that have USGS water use data will be written to the same file.'))
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output', default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    abs_carma_inpath = os.path.abspath(args.carma_inpath)
    success, input_result = verify_input(abs_carma_inpath)
    if not success:
        for e in input_result['errors']:
            print(e)
        sys.exit("Invalid input data, exiting.")

    try:
        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        document = open_existing_carma_document(abs_carma_inpath)

        if 'HUC12Watersheds' not in document or len(document['HUC12Watersheds']) < 1:
            sys.exit(f"No HUC12 watersheds defined in {abs_carma_inpath}")

        eia_plant_loc = PowerPlantLocations()
        usgs_plant_wu = USGSPowerPlantWaterUse()
        power_plant_datasets = []

        # Foreach HUC12...
        for huc12 in document['HUC12Watersheds']:
            huc12_geom = Geometry(huc12['geometry'])
            huc12_shape = asShape(huc12_geom)
            # Find power plants in HUC12
            huc12_plants = eia_plant_loc.get_plants_within_geometry(huc12_shape)
            # Get plants in HUC12 with water use data and those data
            huc12_plants = usgs_plant_wu.get_huc12_powerplant_water_use(huc12['id'],
                                                                        huc12_plants)

            power_plant_datasets.extend(huc12_plants)

        # Write updated CARMA file
        power_plant_objects = [asdict(p) for p in power_plant_datasets]
        write_objects_to_existing_carma_document(power_plant_objects, 'PowerPlantDatasets',
                                                 document, abs_carma_inpath,
                                                 temp_out, args.overwrite)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        sys.exit(e)
    finally:
        shutil.rmtree(temp_out)
