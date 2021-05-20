import sqlite3
import csv
import os
import pkg_resources
import logging


logger = logging.getLogger(__name__)

CARMA_HARVESTERS_RSRC_KEY = 'carma_harvesters'
EIA_FORM_860_SCHEDULE_2_PATH = 'data/2___Plant_Y2019.csv'


class PowerPlantLocations:
    def __init__(self):
        self.plant_loc_in_path = pkg_resources.resource_filename(CARMA_HARVESTERS_RSRC_KEY,
                                                                 EIA_FORM_860_SCHEDULE_2_PATH)
        if not os.path.exists(self.plant_loc_in_path) or not os.access(self.plant_loc_in_path, os.R_OK):
            raise Exception("EIA FORM 860 schedule 2 power plant location file cannot be found or cannot be read.")
        logger.debug(f"Plant location input path: {self.plant_loc_in_path}")

        # Create in-memory database
        self.conn = sqlite3.connect(':memory:')
        # Enable Spatialite extension (so that we can do spatial queries)
        self.conn.enable_load_extension(True)
        self.conn.execute('SELECT load_extension("mod_spatialite")')
        self.conn.enable_load_extension(False)
        self.conn.execute('SELECT InitSpatialMetaData()')

        # Create table to hold plant location data
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS eia_form860_plant_loc
        (
        plant_code INTEGER PRIMARY KEY,
        longitude TEXT,
        latitude TEXT
        )
        ''')
        cur.execute('''SELECT AddGeometryColumn
        (
        'eia_form860_plant_loc',
        'geom_nad83',
        4269,
        'POINT',
        'XY',
        0
        )
        ''')
        cur.execute('''SELECT CreateSpatialIndex
        (
        'eia_form860_plant_loc',
        'geom_nad83'
        )
        ''')

        # Read plant data from CSV into database
        with open(self.plant_loc_in_path, 'r') as plant_loc_file:
            plant_loc_reader = csv.reader(plant_loc_file, delimiter=',')
            for row_num, row in enumerate(plant_loc_reader, start=1):
                if row_num > 2:
                    plant_id = int(row[2])
                    long = row[10]
                    lat = row[9]
                    try:
                        geom_text = f"POINT({long} {lat})"
                        cur.execute("""INSERT INTO eia_form860_plant_loc
                        (plant_code, longitude, latitude, geom_nad83)
                        VALUES (?, ?, ?, GeomFromText(?, 4269))""",
                                    (plant_id, long, lat, geom_text))
                    except sqlite3.IntegrityError as e:
                        logger.error(("Unable to load plant location data, values where: "
                                      f"plant_id: {plant_id}, long: |{long}|, lat: |{lat}|, geom_text: {geom_text}")
                                     )
                        raise e
        cur.close()

    def get_lon_lat_for_plant(self, plant_code: int) -> (str, str):
        cur = self.conn.cursor()
        cur.execute("""SELECT longitude, latitude 
        FROM eia_form860_plant_loc
        WHERE plant_code=? 
        """,
                    (plant_code,))
        return cur.fetchone()
