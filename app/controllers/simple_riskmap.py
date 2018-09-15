import flask as fl
import ee
import random


simple_riskmap = fl.Blueprint('simple_riskmap', __name__, url_prefix="/simple_riskmap")
@simple_riskmap.route("/")
def index():
    return fl.render_template("map.html")


@simple_riskmap.route("/heatmap")
def heatmap():
    img = ee.Image("srtm90_v4")
    img_data = img.getMapId()
    return fl.jsonify({
        "mapid": img_data["mapid"],
        "token": img_data["token"]
    })

heatmap.state = False