#!/usr/bin/env bash
# Author: "alexander"
# Date: 20201130

# script:
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

zips_json=$(dirname $(dirname $(realpath $0)))/data/zips.json
mongoimport --db covid --collection zips --drop --file $zips_json



