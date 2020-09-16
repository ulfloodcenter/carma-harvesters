#!/bin/bash
# Download data
wget https://s3.amazonaws.com/edap-nhdplus/NHDPlusV21/Data/NationalData/NHDPlusV21_NationalData_WBDSnapshot_Shapefile_08.7z \
  https://s3.amazonaws.com/edap-nhdplus/NHDPlusV21/Data/NationalData/NHDPlusV21_NationalData_Seamless_Geodatabase_Lower48_07.7z \
  https://s3-us-west-2.amazonaws.com/mrlc/NLCD_2016_Land_Cover_L48_20190424.zip \
  ftp://ftp.nass.usda.gov/download/res/2019_30m_cdls.zip \
  && 7z x NHDPlusV21_NationalData_WBDSnapshot_Shapefile_08.7z \
  && 7z x NHDPlusV21_NationalData_Seamless_Geodatabase_Lower48_07.7z

# Convert Flowlines to SQLite format for later querying
ogr2ogr -f "SQLite" NHDFlowline_Network.sqlite NHDPlusNationalData/NHDPlusV21_National_Seamless_Flattened_Lower48.gdb NHDFlowline_Network

# Reproject NLCD data to WGS84
gdalwarp -multi -t_srs EPSG:4326 -of GTiff -co "COMPRESS=LZW" -co "ZLEVEL=9" /vsizip/NLCD_2016_Land_Cover_L48_20190424.zip/NLCD_2016_Land_Cover_L48_20190424.img NLCD_2016_Land_Cover_L48_20190424-WGS84.tif

# Reproject CropScape Cropland Data Layer (CDL) to WGS84
gdalwarp -multi -t_srs EPSG:4326 -of GTiff -co "COMPRESS=LZW" -co "ZLEVEL=9" /vsizip/2019_30m_cdls.zip/2019_30m_cdls.img 2019_30m_cdls.tif

# Clean up
# Delete zipfiles
rm NHDPlusV21_NationalData_Seamless_Geodatabase_Lower48_07.7z NHDPlusV21_NationalData_WBDSnapshot_Shapefile_08.7z
# Delete source data
rm -rf NHDPlusNationalData/NHDPlusV21_National_Seamless_Flattened_Lower48.gdb \
  NHDPlusNationalData/NHDPlusV21_NationalData_Seamless_Geodatabase_Lower48_07.txt \
  NHDPlusNationalData/NHDPlusV21_NationalData_WBDSnapshot_FileGDB_08.txt \
  NLCD_2016_Land_Cover_L48_20190424.zip
