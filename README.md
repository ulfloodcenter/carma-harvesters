# CARMA harvesters

## Building the container
```
docker-compose build
```

## Running the container
```
docker-compose run carma
```

Once in the container, you can download underlying GIS data by running `download-data.sh` (see below).

## Using the container

### Download and extract NHDPlusV2 national seemless and NLCD data necessary to extract HUC12 information needed by CARMA
```
cd data
download-data.sh
```
The download and extraction will take a while. Go get some coffee (or maybe lunch).

### Extract HUC12s in CARMA format (after NHDPlusV2 data have been downloaded)
```
carma-huc12-extract -d $DATA_PATH -o $OUT_PATH -n carma-out.json -i $DATA_PATH/myhucs.txt
```

> Note: use `-v` for verbose/debug output.

The NHDPlusV2 data will be read from a directory called "$DATA_PATH",
output will be stored in a directory call "$OUT_PATH", the name of the CARMA file with HUC12 definitions will be
"carma-huc12s-2020-08-04.json". The IDs of the HUC12s to extract will be read from a file called
"$DATA_PATH/myhucs.txt". The contents of this file must be one more more HUC12 IDs, one per line, e.g.:
```
041000030706
040500011602
```

### Extract counties in CARMA format (after TIGER data have been downloaded)
```
carma-county-extract -c $CENSUS_API_KEY -d $DATA_PATH -o $OUT_PATH -n carma-out.json -i $DATA_PATH/mycounties.txt
```

> Note: use `-v` for verbose/debug output.

The TIGER county data will be read from a directory called "$DATA_PATH",
output will be stored in a directory call "$OUT_PATH", the name of the CARMA file with county definitions will be
"carma-counties-2020-08-04.json". The IDs of the counties to extract will be read from a file called
"$DATA_PATH/mycounties.txt". The contents of this file must be one more more state or state+county FIPS codes,
one per line, e.g.:
```
22
28109
```

> A two-digit FIPS indicates that all counties for the entire state should be extracted.
> A five-digit FIPS indicates that a single county should be extracted.

### Generate sub-HUC12 areas from county and HUC12 definitions
```
carma-subhuc12-generate -d $DATA_PATH -c carma-out.json
```

The script `carma-subhuc12-generate` will generate sub-HUC12 areas by computing the overlap between HUC12 and county
geographies in a CARMA data file; a sub-HUC12 area is the portion of a HUC12 that lies in a given county. Consequently,
the CARMA data file (`carma-out.json` in the example) must have one or more definitions for `HUC12Watersheds` and
`Counties`. The following items are stored for each sub-HUC12 area: 1. sub-HUC12 geography; 2. area (total area, crops);
3. landcover (high-density development); and 4. stream stats data (max order, min level, mean annual flow).

### Export CARMA geographies to GeoJSON
Export HUC12, county, and sub-HUC12 definitions from a CARMA data file into GeoJSON FeatureCollection file using the
`carma-geojson-export` command:
```
carma-geojson-export -c carma-out.json -g carma-out.geojson
```

All HUC12, county, and sub-HUC12 geometries encountered in a CARMA data file will be output as features
in a FeatureCollection GeoJSON file, which can be useful for display and debugging purposes. Each CARMA attribute will
be output as a property for each feature.

### Download county water use data from NWIS
```
carma-download-nwis-wateruse -c carma-out.json -y 2010
```

> Note: use `-v` for verbose/debug output.

To download water use data for another year:
```
carma-download-nwis-wateruse -c carma-out.json -y 2015
```

By default, the new year's data will be added to any existing water use data. To overwrite
use `--overwrite`.

### Import groundwater well data
Sadly, there is no national source of groundwater well location data. Still we can import groundwater well location
information into CARMA from state- or jurisdiction-specific format:
```
carma-groundwater-well-import -c carma-out.json -w $MY_WELL_DATA -a $MY_WELL_ATTRIBUTE_MAPPING
```

where:
- `-w` specifies a point GIS dataset (i.e. a file readible by OGR/fiona) containing well locations along with the
following attributes: sector, status, and year completed.
- `-a` specifies a JSON file specifying how well attributes defined in the GIS dataset should be mapped to CARMA
schema format. See 'Groundwater well attribute mapping JSON format' below for example.

