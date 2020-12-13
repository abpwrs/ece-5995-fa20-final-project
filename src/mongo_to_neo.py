from .mongo_models import *
from .neo_models import *


def load_neo4j_w_mongo_data(clear_neo_db=True):
    if clear_neo_db:
        graph_db.run(
            """
            MATCH (n)
            OPTIONAL MATCH (n)-[r]-()
            DELETE n, r")
            """
        )
        print("neo4j data wiped")

    # plan

    # load zipcodes & extract fips for each zipcode
    

    # load county covid cases
    # - create relation between covid records and county
    # - create relation between zipcodes and counties

    # load state covid cases
    # - create realtion between covid records and state
    # - create relation between states and counties

    # load us covid cases
    # - create relation between covid records and us country node
    # - create realtion between all states and the us country node
