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


class CovidRecord(Model):
    cases = Property()
    deaths = Property()
    date = Property()


class Country(Model):
    __primarykey__ = "name"
    name = Property()
    pop = Property()


class State(Model):
    __primarykey__ = "fips"
    fips = Property()
    name = Property()
    pop = Property()

    located_in = RelatedTo(Country, "LOCATED_IN")
    recorded_in = RelatedFrom(CovidRecord, "RECORDED_IN")


class County(Model):
    __primarykey__ = "fips"
    fips = Property()
    name = Property()
    pop = Property()

    located_in = RelatedTo(State, "LOCATED_IN")
    recorded_in = RelatedFrom(CovidRecord, "RECORDED_IN")


class Zipcode(Model):
    __primarykey__ = "zipcode"
    zipcode = Property()
    city = Property()
    loc = Property()
    pop = Property()
    county_fips = Property()

    located_in = RelatedTo(County, "LOCATED_IN")
    recorded_in = RelatedFrom(CovidRecord, "RECORDED_IN")
