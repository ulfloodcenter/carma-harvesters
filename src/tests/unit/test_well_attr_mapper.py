import unittest
import pathlib

from carma_harvesters.wells import WellAttributeMapper


FIXTURE_FILE = 'fixtures/louisiana_groundwater_wells_to_CARMA.json'

ATTR1 = {'DATE_COMPL': '09/13/2011',
         'USE_DESCRI': 'domestic',
         'WELL_STATU': 'Active'}

ATTR2 = {'DATE_COMPL': '06/96',
         'USE_DESCRI': 'commercial public supply',
         'WELL_STATU': 'Inactive'}

ATTR3 = {'DATE_COMPL': "LATE 1970's",
         'USE_DESCRI': 'monitor',
         'WELL_STATU': 'Abandoned'}

ATTR4 = {'DATE_COMPL': "CIRCA 9/95",
         'USE_DESCRI': 'industrial lumber/wood products',
         'WELL_STATU': 'Destroyed'}

ATTR5 = {'DATE_COMPL': "CIRCA 12/2001",
         'USE_DESCRI': 'industrial primary metals processing',
         'WELL_STATU': 'Active'}

ATTR6 = {'DATE_COMPL': "LATE 1980's",
         'USE_DESCRI': 'oil/gas well rig supply',
         'WELL_STATU': 'Destroyed'}

ATTR7 = {'DATE_COMPL': "PRE/1985",
         'USE_DESCRI': 'industrial',
         'WELL_STATU': 'Active'}


class TestWellAttributeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_path = pathlib.Path(__file__).parent.parent.joinpath(FIXTURE_FILE)

    def test_well_attr_mapper(self):
        mapper = WellAttributeMapper(self.fixture_path)

        carma_attr1 = mapper.map_well_attributes(ATTR1)
        self.assertEqual(carma_attr1['yearCompleted'], '2011')
        self.assertEqual(carma_attr1['sector'], 'Domestic')
        self.assertEqual(carma_attr1['status'], 'Active')

        carma_attr2 = mapper.map_well_attributes(ATTR2)
        self.assertEqual(carma_attr2['yearCompleted'], '96')
        self.assertEqual(carma_attr2['sector'], 'Commercial')
        self.assertEqual(carma_attr2['status'], 'Inactive')

        carma_attr3 = mapper.map_well_attributes(ATTR3)
        self.assertEqual(carma_attr3['yearCompleted'], '1979')
        self.assertNotIn('sector', carma_attr3)
        self.assertEqual(carma_attr3['status'], 'Abandoned')

        carma_attr4 = mapper.map_well_attributes(ATTR4)
        self.assertEqual(carma_attr4['yearCompleted'], '95')
        self.assertEqual(carma_attr4['sector'], 'Industrial')
        self.assertEqual(carma_attr4['status'], 'Destroyed')

        carma_attr5 = mapper.map_well_attributes(ATTR5)
        self.assertEqual(carma_attr5['yearCompleted'], '2001')
        self.assertEqual(carma_attr5['sector'], 'Industrial')
        self.assertEqual(carma_attr5['status'], 'Active')

        carma_attr6 = mapper.map_well_attributes(ATTR6)
        self.assertEqual(carma_attr6['yearCompleted'], '1989')
        self.assertEqual(carma_attr6['sector'], 'Commercial')
        self.assertEqual(carma_attr6['status'], 'Destroyed')

        carma_attr7 = mapper.map_well_attributes(ATTR7)
        self.assertEqual(carma_attr7['yearCompleted'], '1984')
        self.assertEqual(carma_attr7['sector'], 'Industrial')
        self.assertEqual(carma_attr7['status'], 'Active')


if __name__ == '__main__':
    unittest.main()
