#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201130

# script:

zips_json=$(dirname $(dirname $(realpath $0)))/data/zips.json
mongoimport --db covid --collection zips --drop --file $zips_json



