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
carma-huc12-extract -d $DATA_PATH -o $DATA_PATH -n carma-huc12s-2020-08-04.json -i $DATA_PATH/myhucs.txt
```

The NHDPlusV2 data will be read from a directory called "$DATA_PATH",
output will be stored in a directory call "$DATA_PATH", the name of the CARMA file with HUC12 definitions will be
"carma-huc12s-2020-08-04.json". The IDs of the HUC12s to extract will be read from a file called
"$DATA_PATH/myhucs.txt". The contents of this file must be one more more HUC12 IDs, one per line, e.g.:
```
041000030706
040500011602
```

