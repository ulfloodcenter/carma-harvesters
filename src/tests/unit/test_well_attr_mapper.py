import unittest
import pathlib

from carma_harvesters.wells import WellAttributeMapper


FIXTURE_FILE = 'fixtures/louisiana_groundwater_wells_to_CARMA.json'

ATTR1 = {'AQUIFER_NA': 'CHICOT AQUIFER,UPPER SAND UNIT', 'AUTHORIZED': 'HUVAL, BRIAN J.', 'AUTHORIZ_1': '2011-09-13',
         'AVAILABLE_': None, 'AVAIL_INFO': 'N', 'BIO_ANALYS': 'N', 'CASING_DIA': '3', 'CASING_D_1': None,
         'CASING_D_2': None, 'CASING_LEN': '210', 'CASING_MAT': 'PLASTIC', 'CEMENTED_F': '10', 'CHEM_ANALY': 'N',
         'COMMENTS': None, 'CONTACT': 'HUVAL, BRIAN J.', 'DATE_COMPL': '09/13/2011', 'DATE_MEASU': '9-13-11',
         'DATE_OF_AD': None, 'DATE_PLUGG': None, 'DATE_REGIS': '9-20-11', 'DIAMETER_O': None, 'DRAWDOWN': None,
         'DRILLERS_1': '426', 'DRILLERS_N': 'HUVAL, BRIAN , WATER WELL DRILLING', 'DRILL_LOG': 'D', 'ELEC_LOG': 'N',
         'ELEVATION': '0025', 'EXTENSION1': None, 'EXTENSION_': None, 'EXTENSIO_1': None, 'GEOLOGIC_U': '112CHCTU',
         'GRAVEL_PAC': 'N', 'GROUND_EVE': None, 'HEAT_PUMP1': None, 'HEAT_PUMP_': 0, 'HOLE_DEPTH': '220',
         'IDENTIFICA': '301041092120801', 'INDUSTRIAL': None, 'INDUSTRI_1': None, 'INSPECTION': '2011-10-25',
         'INSPECTOR': 'T BROUSSARD', 'INSPECTOR_': None, 'LATITUDE': '301041', 'LATITUDE_D': 0, 'LATITUDE_M': 0,
         'LATITUDE_S': 0.0, 'LOCAL_WELL': '11461Z', 'LOCATION_C': 'DUSON', 'LOCATION_L': 'INTXN OF LA719 & RIDGE RD',
         'LOCATION_M': 0.6, 'LONGITUDE': '921208', 'LONGITUDE1': 0, 'LONGITUDE_': 0, 'LONGITUD_1': None,
         'MECHANIC_A': 'N', 'OWNERS_NAM': 'ALICE COA', 'OWNERS_NUM': None, 'OWNER_STAT': 'N', 'PARISH_COD': '28',
         'PARISH_NAM': 'LAFAYETTE', 'PARISH_NUM': '055', 'PA_DETAILS': None, 'PA_REMARKS': None, 'PA_SIGNATU': None,
         'PA_SIGNA_1': None, 'PLUGGED_BY': None, 'PLUGGED__1': None, 'PUBLIC_SUP': None, 'PUBLIC_S_1': None,
         'PUMPDOWN_C': None, 'PUMP_DETER': None, 'PUMP_DOWN_': 'G', 'PUMP_GROUN': None, 'PUMP_HOURS': None,
         'PUMP_HOU_1': 0, 'PUMP_MOTOR': None, 'PUMP_PLANN': 0, 'PUMP_PLA_1': 0, 'PUMP_PLA_2': None, 'PUMP_RATE': None,
         'PUMP_SETTI': None, 'PUMP_STATI': None, 'PUMP_TEST': 'N', 'PUMP_TEST_': None, 'QUAD_NUM': '182A',
         'RANGE': '03E', 'REMARKS': 'WWC 618 SUBCONTRACTOR', 'REPLACEMEN': 'N', 'REVISED_LA': None, 'REVISED_LO': None,
         'SCREEN_DIA': '3', 'SCREEN_D_1': None, 'SCREEN_D_2': None, 'SCREEN_INT': None, 'SCREEN_TYP': 'PLASTIC',
         'SECTION': '018', 'SEQUENCE_N': '00', 'SERIAL_NUM': None, 'SITE_ADDRE': None, 'SITE_CITY': None,
         'SITE_ZIP': None, 'SLOT_LENGT': '10', 'SLOT_SIZE': '.014', 'SOURCE_OF_': 'D', 'STATE_CODE': '22',
         'TOWNSHIP': '10S', 'USE_DESCRI': 'domestic', 'WATER_LEVE': '61', 'WATER_WELL': 559291,
         'WATER_WE_1': '055-11461Z', 'WELL_DEPTH': '220', 'WELL_STATU': 'Active', 'WELL_SUBUS': None, 'WELL_USE': 'H',
         'WWO_SEQ_NU': 18891.0, 'X_LONGDD': -92.20222222, 'YIELD': None, 'YIELD_MEAS': None, 'Y_LATDD': 30.17805556}

