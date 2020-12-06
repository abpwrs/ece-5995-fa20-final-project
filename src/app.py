from flask import Flask, jsonify, render_template
# from flask.ext.scss import Scss
from flask_mongoengine import MongoEngine
import mongoengine as me
from flask_assets import Environment, Bundle



# init app
app = Flask(__name__)
# config mongodb
app.config['MONGODB_SETTINGS'] = {
    "db": "covid",
}

# init db
mongo_db = MongoEngine(app)

# flask assets - styling
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('index.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)


# models
class CovidUS(me.Document):
    meta = {
        'collection': 'covid_us'
    }
    date = me.StringField(required=True, unique=True)
    cases = me.IntField(required=True, min_value=0)
    deaths = me.IntField(required=True, min_value=0)


# define app routes
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/covid')
@app.route('/covid/<date>')
def covid_us(date=None):
    print(date, type(date))
    if date:
        covidus_data = CovidUS.objects(date=date).first()
        print(covidus_data, type(covidus_data))
        return jsonify(covidus_data)
    else:
        covidus_data = CovidUS.objects().first()
        print(covidus_data, type(covidus_data))
        return jsonify(covidus_data)