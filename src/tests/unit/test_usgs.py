# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import unittest

from shapely.geometry import asShape

from carma_harvesters.powerplants.eia import PowerPlantLocations
from carma_harvesters.powerplants.usgs import USGSPowerPlantWaterUse


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

        plant_loc = PowerPlantLocations()
        self.assertIsNotNone(plant_loc)
        la_plants = plant_loc.get_plants_within_geometry(test_geom)
        # There should be 92 points in the above polygon
        self.assertEqual(92, len(la_plants))

        usgs_plant_wu = USGSPowerPlantWaterUse()
        self.assertIsNotNone(usgs_plant_wu)

        dummy_huc12 = 'https://geoconnex.us/usgs/hydrologic-unit/080801030109'
        la_plants_wu = usgs_plant_wu.get_huc12_powerplant_water_use('https://geoconnex.us/usgs/hydrologic-unit/080801030109',
                                                                   la_plants)
        self.assertEqual(31, len(la_plants_wu))
        # First plant
        self.assertEqual(6055, la_plants_wu[0].eiaPlantCode)
        self.assertEqual(-91.3692, la_plants_wu[0].eiaLongitude)
        self.assertEqual(30.7261, la_plants_wu[0].eiaLatitude)
        self.assertEqual(dummy_huc12, la_plants_wu[0].huc12)
        cons = la_plants_wu[0].usgsConsumption
        self.assertEqual(2, len(cons))
        # First consumption value
        self.assertEqual(2010, cons[0].year)
        self.assertEqual(14.6, cons[0].value)
        self.assertEqual(1, len(cons[0].waterSource))
        self.assertEqual('Surface Water', cons[0].waterSource[0])
        self.assertEqual(1, len(cons[0].waterType))
        self.assertEqual('Fresh', cons[0].waterType[0])
        # Second consumption value
        self.assertEqual(2015, cons[1].year)
        self.assertEqual(8.58, cons[1].value)
        self.assertEqual(1, len(cons[1].waterSource))
        self.assertEqual('Surface Water', cons[1].waterSource[0])
        self.assertEqual(1, len(cons[1].waterType))
        self.assertEqual('Fresh', cons[1].waterType[0])
        withd = la_plants_wu[0].usgsWithdrawal
        self.assertEqual(2, len(withd))
        # First withdrawal value
        self.assertEqual(2010, withd[0].year)
        self.assertEqual(367.0, withd[0].value)
        self.assertEqual(1, len(withd[0].waterSource))
        self.assertEqual('Surface Water', withd[0].waterSource[0])
        self.assertEqual(1, len(withd[0].waterType))
        self.assertEqual('Fresh', withd[0].waterType[0])
        # Second withdrawal value
        self.assertEqual(2015, withd[1].year)
        self.assertEqual(242.0, withd[1].value)
        self.assertEqual(1, len(withd[1].waterSource))
        self.assertEqual('Surface Water', withd[1].waterSource[0])
        self.assertEqual(1, len(withd[1].waterType))
        self.assertEqual('Fresh', withd[1].waterType[0])

        # Last plant
        self.assertEqual(56565, la_plants_wu[-1].eiaPlantCode)
        self.assertEqual(-93.760125, la_plants_wu[-1].eiaLongitude)
        self.assertEqual(32.51947, la_plants_wu[-1].eiaLatitude)
        self.assertEqual(dummy_huc12, la_plants_wu[-1].huc12)
        cons = la_plants_wu[-1].usgsConsumption
        self.assertEqual(2, len(cons))
        # First consumption value
        self.assertEqual(2010, cons[0].year)
        self.assertEqual(0.76, cons[0].value)
        self.assertEqual(1, len(cons[0].waterSource))
        self.assertEqual('Surface Water', cons[0].waterSource[0])
        self.assertEqual(1, len(cons[0].waterType))
        self.assertEqual('Fresh', cons[0].waterType[0])
        # Second consumption value
        self.assertEqual(2015, cons[1].year)
        self.assertEqual(1.59, cons[1].value)
        self.assertEqual(1, len(cons[1].waterSource))
        self.assertEqual('Surface Water', cons[1].waterSource[0])
        self.assertEqual(1, len(cons[1].waterType))
        self.assertEqual('Fresh', cons[1].waterType[0])
        withd = la_plants_wu[-1].usgsWithdrawal
        self.assertEqual(2, len(withd))
        # First withdrawal value
        self.assertEqual(2010, withd[0].year)
        self.assertEqual(1.06, withd[0].value)
        self.assertEqual(1, len(withd[0].waterSource))
        self.assertEqual('Surface Water', withd[0].waterSource[0])
        self.assertEqual(1, len(withd[0].waterType))
        self.assertEqual('Fresh', withd[0].waterType[0])
        # Second withdrawal value
        self.assertEqual(2015, withd[1].year)
        self.assertEqual(2.23, withd[1].value)
        self.assertEqual(1, len(withd[1].waterSource))
        self.assertEqual('Surface Water', withd[1].waterSource[0])
        self.assertEqual(1, len(withd[1].waterType))
        self.assertEqual('Fresh', withd[1].waterType[0])
