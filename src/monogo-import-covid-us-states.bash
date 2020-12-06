#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201205

# script:
covid_us_states_csv=$(dirname $(dirname $(realpath $0)))/data/covid-19-data/us-states.csv
mongoimport --db covid --collection covid_us_states --type csv --headerline --drop --file $covid_us_states_csv


