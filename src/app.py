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
    "Number of cases in a state over a date range",  # params for state, start date, and end date               - get_cases_by_state - DONE
    "Number of cases in a county over a date range",  # params for state, county, start date, and end date      - get_cases_by_county - DONE
    "Rank counties by net cases",  # params for start, end date, and state                                      - get_ranked_cases_by_county - DONE
    "Rank counties by cases as percentage of population",  # params for start, end date, and state              - get_ranked_cases_by_county_as_pop_percentage
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
    context["query_name"] = QUERY_TEXT[0]
    counties = ["Please Insert State"]
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

    state_name = request.form.get("states")
    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    start_date, end_date = validate_date_range_state(start_date, end_date, state_name)
    context["output"] = get_cases_by_state(state_name, start_date, end_date)

    return render_template("query1.html", context=context)


# Query 2
@app.route("/query2", methods=["GET"])
@app.route("/query2/<state>", methods=["GET"])
def query2(state=None):
    context = {}
    context["query_name"] = QUERY_TEXT[1]
    counties = ["Please Insert State"]
    if state:
        context["selected_state"] = state
        counties = get_counties(state)

    context["states"] = STATES
    context["countys"] = counties
    # print(context["countys"])
    return render_template("query2.html", context=context)


@app.route("/submission2", methods=["POST"])
def dropdown_submission2():
    print(request.form)
    context = {}
    if request.form.get("countys") == "Please Insert State":
        return render_template("query2.html", context=context)

    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    print("\n\County:", request.form.get("countys"), "\n\n")
    context["output"] = request.form.get("states")
    context["states"] = STATES
    # print(context.get("output"))

    state_name = request.form.get("states")
    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    county_name = request.form.get("countys")
    start_date, end_date = validate_date_range_county(
        start_date, end_date, state_name=state_name, county_name=county_name
    )
    context["output"] = get_cases_by_county(
        state_name, county_name, start_date, end_date
    )

    return render_template("query2.html", context=context)


# Query 3
@app.route("/query3", methods=["GET"])
# @app.route("/query3/<state>", methods=["GET"])
def query3(state=None):
    context = {}
    context["query_name"] = QUERY_TEXT[2]
    counties = ["Please Insert State"]
    # counties = None
    # if state:
    #     context['selected_state'] = state
    #     counties = get_counties(state)

    context["states"] = STATES
    # context["countys"] = counties
    # print(context["countys"])
    return render_template("query3.html", context=context)


@app.route("/submission3", methods=["POST"])
def dropdown_submission3():
    print(request.form)
    context = {}
    # if request.form.get("countys") == "Please Insert State":
    #     return render_template("query3.html", context=context)

    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    # print("\nCounty:", request.form.get("countys"), "\n\n")
    context["output"] = request.form.get("states")
    context["states"] = STATES
    # print(context.get("output"))
    state_name = request.form.get("states")
    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    start_date, end_date = validate_date_range_state(start_date, end_date, state_name)
    context["output"] = get_ranked_cases_by_county(state_name, start_date, end_date)
    return render_template("query3.html", context=context)


# Query 4
@app.route("/query4", methods=["GET"])
# @app.route("/query4/<state>", methods=["GET"])
def query4(state=None):
    context = {}
    context["query_name"] = QUERY_TEXT[3]
    # counties = ["Please Insert State"]
    # if state:
    #     context['selected_state'] = state
    #     counties = get_counties(state)

    context["states"] = STATES
    # context["countys"] = counties
    # print(context["countys"])
    return render_template("query4.html", context=context)


@app.route("/submission4", methods=["POST"])
def dropdown_submission4():
    print(request.form)
    context = {}
    # if request.form.get("countys") == "Please Insert State":
    #     return render_template("query4.html", context=context)

    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    print("\n\nState:", request.form.get("states"), "\n\n")
    # print("\nCounty:", request.form.get("countys"), "\n\n")
    context["output"] = request.form.get("states")
    context["states"] = STATES
    # print(context.get("output"))
    state_name = request.form.get("states")
    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    start_date, end_date = validate_date_range_state(start_date, end_date, state_name)
    context["output"] = get_ranked_cases_by_county_as_pop_percentage(
        state_name, start_date, end_date
    )
    return render_template("query4.html", context=context)


# Query 5
@app.route("/query5", methods=["GET"])
def query5():
    context = {}
    context["query_name"] = QUERY_TEXT[4]
    counties = ["Please Insert State"]
    context["states"] = STATES
    return render_template("query5.html", context=context)


@app.route("/submission5", methods=["POST"])
def dropdown_submission5():
    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    context = {}
    context["states"] = STATES
    print(context.get("output"))

    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    # start_date, end_date = validate_date_range_state(start_date, end_date) # -- TODO: validate across all states
    context["output"] = get_ranked_cases_by_state(start_date, end_date)
    return render_template("query5.html", context=context)


# Query 6
@app.route("/query6", methods=["GET"])
def query6():
    context = {}
    context["query_name"] = QUERY_TEXT[5]
    counties = ["Please Insert State"]
    context["states"] = STATES
    return render_template("query6.html", context=context)


@app.route("/submission6", methods=["POST"])
def dropdown_submission6():
    print("\n\nDateStart:", request.form.get("startDate"))
    print("\n\nDateEnd:", request.form.get("endDate"))
    context = {}
    context["output"] = request.form.get("states")
    context["states"] = STATES
    print(context.get("output"))

    start_date = request.form.get("startDate")
    end_date = request.form.get("endDate")
    # start_date, end_date = validate_date_range_state(start_date, end_date) # -- TODO: validate across all states
    context["output"] = get_ranked_cases_by_state_as_pop_percentage(
        start_date, end_date
    )
    return render_template("query6.html", context=context)


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
