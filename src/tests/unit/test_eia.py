import unittest

from carma_harvesters.powerplants.eia import PowerPlantLocations


class TestPowerPlantLocations(unittest.TestCase):
    def test_powerplant_locations(self):
        loc = PowerPlantLocations()
        self.assertIsNotNone(loc)

        response = loc.get_lon_lat_for_plant(63924)
        self.assertIsNotNone(response)
        self.assertEqual('-85.654444', response[0])
        self.assertEqual('40.294347', response[1])

        response = loc.get_lon_lat_for_plant(6392400)
        self.assertIsNone(response)
