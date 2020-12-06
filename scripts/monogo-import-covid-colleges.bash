#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201205

# script:
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

covid_colleges_csv=$(dirname $(dirname $(realpath $0)))/data/covid-19-data/colleges/colleges.csv
mongoimport --db covid --collection covid_colleges --type csv --headerline --drop --file $covid_colleges_csv

