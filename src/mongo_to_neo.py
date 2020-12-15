from mongo_models import *
from neo_models import *
from tqdm import tqdm
import logging
from datetime import datetime

from py2neo.ogm import RelatedObjects, RelatedTo
from py2neo import Relationship

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")  
log_fname = f"logs/{TIMESTAMP}.log.txt"
logging.basicConfig(filename=log_fname, level=logging.WARNING)

me.connect("covid")
# create a standalone mongo_db connection (not connected to flask app)

def load_zipcodes():
    print("Loading zipcode data")
    for zip in tqdm(Zips.objects):
        zipcode_value = zip.zipcode
        # for each zipcode grab the county FIPS code
        try:
            zip2fip = Zips2Fips.objects(zip=zipcode_value)[0]
            county_fips = zip2fip.stcountyfp
            # print(zipcode_value, county_fips)
            # print(type(zipcode_value), type(county_fips))
            neo_zip_node = Zipcode()
            neo_zip_node.zipcode = zipcode_value
            neo_zip_node.city = zip.city
            neo_zip_node.loc = zip.loc
            neo_zip_node.pop = zip.pop
            neo_zip_node.county_fips = county_fips
            graph_db.merge(neo_zip_node)

        except IndexError as e:
            logging.warning(f"NO FIP FOR Zips(zipcode={zipcode_value})")

def load_counties():
    print("Loading county coivd data")

    for county_ob in CovidUSCounties.objects:
        county_name = county_ob.county
        print(county_name)
        try:
            neo_county_node = County()
            neo_county_node.fips = county_ob.fips
            neo_county_node.name = county_name

            # no relations to this node (yet)
            graph_db.merge(neo_county_node)
        
            zipcodes_in_county = list(Zipcode.match(graph_db).where(f"_.county_fips = {county_ob.fips}"))

            # print(zipcodes_in_county)
            # -- loop and create relations to the neo_county_noed
            for zipcode_node in zipcodes_in_county:
                command_string = f"MATCH (c:County {{fips:{neo_county_node.fips}}}), (z:Zipcode {{zipcode:\"{zipcode_node.zipcode}\"}}) MERGE (c)<-[:LOCATED_IN]-(z) RETURN c, z"
                graph_db.run(command_string)


            # create covid record for the county
            covid_record = CovidRecord()
            covid_record.cases = county_ob.cases
            covid_record.deaths = county_ob.deaths
            covid_record.date = county_ob.date
            covid_record = graph_db.merge(covid_record)

            # nope, it will be mapped to a County, State or US, using [:RECORDED_IN]
            
            # TODO: create covid record and map it to the county object
            command_string = f"MATCH (c:County {{fips:{neo_county_node.fips}}}), (covid:CovidRecord {{id: {covid_record.__primaryvalue__}}}) MERGE (c)<-[:RECORDED_IN]-(covid) RETURN c, covid"
            graph_db.run(command_string)
        except Exception as e:
            logging.warning(e)

        # Sum population for each county
        command_string = f"MATCH (c:County)<-[:LOCATED_IN]-(z:Zipcode) SET c.pop = SUM(z.pop)"
        graph_db.run(command_string)

# def load_states():
#     print("Loading state covid data")

#     for state_ob in CovidUSStates.objects:
#         state_name = state_ob.state
#         try:
#             neo_state_node = State()
#             neo_state_node.fip = state_ob.fips
#             neo_state_node.name = state_name

# def load_us():
#     print("Loading US covid data")
#     for country_ob in CovidUS.objects:
#         try:
#             neo_country_node = Country()


def load_neo4j_w_mongo_data(clear_neo_db=False):
    if clear_neo_db:
        print("wiping neo data")
        graph_db.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r")
        print("neo4j data wiped")

    # plan

    # load zipcodes & extract fips for each zipcode

    # TODO: uncomment before submission
    load_zipcodes()

    # load county covid cases
    # - create relation between covid records and county
    # - create relation between zipcodes and counties
    # CovidUSCounties -- mongo_models
    # County -- neo_models
    load_counties()

    # load state covid cases
    # - create realtion between covid records and state
    # - create relation between states and counties
    # load_states()


    # load us covid cases
    # - create relation between covid records and us country node
    # - create realtion between all states and the us country node
    # load_us()


if __name__ == "__main__":
    load_neo4j_w_mongo_data(clear_neo_db=False)
