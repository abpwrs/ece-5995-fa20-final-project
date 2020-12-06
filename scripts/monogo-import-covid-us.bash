#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201205

# script:
covid_us_csv=$(dirname $(dirname $(realpath $0)))/data/covid-19-data/us.csv
mongoimport --db covid --collection covid_us --type csv --headerline --drop --file $covid_us_csv

