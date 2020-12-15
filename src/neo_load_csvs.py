from neo_models import *


# load zipcodes
# zipcode,city,loc,pop,state
command = """
:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "file:///zips.csv" AS row
MERGE (z:Zipcode {zipcode: row.zipcode, city:row.city, loc: row.loc, pop: row.pop})
"""
graph_db.run(command)


# load counties
# date,county,state,fips,cases,deaths
command = """
:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "file:///dropped-us-counties.csv" AS row
MERGE (c:County {fips: row.fips, name:row.county, state: row.state})
WITH c, row
MERGE (covid:CovidRecord {cases: toInteger(row.cases), date: row.date, deaths: toInteger(row.deaths)})
MERGE (c)<-[r:RECORDED_IN]-(covid);
"""
graph_db.run(command)


# load zip-fip mapping
# zip,countyname,state,stcountyfp,classfp
command = """
:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM "file:///ZIP-COUNTY-FIPS_2017-06.csv" AS row
MATCH (c:County {fips: row.stcountyfp} ), (z:Zipcode {zipcode: row.zip})
MERGE (c)<-[r:LOCATED_IN]-(z)
"""
graph_db.run(command)