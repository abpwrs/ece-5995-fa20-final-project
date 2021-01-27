from .neo_models import graph_db


def validate_date_range_state(start_date, end_date, state_name):
    oldest = oldest_record_for_state(state_name=state_name)
    newest = newest_record_for_state(state_name=state_name)

    if (
        start_date < oldest
    ):  # if start is older than the oldest record, start becomes the oldest record
        start_date = oldest

    if (
        end_date > newest
    ):  # if end is newer than the newest record, end becomes the newest
        end_date = newest

    return start_date, end_date


def validate_date_range_county(start_date, end_date, state_name, county_name):
    oldest = oldest_record_for_county(state_name=state_name, county_name=county_name)
    newest = newest_record_for_county(state_name=state_name, county_name=county_name)

    if (
        start_date < oldest
    ):  # if start is older than the oldest record, start becomes the oldest record
        start_date = oldest
    if (
        end_date > newest
    ):  # if end is newer than the newest record, end becomes the newest
        end_date = newest

    return start_date, end_date


def oldest_record_for_state(state_name):
    result = graph_db.run(
        f'MATCH (s:State {{ name: "{state_name}" }})<-[:RECORDED_IN]-(covid:CovidRecord) RETURN covid.date AS date ORDER BY date ASC LIMIT 1'
    )
    return result.data()[0]["date"]


def oldest_record_for_county(state_name, county_name):
    result = graph_db.run(
        f'MATCH (s:State {{ name: "{state_name}" }})<-[:LOCATED_IN]-(c:County {{ name: "{county_name}" }})<-[:RECORDED_IN]-(covid:CovidRecord) RETURN covid.date AS date ORDER BY date ASC LIMIT 1'
    )
    return result.data()[0]["date"]


def newest_record_for_state(state_name):
    result = graph_db.run(
        f'MATCH (s:State {{ name: "{state_name}" }})<-[:RECORDED_IN]-(covid:CovidRecord) RETURN covid.date AS date ORDER BY date DESC LIMIT 1'
    )
    return result.data()[0]["date"]


def newest_record_for_county(state_name, county_name):
    result = graph_db.run(
        f'MATCH (s:State {{ name: "{state_name}" }})<-[:LOCATED_IN]-(c:County {{ name: "{county_name}" }})<-[:RECORDED_IN]-(covid:CovidRecord) RETURN covid.date AS date ORDER BY date DESC LIMIT 1'
    )
    return result.data()[0]["date"]


def get_states():
    result = graph_db.run("MATCH (s:State) RETURN s.name AS name")
    return [d["name"] for d in result.data()]


def get_counties(state_name):
    result = graph_db.run(
        f'MATCH (s:State {{ name: "{state_name}"}})<-[r:LOCATED_IN]-(c:County) RETURN c.name as name'
    )
    return [d["name"] for d in result.data()]


def get_cases_by_state(state_name, start_date, end_date):
    result = graph_db.run(
        f'MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(s:State {{ name: "{state_name}" }})<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) RETURN covidNew.cases-covidOld.cases as cases'
    )
    return result.data()


def get_cases_by_state_as_pop_percentage(state_name, start_date, end_date):
    result = graph_db.run(
        f'MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(s:State {{ name: "{state_name}" }})<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) WITH covidNew.cases-covidOld.cases as cases, s RETURN 100 * toFloat(cases) / toFloat(s.pop) as case_percentage'
    )
    return result.data()


def get_cases_by_county(state_name, county_name, start_date, end_date):
    result = graph_db.run(
        f'MATCH (s:State {{name: "{state_name}"}})<-[:LOCATED_IN]-(c:County {{name: "{county_name}"}}) WITH s, c MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(c)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) RETURN covidNew.cases-covidOld.cases as cases'
    )
    return result.data()


def get_cases_by_county_as_pop_percentage(
    state_name, county_name, start_date, end_date
):
    result = graph_db.run(
        f'MATCH (s:State {{name: "{state_name}"}})<-[:LOCATED_IN]-(c:County {{name: "{county_name}"}}) WITH s, c MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(c)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) WITH covidNew.cases-covidOld.cases as cases, c RETURN 100 * toFloat(cases) / toFloat(c.pop) as case_percentage'
    )
    return result.data()


# return list of states
def get_ranked_cases_by_state(start_date, end_date):
    result = graph_db.run(
        f'MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(s:State)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) RETURN s.name, covidNew.cases-covidOld.cases as cases ORDER BY cases DESC'
    )
    return result.data()


# return list of states
def get_ranked_cases_by_state_as_pop_percentage(start_date, end_date):
    result = graph_db.run(
        f'MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(s:State)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) WITH 100*toFloat(covidNew.cases-covidOld.cases) / toFloat(s.pop) as case_percentage, s RETURN s.name, case_percentage ORDER BY case_percentage DESC'
    )
    return result.data()


# return list of counties by net cases within a state
def get_ranked_cases_by_county(state_name, start_date, end_date):
    result = graph_db.run(
        f'MATCH (s:State {{name: "{state_name}"}})<-[:LOCATED_IN]-(c:County) WITH s, c MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(c)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) RETURN c.name, covidNew.cases-covidOld.cases as cases ORDER BY cases DESC'
    )
    return result.data()


# return list of counties by net cases within a state
def get_ranked_cases_by_county_as_pop_percentage(state_name, start_date, end_date):
    result = graph_db.run(
        f'MATCH (s:State {{name: "{state_name}"}})<-[:LOCATED_IN]-(c:County) WITH s, c MATCH (covidNew:CovidRecord {{ date: "{end_date}" }} )-[:RECORDED_IN]->(c)<-[:RECORDED_IN]-( covidOld:CovidRecord {{ date: "{start_date}" }} ) WITH 100*toFloat(covidNew.cases-covidOld.cases) / toFloat(s.pop) as case_percentage, c RETURN c.name, case_percentage ORDER BY case_percentage DESC'
    )
    return result.data()
