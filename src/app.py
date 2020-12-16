from flask import Flask, jsonify, render_template, redirect, request
from flask_assets import Bundle, Environment
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap

from .mongo_models import (
    CovidColleges,
    CovidUS,
    CovidUSCounties,
    CovidUSStates,
    Zips,
    Zips2Fips,
    initialize_mongo_db,
)
from .neo_models import *

# init app
app = Flask(__name__)
Bootstrap(app)
datepicker(app)
# config mongodb
app.config["MONGODB_SETTINGS"] = {
    "db": "covid",
}

# init db
initialize_mongo_db(app)

# flask assets - styling
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle("index.scss", filters="pyscss", output="gen/all.css")
assets.register("scss_all", scss)

# TODO:
QUERIES = ["/query1", "/query2", "/query3"]

# define app routes
@app.route("/", methods=["GET"])
def startup():
    context = {}
    context["queries"] = [
        "Why is Harsh the best?",
        "Why is Alex poopy?",
        "Why is Colton?",
    ]
    context["queries"] = [(i, txt) for i, txt in enumerate(context["queries"])]
    return render_template("index.html", context=context)


@app.route("/pick", methods=["POST"])
def pick():
    print("\n\n", request.form, "\n\n")
    print(request.form)
    return redirect(QUERIES[int(request.form.get("queries"))])


@app.route("/text/<text>")
def index(text=None):
    context = {}
    if text:
        context["text"] = text
        context["covid"] = [i for i in range(5)]
    return render_template("index.html", context=context)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     names = ["Harsh", "Alex", "Colton"]
#     context = {}
#     context['names'] = names
#     return render_template("index.html", context=context)


# @app.route("/submission", methods=["POST"])
# def dropdown_submission():
#     print("\n\nNAME:", request.form['names'], "\n\n")
#     return redirect("/")


@app.route("/query1", methods=["GET", "POST"])
def query1():
    names = ["Harsh", "Alex", "Colton"]
    states = [
        "Alabama",
        "Alaska",
        "American Samoa",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "District of Columbia",
        "Florida",
        "Georgia",
        "Guam",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Minor Outlying Islands",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Northern Mariana Islands",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Puerto Rico",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "U.S. Virgin Islands",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]
    context = {}
    context["names"] = names
    context["states"] = states
    return render_template("query1.html", context=context)


@app.route("/submission", methods=["POST"])
def dropdown_submission():
    # print("\n\n", request.form, "\n\n")
    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    # print(request.form)
    asdf = "asdf"
    context = {}
    context["output"] = request.form.get("states")
    print(context.get("output"))
    return render_template("query1.html", context=context)


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

if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
