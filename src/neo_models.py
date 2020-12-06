from py2neo.ogm import Model, RelatedTo, RelatedFrom, Property

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


class CovidRecord(Model):
    cases = Property()
    deaths = Property()
    date = Property()
