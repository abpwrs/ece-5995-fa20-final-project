from flask import Flask, jsonify, render_template
from flask_assets import Bundle, Environment

# from flask.ext.scss import Scss
from flask_mongoengine import MongoEngine

from .mongo_models import (
    CovidUS,
    CovidUSStates,
    CovidUSCounties,
    CovidColleges,
    Zips,
    Zips2Fips,
)
from .neo_models import *

# init app
app = Flask(__name__)
# config mongodb
app.config["MONGODB_SETTINGS"] = {
    "db": "covid",
}

# init db
mongo_db = MongoEngine(app)

# flask assets - styling
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle("index.scss", filters="pyscss", output="all.css")
assets.register("scss_all", scss)


# define app routes
@app.route("/")
def index():
    return render_template("index.html")


# start mongodb test routes
# ####################################################
@app.route("/first/covidus")
def covidus():
    covidus_data = CovidUS.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


@app.route("/first/covidusstates")
def covidusstates():
    covidus_data = CovidUSStates.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


@app.route("/first/coviduscounties")
def coviduscounties():
    covidus_data = CovidUSCounties.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


@app.route("/first/covidcolleges")
def covidcolleges():
    covidus_data = CovidColleges.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


@app.route("/first/zips")
def zips():
    covidus_data = Zips.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


@app.route("/first/zips2fips")
def zips2fips():
    covidus_data = Zips2Fips.objects().first()
    print(covidus_data, type(covidus_data))
    return jsonify(covidus_data)


# ####################################################
# end mongodb test routes
