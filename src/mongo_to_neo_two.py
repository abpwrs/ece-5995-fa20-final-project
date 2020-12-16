from mongo_models import *
from neo_models import *
from tqdm import tqdm
import logging
from datetime import datetime

# SPEED PROBLEMS IN OG
# add unique constraints, and generate a python data structure that then gets unwoud in NEO -- remove OGM

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")
log_fname = f"logs/{TIMESTAMP}.log.txt"
logging.basicConfig(filename=log_fname, level=logging.WARNING)

me.connect("covid")
# create a standalone mongo_db connection (not connected to flask app)


def load_zipcodes():
    print("Loading zipcode coivd data")
    zip_data = []
    for zip_ob in tqdm(Zips.objects):
        try:
            zip2fip = Zips2Fips.objects(zip=zip_ob.zipcode)[0]
            county_fips = zip2fip.stcountyfp
            zip_data.append(
                {
                    "zipcode": zip_ob.zipcode,
                    "county_fips": county_fips,
                    "city": zip_ob.city,
                    "loc": zip_ob.loc,
                    "pop": zip_ob.pop,
                }
            )
        except IndexError as e:
            logging.warning(f"NO FIP FOR Zips(zipcode={zip_ob.zipcode})")
        
    q = """
    UNWIND $data_d AS data
    MERGE (z:Zipcode { zipcode: data.zipcode, county_fips: data.county_fips, city: data.city, loc: data.loc, pop: data.pop})
    """
    graph_db.run(q, data_d=zip_data)


def load_counties():
    print("Loading county coivd data")
    county_data = []
    for county_ob in tqdm(CovidUSCounties.objects):
        county_data.append(
            {
                # county data
                "fips" : str(county_ob.fips).zfill(5),
                "name": county_ob.county,
                "state": county_ob.state,

                # covid record data
                "cases": county_ob.cases,
                "deaths": county_ob.deaths,
                "date": county_ob.date
            }
        )

    # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    # load data in batches
    def divide_chunks(l, n): 
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    data = list(divide_chunks(county_data, 10000))
    for batch in tqdm(data):
        q = """
        UNWIND $data_d AS data
        MERGE (c:County { fips: data.fips, name: data.name, state: data.state })
        MERGE (c)<-[r:RECORDED_IN]-(covid:CovidRecord { cases: data.cases, deaths: data.name, date: data.date })
        """
        graph_db.run(q, data_d=batch)

    # link zips to counties
    q = """
    MATCH (c:County)
    WITH c
    MATCH (z:Zipcode {county_fips: c.fips})
    MERGE (c)<-[r:LOCATED_IN]-(z)
    """
    graph_db.run(q)

    # Sum population for each county
    q = f"MATCH (c:County)<-[:LOCATED_IN]-(z:Zipcode) WITH c, SUM(z.pop) AS c_pop SET c.pop = c_pop"
    graph_db.run(q)


def load_states():
    print("Loading state covid data")
    state_data = []
    for state_ob in tqdm(CovidUSStates.objects):
        state_data.append(
            {
                # county data
                "fips" : str(state_ob.fips).zfill(2),
                "name": state_ob.state,

                # covid record data
                "cases": state_ob.cases,
                "deaths": state_ob.deaths,
                "date": state_ob.date
            }
        )

    # https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    # load data in batches
    def divide_chunks(l, n): 
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    data = list(divide_chunks(state_data, 1000))
    for batch in tqdm(data):
        q = """
        UNWIND $data_d AS data
        MERGE (s:State { fips: data.fips, name: data.name })
        MERGE (s)<-[r:RECORDED_IN]-(covid:CovidRecord { cases: data.cases, deaths: data.deaths, date: data.date })
        """
        graph_db.run(q, data_d=batch)

    # link states and counties
    q = """
    MATCH (s:State)
    WITH s
    MATCH (c:County {state: s.name})
    MERGE (s)<-[r:LOCATED_IN]-(c)
    """
    graph_db.run(q)

    # Sum population for each state
    command_string = (
        f"MATCH (s:State)<-[:LOCATED_IN]-(c:County) WITH s, SUM(c.pop) AS s_pop SET s.pop = s_pop"
    )
    graph_db.run(command_string)


def load_us():
    print("Loading US covid data")

    command_string = f"MERGE (c:Country {{name: \"us\"}})"
    graph_db.run(command_string)

    us_data = []
    for state_ob in tqdm(CovidUSStates.objects):
        us_data.append(
            {
                # covid record data
                "cases": state_ob.cases if state_ob.cases else 0,
                "deaths": state_ob.deaths if state_ob.deaths else 0,
                "date": state_ob.date
            }
        )

    def divide_chunks(l, n): 
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    data = list(divide_chunks(us_data, 100))
    for batch in tqdm(data):
        q = """
        UNWIND $data_d AS data
        MATCH (c:Country { name: "us" })
        MERGE (c)<-[r:RECORDED_IN]-(covid:CovidRecord { cases: data.cases, deaths: data.deaths, date: data.date })
        """
        graph_db.run(q, data_d=batch)

    # link states and counties
    q = """
    MATCH (c:Country { name: "us" }), (s:State)
    MERGE (c)<-[r:LOCATED_IN]-(s)
    """
    graph_db.run(q)

    # Sum population for each state
    command_string = (
        f"MATCH (c:Country {{name: \"us\"  }})<-[:LOCATED_IN]-(s:State) WITH c, SUM(s.pop) AS c_pop SET c.pop = c_pop"
    )
    graph_db.run(command_string)

def load_neo4j_w_mongo_data(clear_neo_db=False):
    if clear_neo_db:
        print("wiping neo data")
        graph_db.run("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r")
        print("neo4j data wiped")


    graph_db.run("DROP CONSTRAINT county_fips_unique")
    graph_db.run("DROP CONSTRAINT zipcode_zipcode_unique")
    graph_db.run("DROP CONSTRAINT state_fips_unique")

    print("Adding neo4j field constraints to speed up reads/writes")
    graph_db.run(
        "CREATE CONSTRAINT county_fips_unique IF NOT EXISTS ON (c:County) ASSERT c.fips IS UNIQUE"
    )
    graph_db.run(
        "CREATE CONSTRAINT country_name IF NOT EXISTS ON (c:Country) ASSERT c.name IS UNIQUE"
    )
    graph_db.run(
        "CREATE CONSTRAINT zipcode_zipcode_unique IF NOT EXISTS ON (z:Zipcode) ASSERT z.zipcode IS UNIQUE"
    )
    graph_db.run(
        "CREATE CONSTRAINT state_fips_unique IF NOT EXISTS ON (s:State) ASSERT s.fips IS UNIQUE"
    )

    print("Adding neo4j indicies")
    graph_db.run("CREATE BTREE INDEX zipcode_county_fips_index IF NOT EXISTS FOR (n:Zipcode) ON (n.county_fips)")

    # plan

    # load zipcodes & extract fips for each zipcode
    load_zipcodes()

    # load county covid cases
    load_counties()

    # load state covid cases
    load_states()

    # load us covid cases
    load_us()


if __name__ == "__main__":
    load_neo4j_w_mongo_data(clear_neo_db=False)
