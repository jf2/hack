import flask as fl


simple_riskmap = fl.Blueprint('simple_riskmap', __name__, url_prefix="/simple_riskmap")
@simple_riskmap.route("/")
def index():
    return fl.render_template("map.html")

@simple_riskmap.route("/heatmap")
def heatmap(loc=None, lat=None):
    return fl.jsonify({
        "loc": loc,
        "lat": lat
    })