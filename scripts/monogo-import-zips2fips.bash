#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201130

# script:
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

zips2fips_csv=$(dirname $(dirname $(realpath $0)))/data/ZIP-COUNTY-FIPS_2017-06.csv
mongoimport --db covid --collection zips2fips --type csv --drop --file $zips2fips_csv --columnsHaveTypes --fields="zip.string(),countyname.string(),state.string(),stcountyfp.string(),classfp.string()" 





