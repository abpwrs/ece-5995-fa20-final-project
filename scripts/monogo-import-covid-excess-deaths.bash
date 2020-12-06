#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201205

# script:
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

covid_excess_deaths_csv=$(dirname $(dirname $(realpath $0)))/data/covid-19-data/excess-deaths/deaths.csv
mongoimport --db covid --collection covid_excess_deaths --type csv --headerline --drop --file $covid_excess_deaths_csv