#### Groundwater well attribute mapping JSON format
Below is an example for extracting CARMA-formatted wells attribute data from Louisiana
[water wells registration data](https://www.sonris.com).
```json
{
    "attributes": {
        "sector": "USE_DESCRI",
        "status": "WELL_STATU",
        "yearCompleted": "DATE_COMPL"
    },
    "values": {
        "USE_DESCRI": {
            "Public Supply": ["public supply", "rural public supply",
                "commercial public supply", "municipal public supply", "institution public supply"],
            "Domestic": ["domestic"],
            "Commercial": ["commercial public supply", "aquaculture", "oil/gas well rig supply"],
            "Industrial": ["industrial\\s*\\.*"],
            "Power Generation": ["power generation"],
            "Irrigation": ["irrigation"],
            "Livestock": ["livestock"]
        },
        "WELL_STATU": {
            "Active": ["Active"],
            "Abandoned": ["Abandoned"],
            "Destroyed": ["Destroyed"],
            "Inactive": ["Inactive"]
        },
        "DATE_COMPL": [
            "(?P<month>[0-9]{1,2})/(?P<year>[0-9]{2,4})",
            "(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<year>[0-9]{2,4})",
            "CIRCA (?P<month>[0-9]{1,2})/(?P<year>[0-9]{2})",
            {"LATE 1970's": "1979"},
            {"LATE 1980's": "1989"},
            {"PRE/1985": "1984"}
        ]
    }
}
```

The `attributes` object specifies a one-to-one mapping between CARMA well data attribute names
and well attribute names in the input point GIS file.

The `values` object specifies a one-to-many mapping GIS file attribute name and
[regular expressions](https://docs.python.org/3/library/re.html) or mappings that can be used to
extract CARMA-compatible attribute values from attribute values stored in the GIS file.

For CARMA well data attributes that are enumerated values, the value mapping should map to an object that maps each
CARMA attribute value to one or more patterns to use to extract that CARMA attribute value from the
GIS attribute value.

For CARMA well data attributes that can be any value (currently only 'yearCompleted'), the value mapping should map
to either: (1) a list of regular expressions to use to extract that CARMA attribute value from the
GIS attribute value; or (2) a static mapping between a GIS attribute value and CARMA attribute value, for example:
GIS attribute values of "LATE 1970's" should be written as "1979" to the 'yearComplete' CARMA attribute.

### Define a WaSSI analysis
To start a new WaSSI analysis, it is necessary to first create a new WaSSI definition in your CARMA file:
```
carma-wassi-init -c carma-out.json -cy 2019 -dy 2016 -wy 2016 -d "My WaSSI analysis description"
```

where:
- `-cy` specifies the year to use for crop data in the analysis (required)
- `-dy` specifies the year to use for developed area data in the analysis (required)
- `-wy` specifies the year to use for groundwater well count data (required)
- `-d` specifies the a description to use for the WaSSI analysis (optional)

### Generate disaggregation weights for WaSSI analysis
WaSSI analysis involves disaggregating county-level water use data to the HUC12 scale. This disaggregation relies on
a series of weights for both surface water and groundwater:
```
carma-wassi-weight-generate -c carma-out.json -i $UUID_OF_WASSI_ANALYSIS
```

where:
- `-i` specifies the UUID of a WaSSI analysis definition stored in `carma-out.json`.

> Note that `carma-out.json` must have 'SubHUC12Watersheds' and `Counties` defined.

## Census data

* API documentation: https://api.census.gov/data.html
* Get API key here: https://api.census.gov/data/key_signup.html

## Dev environment setup

### macOS (Homebrew)

Install OS dependencies
```
brew update
brew install python numpy gdal spatialite-tools proj
```

Setup Python
```
python3 -m venv venv
source venv/bin/activate
```

If running on AppleSilicon, do this afterwards:
```
pip install Cython
pip install --no-binary :all: --no-use-pep517 numpy
pip install --no-deps pygeos
pip install git+https://github.com/Toblerity/Fiona#egg=fiona
```

Install CARMA Python dependencies (unless using AppleSilicon)
```
cd src
pip install -r requirements.txt
```

Install CARMA Python dependencies (ONLY if using AppleSilicon)
```
cd src
pip install -r requirements-aarch64.txt
```

Install CARMA
```
carma-schema
python setup.py install
cd ..
python setup.py install
```