ATTR2 = {'AQUIFER_NA': 'CHICOT AQUIFER,UPPER SAND UNIT', 'AUTHORIZED': None, 'AUTHORIZ_1': None,
         'AVAILABLE_': 'Driller Log, Water Level', 'AVAIL_INFO': 'W', 'BIO_ANALYS': None, 'CASING_DIA': '2',
         'CASING_D_1': None, 'CASING_D_2': None, 'CASING_LEN': None, 'CASING_MAT': 'PLASTIC', 'CEMENTED_F': None,
         'CHEM_ANALY': None, 'COMMENTS': None, 'CONTACT': None, 'DATE_COMPL': '06/96', 'DATE_MEASU': '06/30/96',
         'DATE_OF_AD': '1997-04-10', 'DATE_PLUGG': None, 'DATE_REGIS': '08/96', 'DIAMETER_O': None, 'DRAWDOWN': None,
         'DRILLERS_1': '256', 'DRILLERS_N': 'FOREST, SHELDON', 'DRILL_LOG': 'D', 'ELEC_LOG': None, 'ELEVATION': '25',
         'EXTENSION1': None, 'EXTENSION_': None, 'EXTENSIO_1': None, 'GEOLOGIC_U': '112CHCTU', 'GRAVEL_PAC': 'N',
         'GROUND_EVE': None, 'HEAT_PUMP1': None, 'HEAT_PUMP_': 0, 'HOLE_DEPTH': '210', 'IDENTIFICA': '300836092091002',
         'INDUSTRIAL': None, 'INDUSTRI_1': None, 'INSPECTION': None, 'INSPECTOR': None, 'INSPECTOR_': None,
         'LATITUDE': '300836', 'LATITUDE_D': 0, 'LATITUDE_M': 0, 'LATITUDE_S': 0.0, 'LOCAL_WELL': '8696Z',
         'LOCATION_C': None, 'LOCATION_L': None, 'LOCATION_M': 0.0, 'LONGITUDE': '920910', 'LONGITUDE1': 0,
         'LONGITUDE_': 0, 'LONGITUD_1': None, 'MECHANIC_A': None, 'OWNERS_NAM': 'KEITH BERNARD', 'OWNERS_NUM': None,
         'OWNER_STAT': None, 'PARISH_COD': '28', 'PARISH_NAM': 'LAFAYETTE', 'PARISH_NUM': '055', 'PA_DETAILS': None,
         'PA_REMARKS': None, 'PA_SIGNATU': None, 'PA_SIGNA_1': None, 'PLUGGED_BY': None, 'PLUGGED__1': None,
         'PUBLIC_SUP': None, 'PUBLIC_S_1': None, 'PUMPDOWN_C': None, 'PUMP_DETER': None, 'PUMP_DOWN_': None,
         'PUMP_GROUN': None, 'PUMP_HOURS': None, 'PUMP_HOU_1': 0, 'PUMP_MOTOR': None, 'PUMP_PLANN': 0, 'PUMP_PLA_1': 0,
         'PUMP_PLA_2': None, 'PUMP_RATE': None, 'PUMP_SETTI': None, 'PUMP_STATI': None, 'PUMP_TEST': None,
         'PUMP_TEST_': None, 'QUAD_NUM': '182A', 'RANGE': '03E', 'REMARKS': None, 'REPLACEMEN': None,
         'REVISED_LA': None, 'REVISED_LO': None, 'SCREEN_DIA': '2', 'SCREEN_D_1': None, 'SCREEN_D_2': None,
         'SCREEN_INT': '205-210', 'SCREEN_TYP': None, 'SECTION': '027', 'SEQUENCE_N': '02', 'SERIAL_NUM': None,
         'SITE_ADDRE': None, 'SITE_CITY': None, 'SITE_ZIP': None, 'SLOT_LENGT': None, 'SLOT_SIZE': None,
         'SOURCE_OF_': 'D', 'STATE_CODE': '22', 'TOWNSHIP': '10S', 'USE_DESCRI': 'domestic', 'WATER_LEVE': '48.00',
         'WATER_WELL': 447561, 'WATER_WE_1': '055-8696Z', 'WELL_DEPTH': '210', 'WELL_STATU': 'Active',
         'WELL_SUBUS': None, 'WELL_USE': 'H', 'WWO_SEQ_NU': 161988.0, 'X_LONGDD': -92.15277778, 'YIELD': None,
         'YIELD_MEAS': None, 'Y_LATDD': 30.14333333}

