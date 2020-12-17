from flask import Flask, jsonify, render_template, redirect, request
from flask_assets import Bundle, Environment
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from .queries import *

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
js = Bundle("main.js", filters="jsmin", output="gen/all.js")
assets.register("js_all", js)



# TODO:
QUERY_ROUTES = ["/query1", "/query2", "/query3", "/query4", "/query5", "/query6"]
QUERY_TEXT = [
    "Number of cases in a state over a date range",  # params for state, start date, and end date               - get_cases_by_state
    "Number of cases in a county over a date range",  # params for state, county, start date, and end date      - get_cases_by_county
    
    "Rank counties by net cases",  # params for start, end date, and state, and county                          - get_ranked_cases_by_county
    "Rank counties by cases as percentage of population",  # params for start, end date, state, and county      - get_ranked_cases_by_county_as_pop_percentage

    "Rank states by net cases",  # params for start, end date                                                   - get_ranked_cases_by_state
    "Rank states by cases as percentage of population",  # params for start, end date,                          - get_ranked_cases_by_state_as_pop_percentage
]
STATES = sorted(get_states())

# define app routes
@app.route("/", methods=["GET"])
def index():
    context = {}
    context["queries"] = QUERY_TEXT
    context["queries"] = [(i, txt) for i, txt in enumerate(context["queries"])]
    return render_template("index.html", context=context)


@app.route("/pick", methods=["POST"])
def pick():
    print("\n\n", request.form, "\n\n")
    print(request.form)
    return redirect(QUERY_ROUTES[int(request.form.get("queries"))])


# Query 1
@app.route("/query1", methods=["GET"])
def query1():
    context = {}
    context["states"] = STATES
    return render_template("query1.html", context=context)


@app.route("/submission1", methods=["POST"])
def dropdown_submission():
    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    context = {}
    context["output"] = request.form.get("states")
    context["states"] = STATES
    print(context.get("output"))
    return render_template("query1.html", context=context)


# Query 2
@app.route("/query2", methods=["GET"])
@app.route("/query2/<state>", methods=["GET"])
def query2(state=None):
    context = {}
    counties = ["Please Insert State"]
    if state:
        context['selected_state'] = state
        counties = get_counties(state)

    context["states"] = STATES
    context["countys"] = counties
    # print(context["countys"])
    return render_template("query2.html", context=context)


@app.route("/submission2", methods=["POST"])
def dropdown_submission2():
    print(request.form)
    context = {}
    STATE_CURR = request.form.get("states")
    if request.form.get("countys") == "Please Insert State":
        return render_template("query2.html", context=context)

    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    print("\n\County:", request.form.get("countys"), "\n\n")
    context["output"] = request.form.get("states")
    context["states"] = STATES
    # print(context.get("output"))
    return render_template("query2.html", context=context)


# Query 3
@app.route("/query3", methods=["GET"])
@app.route("/query3/<state>", methods=["GET"])
def query3(state=None):
    context = {}
    counties = ["Please Insert State"]
    if state:
        context['selected_state'] = state
        counties = get_counties(state)

    context["states"] = STATES
    context["countys"] = counties
    # print(context["countys"])
    return render_template("query3.html", context=context)


@app.route("/submission3", methods=["POST"])
def dropdown_submission3():
    print(request.form)
    context = {}
    STATE_CURR = request.form.get("states")
    if request.form.get("countys") == "Please Insert State":
        return render_template("query3.html", context=context)

    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    print("\nCounty:", request.form.get("countys"), "\n\n")
    context["output"] = request.form.get("states")
    context["states"] = STATES
    # print(context.get("output"))
    return render_template("query3.html", context=context)



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
