import flask as fl
import ee
import datetime as dt
import random


simple_riskmap = fl.Blueprint('simple_riskmap', __name__, url_prefix="/simple_riskmap")
simple_riskmap.config = {}

@simple_riskmap.record
def record_params(setup_state):
    app = setup_state.app
    simple_riskmap.config = {**app.config}


@simple_riskmap.route("/")
def index():
    return fl.render_template("map.html")


@simple_riskmap.route("/heatmap")
def heatmap():
    landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003')
    ndvi1999 = landsat1999.select('B4').subtract(landsat1999.select('B3')).divide(landsat1999.select('B4').add(landsat1999.select('B3')));

    img_data = ndvi1999.getMapId()
    return fl.jsonify({
        "mapid": img_data["mapid"],
        "token": img_data["token"]
    })

@simple_riskmap.route("/test_heatmap")
def test_heatmap(start_date=None, end_date=None):
    end_date = dt.date.today() if end_date is None else dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    if start_date is None:
        start_date = dt.datetime(year=end_date.year - simple_riskmap.config["riskmap"]["default_lookback_years"],
                                 day=end_date.day, month=end_date.month)
    else:
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()

    collection = ee.ImageCollection("FIRMS").\
        filterDate(start_date.isoformat(), end_date.isoformat()).\
        select('T21')
    mean = collection.reduce(ee.Reducer.mean())
    data = mean .getMapId()

    return fl.render_template("test_map.html", mapid=data["mapid"], token=data["token"])