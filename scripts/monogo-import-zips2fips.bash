#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201130

# script:
zips2fips_csv=$(dirname $(dirname $(realpath $0)))/data/ZIP-COUNTY-FIPS_2017-06.csv
mongoimport --db covid --collection zips2fips --type csv --headerline --drop --file $zips2fips_csv



