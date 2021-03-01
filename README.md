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

## Census data

* API documentation: https://api.census.gov/data.html
* Get API key here: https://api.census.gov/data/key_signup.html
