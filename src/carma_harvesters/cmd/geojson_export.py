# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import argparse
import logging
import sys
import os
import tempfile
import traceback
import shutil
from collections import OrderedDict
import uuid

from carma_schema import CarmaItemNotFound, get_wassi_analysis_by_id, join_wassi_values_to_huc12_geojson

from .. exception import SchemaValidationException
from .. common import verify_input, verify_output, open_existing_carma_document, output_json, \
    join_wateruse_data_to_huc12_geojson


EXPORT_TYPE_ALL = 'all'
EXPORT_TYPE_HUC12 = 'huc12'
EXPORT_TYPE_SUBHUC12 = 'subhuc12'
EXPORT_TYPE_COUNTY = 'county'
EXPORT_TYPES = [EXPORT_TYPE_ALL, EXPORT_TYPE_HUC12, EXPORT_TYPE_SUBHUC12, EXPORT_TYPE_COUNTY]
EXPORT_TYPE_DEFAULT = EXPORT_TYPE_ALL


logger = logging.getLogger(__name__)


def _entity_to_geojson_feature(entity, entity_type):
    feature = OrderedDict()
    feature['type'] = 'Feature'
    feature['geometry'] = entity['geometry']
    properties = OrderedDict()
    feature['properties'] = properties
    properties['type'] = entity_type
    for k in filter(lambda k: k != 'geometry', entity.keys()):
        properties[k] = entity[k]
    return feature


def _entities_to_export(export_type_argument: str) -> (bool, bool, bool):
    if export_type_argument == EXPORT_TYPE_ALL:
        return True, True, True
    elif export_type_argument == EXPORT_TYPE_COUNTY:
        return True, False, False
    elif export_type_argument == EXPORT_TYPE_HUC12:
        return False, True, False
    elif export_type_argument == EXPORT_TYPE_SUBHUC12:
        return False, False, True


def main():
    parser = argparse.ArgumentParser(description=('Export HUC12, county, and sub-HUC12 definitions from a CARMA data '
                                                  'file into GeoJSON FeatureCollection file.'))
    parser.add_argument('-c', '--carma_inpath', required=True,
                        help=('Path of CARMA file containing definitions HUC12, county, and '
                              'sub-HUC12 definitions that should be export to GeoJSON.'))
    parser.add_argument('-g', '--geojson_out', required=True,
                        help=('Name of file to contain GeoJSON representations of CARMA '
                              'definitions'))
    parser.add_argument('-e', '--export_entities', required=False, choices=EXPORT_TYPES, default=EXPORT_TYPE_DEFAULT,
                        help='Type of entities to export.')
    parser.add_argument('-i', '--wassi_id', required=False,
                        help='UUID representing the ID of WaSSI analysis to export HUC12 values for.')
    parser.add_argument('-v', '--verbose', help='Produce verbose output', action='store_true', default=False)
    parser.add_argument('--debug', help='Debug mode: do not delete output if there is an exception',
                        action='store_true', default=False)
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

    success, out_result = verify_output(args.geojson_out, args.overwrite)
    if not success:
        for e in out_result['errors']:
            print(e)
        sys.exit("Invalid output path, exiting.")

    wassi_id = None
    if args.wassi_id:
        try:
            wassi_id = uuid.UUID(args.wassi_id)
        except ValueError as e:
            sys.exit(f"Invalid WaSSI ID {args.wassi_id}.")

    export_county, export_huc12, export_subhuc12 = _entities_to_export(args.export_entities)

    error = False

    try:
        document = open_existing_carma_document(abs_carma_inpath)

        wassi = None
        if wassi_id:
            wassi = get_wassi_analysis_by_id(document, wassi_id)
            if wassi is None:
                raise CarmaItemNotFound(f"No WaSSI analysis with ID {wassi_id} defined in {abs_carma_inpath}")

        # Make temporary working directory
        temp_out = tempfile.mkdtemp()
        logger.debug(f"Temp dir: {temp_out}")

        # Skeleton of GeoJSON FeatureCollection file
        feature_collection = OrderedDict()
        feature_collection['type'] = 'FeatureCollection'
        features = []
        feature_collection['features'] = features

        # Export counties
        if export_county and 'Counties' in document:
            [features.append(_entity_to_geojson_feature(e, 'County')) for e in document['Counties']]
        # Export HUC12 watersheds
        if export_huc12 and 'HUC12Watersheds' in document:
            if wassi:
                [features.append(join_wateruse_data_to_huc12_geojson(document, join_wassi_values_to_huc12_geojson(wassi, _entity_to_geojson_feature(e, 'HUC12Watershed')), wassi.waterUseYear)) for e in document['HUC12Watersheds']]
            else:
                [features.append(_entity_to_geojson_feature(e, 'HUC12Watershed')) for e in document['HUC12Watersheds']]
        # Export sub-HUC12 watersheds
        if export_subhuc12 and 'SubHUC12Watersheds' in document:
            [features.append(_entity_to_geojson_feature(e, 'SubHUC12Watershed')) for e in document['SubHUC12Watersheds']]

        # Write GeoJSON FeatureCollection
        output_json(out_result['paths']['out_file_path'], temp_out, feature_collection, args.overwrite,
                    validate=None)

    except CarmaItemNotFound as cinf:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(cinf)
    except SchemaValidationException as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    except Exception as e:
        logger.error(traceback.format_exc())
        error = True
        sys.exit(e)
    finally:
        if error and args.debug:
            pass
        else:
            shutil.rmtree(temp_out)
