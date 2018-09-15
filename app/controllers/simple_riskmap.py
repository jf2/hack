import flask as fl
import ee
import random


simple_riskmap = fl.Blueprint('simple_riskmap', __name__, url_prefix="/simple_riskmap")
@simple_riskmap.route("/")
def index():
    return fl.render_template("map.html")


@simple_riskmap.route("/heatmap")
def heatmap():
    landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003');
    landsat2008 = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012');

    ndvi1999 = landsat1999.select('B4').subtract(landsat1999.select('B3')).divide(landsat1999.select('B4').add(landsat1999.select('B3')));

    img_data = ndvi1999.getMapId()
    return fl.jsonify({
        "mapid": img_data["mapid"],
        "token": img_data["token"]
    })

heatmap.state = False