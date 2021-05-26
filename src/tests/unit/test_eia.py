import unittest

from shapely.geometry import asShape

from carma_harvesters.powerplants.eia import PowerPlantLocations


class TestPowerPlantLocations(unittest.TestCase):
    def test_powerplant_locations_geom(self):
        # -93.8562,29.9930,-91.0107,32.6024
        test_geojson = {
            "type": "Polygon",
            "coordinates": [[ [-95.8562, 28.9930], 
                              [-95.8562, 32.6024], 
                              [-91.0107, 32.6024],
                              [-91.0107, 29.9930],
                              [-95.8562, 29.9930] ]]
        }
        test_geom = asShape(test_geojson)

        loc = PowerPlantLocations()
        self.assertIsNotNone(loc)

        la_plants = loc.get_plants_within_geometry(test_geom)
        # There should be 92 points in the above polygon
        self.assertEqual(92, len(la_plants))
        # First plant
        self.assertEqual(6055, la_plants[0].eiaPlantCode)
        self.assertEqual(-91.3692, la_plants[0].eiaLongitude)
        self.assertEqual(30.7261, la_plants[0].eiaLatitude)
        # Last plant
        self.assertEqual(54240, la_plants[-1].eiaPlantCode)
        self.assertEqual(-92.6497, la_plants[-1].eiaLongitude)
        self.assertEqual(32.5256, la_plants[-1].eiaLatitude)


