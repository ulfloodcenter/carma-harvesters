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
carma-huc12-extract -d $DATA_PATH -o $OUT_PATH -n carma-huc12s-2020-08-04.json -i $DATA_PATH/myhucs.txt
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
carma-county-extract -c $CENSUS_API_KEY -d $DATA_PATH -o $OUT_PATH -n carma-counties-2020-08-04.json -i $DATA_PATH/mycounties.txt
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

## Census data

* API documentation: https://api.census.gov/data.html
* Get API key here: https://api.census.gov/data/key_signup.html
