import flask as fl
import ee
import datetime as dt
import random
from app.computation.transform import z_score, unit, mean
from app.computation.cmap import balance


simple_riskmap = fl.Blueprint('simple_riskmap', __name__, url_prefix="/simple_riskmap")
simple_riskmap.config = {}

@simple_riskmap.record
def record_params(setup_state):
    app = setup_state.app
    simple_riskmap.config = {**app.config}


@simple_riskmap.route("/")
def index():
    return fl.render_template("map.html")

@simple_riskmap.route("/nonreduced")
def big():
    return fl.render_template("nonreduced_map.html")

@simple_riskmap.route("/landsat")
def landsat():
    landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003')
    ndvi1999 = landsat1999.select('B4').\
        subtract(landsat1999.select('B3')).\
        divide(landsat1999.select('B4').
               add(landsat1999.select('B3')))

    img_data = ndvi1999.getMapId()
    return fl.jsonify({
        "mapid": img_data["mapid"],
        "token": img_data["token"]
    })

@simple_riskmap.route("/heatmap")
def heatmap():
    start_date = fl.request.args.get('start_date', None)
    end_date = fl.request.args.get('end_date', None)
    wind = bool(int(fl.request.args.get("wind", None)))
    drought = bool(int(fl.request.args.get("drought", None)))

    end_date = dt.date.today() if end_date is None else dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    if start_date is None:
        start_date = dt.datetime(year=end_date.year - simple_riskmap.config["riskmap"]["default_lookback_years"],
                                 day=end_date.day, month=end_date.month)
    else:
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()

    fix_drought = ee.Image(2000)
    fix_wind = ee.Image(200)
    fix_null = ee.Image(0.)

    wind_collection = ee.ImageCollection('FIRMS'). \
        filterDate(start_date.isoformat(), end_date.isoformat()).\
        select("T21")

    drought_collection = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE'). \
        filterDate(start_date.isoformat(), end_date.isoformat()).\
        select("pdsi")

    m_wind = wind_collection.mean().unmask().divide(fix_wind)
    m_drought = drought_collection.mean().divide(fix_drought)

    if drought and wind:
        m = m_drought.add(m_wind)
    if drought and not wind:
        m = m_drought
    if not drought and wind:
        m = m_wind
    if not drought and not wind:
        m = fix_null

    data = m.getMapId({"palette": balance, "min": 0, "max": 1., "opacity": 0.75})

    return fl.jsonify({
        "mapid": data["mapid"],
        "token": data["token"]
    })


@simple_riskmap.route("/nonreduced_heatmap")
def nonreduced_heatmap():
    start_date = fl.request.args.get('start_date', None)
    end_date = fl.request.args.get('end_date', None)

    ne = (float(fl.request.args.get("ne_lng")), float(fl.request.args.get("ne_lat")))
    sw = (float(fl.request.args.get("sw_lng")), float(fl.request.args.get("sw_lat")))

    geom = ee.Geometry.Rectangle(ne[0], ne[1], sw[0], sw[1])
    today = dt.date.today()
    end_date = dt.date(year=today.year, month=today.month, day=today.day - 1) \
        if end_date is None else dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    if start_date is None:
        start_date = dt.datetime(year=end_date.year - simple_riskmap.config["riskmap"]["default_lookback_years"],
                                 day=end_date.day, month=end_date.month)
    else:
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    epsilon = ee.Image(1e-14)

    fire_collection = ee.ImageCollection("NOAA/GFS0P25").\
        filterDate(start_date.isoformat(), end_date.isoformat()).\
        select("temperature_2m_above_ground")

    fire_mean = fire_collection.mean()
    fire = fire_mean.getMapId({"palette": balance, "min": -35, "max": 70, "opacity": 0.75})

    return fl.jsonify([{"mapid": fire["mapid"], "token": fire["token"]}])
    # datas = [fire.getMapId(vis_params={"min": -2, "max": +2, "palette": ['red', 'orange', 'yellow']}),
    #          drought.getMapId(vis_params={"min": -2, "max": +2, "palette": ['aqua', 'teal', 'blue']})]

    # return fl.jsonify([{"mapid": data["mapid"], "token": data["token"]} for data in datas])