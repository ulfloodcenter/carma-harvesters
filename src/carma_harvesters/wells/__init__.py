import json
import re


YEAR_COMPLETED_ATTR = 'yearCompleted'


class WellAttributeMapper:
    def __init__(self, mapper_config_path: str):
        with open(mapper_config_path, 'r') as f:
            self.config = json.load(f)

    def map_well_attributes(self, well_properties: dict) -> dict:
        """
        Map from native well attributes to CARMA-compliant attributes
        :param well_properties: Properties for a feature of a GeoJSON-like Python geo interface feature collection
        :return:
        """
        mapped_value = {}
        for carma_property, native_property in self.config['attributes'].items():
            carma_value = None
            native_value = well_properties[native_property]
            if carma_property == YEAR_COMPLETED_ATTR:
                #import pdb; pdb.set_trace()
                # Value entry will be a list of patterns
                for mapping in self.config['values'][native_property]:
                    if isinstance(mapping, dict):
                        if native_value in mapping:
                            carma_value = mapping[native_value]
                            break
                    elif isinstance(mapping, str):
                        m = re.match(mapping, native_value)
                        if m:
                            carma_value = m.group('year')
                        break
            else:
                # Value entry will be dictionary whose keys are patterns to be used to attempt to classify inputs into
                # a valid CARMA, which is specified by the value of the key. Try to match one of these patterns
                value_mapping = self.config['values'][native_property]
                # import pdb; pdb.set_trace()
                for pattern, tmp_carma_value in value_mapping.items():
                    m = re.match(pattern, native_value)
                    if m:
                        carma_value = tmp_carma_value
                    break

            if carma_value:
                mapped_value[carma_property] = carma_value

        return mapped_value
