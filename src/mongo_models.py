import mongoengine as me
from flask_mongoengine import MongoEngine

app_mongo_db = MongoEngine()


def initialize_mongo_db(app):
    app_mongo_db.init_app(app)


class CovidUS(me.Document):
    meta = {"collection": "covid_us"}
    date = me.StringField(required=True, unique=True)
    cases = me.IntField(required=True, min_value=0)
    deaths = me.IntField(required=True, min_value=0)


class CovidUSStates(me.Document):
    meta = {"collection": "covid_us_states"}
    date = me.StringField(required=True)
    state = me.StringField(required=True)
    fips = me.IntField(required=True)
    cases = me.IntField(required=True, min_value=0)
    deaths = me.IntField(required=True, min_value=0)


class CovidUSCounties(me.Document):
    meta = {"collection": "covid_us_counties"}
    date = me.StringField(required=True)
    county = me.StringField(required=True)
    state = me.StringField(required=True)
    fips = me.IntField(required=True)
    cases = me.IntField(required=True, min_value=0)
    deaths = me.IntField(required=True, min_value=0)


class CovidColleges(me.Document):
    meta = {"collection": "covid_colleges"}
    date = me.StringField(required=True)
    state = me.StringField(required=True)
    county = me.StringField(required=True)
    city = me.StringField(required=True)
    ipeds_id = me.IntField(required=True, unique=True)
    college = me.StringField(required=True)
    cases = me.IntField(required=True, min_value=0)
    notes = me.StringField(required=True)


class Zips(me.Document):
    meta = {"collection": "zips"}
    zipcode = me.StringField(required=True)
    city = me.StringField(required=True)
    loc = me.ListField(field=me.FloatField())
    pop = me.IntField(required=True, min_value=0)
    state = me.StringField(required=True)


class Zips2Fips(me.Document):
    meta = {"collection": "zips2fips"}
    zip = me.StringField(required=True)
    countyname = me.StringField(required=True)
    state = me.StringField(required=True)
    stcountyfp = me.StringField(required=True)
    classfp = me.StringField(required=True)
