#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201205

# script:
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

covid_us_counties_csv=$(dirname $(dirname $(realpath $0)))/data/covid-19-data/us-counties.csv
mongoimport --db covid --collection covid_us_counties --type csv --headerline --drop --file $covid_us_counties_csv