ATTR3 = {'AQUIFER_NA': '[TO BE DETERMINED]', 'AUTHORIZED': None, 'AUTHORIZ_1': None,
         'AVAILABLE_': 'Driller Log, Water Level', 'AVAIL_INFO': 'W', 'BIO_ANALYS': None, 'CASING_DIA': '2',
         'CASING_D_1': None, 'CASING_D_2': None, 'CASING_LEN': None, 'CASING_MAT': 'PLASTIC', 'CEMENTED_F': None,
         'CHEM_ANALY': None, 'COMMENTS': None, 'CONTACT': None, 'DATE_COMPL': "LATE 1970's", 'DATE_MEASU': '06/25/10',
         'DATE_OF_AD': '2010-07-02', 'DATE_PLUGG': None, 'DATE_REGIS': '06/10', 'DIAMETER_O': None, 'DRAWDOWN': None,
         'DRILLERS_1': '522', 'DRILLERS_N': 'KOURCO', 'DRILL_LOG': 'D', 'ELEC_LOG': None, 'ELEVATION': '25',
         'EXTENSION1': None, 'EXTENSION_': None, 'EXTENSIO_1': None, 'GEOLOGIC_U': '00000000', 'GRAVEL_PAC': 'N',
         'GROUND_EVE': None, 'HEAT_PUMP1': None, 'HEAT_PUMP_': 0, 'HOLE_DEPTH': '54', 'IDENTIFICA': '301054092061501',
         'INDUSTRIAL': None, 'INDUSTRI_1': None, 'INSPECTION': None, 'INSPECTOR': None, 'INSPECTOR_': None,
         'LATITUDE': '301054', 'LATITUDE_D': 0, 'LATITUDE_M': 0, 'LATITUDE_S': 0.0, 'LOCAL_WELL': '11300Z',
         'LOCATION_C': None, 'LOCATION_L': None, 'LOCATION_M': 0.0, 'LONGITUDE': '920615', 'LONGITUDE1': 0,
         'LONGITUDE_': 0, 'LONGITUD_1': None, 'MECHANIC_A': None, 'OWNERS_NAM': 'SOUTHWEST FOODS', 'OWNERS_NUM': 'MW-2',
         'OWNER_STAT': None, 'PARISH_COD': '28', 'PARISH_NAM': 'LAFAYETTE', 'PARISH_NUM': '055', 'PA_DETAILS': None,
         'PA_REMARKS': None, 'PA_SIGNATU': None, 'PA_SIGNA_1': None, 'PLUGGED_BY': None, 'PLUGGED__1': None,
         'PUBLIC_SUP': None, 'PUBLIC_S_1': None, 'PUMPDOWN_C': None, 'PUMP_DETER': None, 'PUMP_DOWN_': None,
         'PUMP_GROUN': None, 'PUMP_HOURS': None, 'PUMP_HOU_1': 0, 'PUMP_MOTOR': None, 'PUMP_PLANN': 0, 'PUMP_PLA_1': 0,
         'PUMP_PLA_2': None, 'PUMP_RATE': None, 'PUMP_SETTI': None, 'PUMP_STATI': None, 'PUMP_TEST': None,
         'PUMP_TEST_': None, 'QUAD_NUM': '182B', 'RANGE': '04E', 'REMARKS': None, 'REPLACEMEN': None,
         'REVISED_LA': None, 'REVISED_LO': None, 'SCREEN_DIA': '2', 'SCREEN_D_1': None, 'SCREEN_D_2': None,
         'SCREEN_INT': '43-53', 'SCREEN_TYP': None, 'SECTION': '007', 'SEQUENCE_N': '01', 'SERIAL_NUM': None,
         'SITE_ADDRE': None, 'SITE_CITY': None, 'SITE_ZIP': None, 'SLOT_LENGT': None, 'SLOT_SIZE': None,
         'SOURCE_OF_': 'D', 'STATE_CODE': '22', 'TOWNSHIP': '08S', 'USE_DESCRI': 'monitor', 'WATER_LEVE': '45.82',
         'WATER_WELL': 450161, 'WATER_WE_1': '055-11300Z', 'WELL_DEPTH': '53', 'WELL_STATU': 'Active',
         'WELL_SUBUS': None, 'WELL_USE': 'M', 'WWO_SEQ_NU': 0.0, 'X_LONGDD': -92.10416667, 'YIELD': None,
         'YIELD_MEAS': None, 'Y_LATDD': 30.18166667}


class TestWellAttributeMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_path = pathlib.Path(__file__).parent.parent.joinpath(FIXTURE_FILE)

    def test_well_attr_mapper(self):
        mapper = WellAttributeMapper(self.fixture_path)
        import pdb; pdb.set_trace()
        carma_attr1 = mapper.map_well_attributes(ATTR1)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
