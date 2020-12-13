from py2neo.ogm import Graph, Model, Property, RelatedFrom, RelatedTo


graph_db = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j"))

# example write
# s = State()
# s.fips = 'asdf'
# s.namee = 'fdsa'
# s.pop=1
# graph_db.push(s)

# example query
# graph_db.run("MATCH (n:State) RETURN n")


# TODO: define relationships
class Country(Model):
    name = Property()
    pop = Property()


class State(Model):
    fips = Property()
    name = Property()
    pop = Property()


class County(Model):
    fips = Property()
    name = Property()
    pop = Property()


class Zipcode(Model):
    zipcode = Property()
    city = Property()
    loc = Property()
    pop = Property()
    county_fips = Property()


class CovidRecord(Model):
    cases = Property()
    deaths = Property()
    date = Property()
