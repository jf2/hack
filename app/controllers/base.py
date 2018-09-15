import flask as fl

from app.controllers.simple_riskmap import simple_riskmap

tabs = [simple_riskmap]
base = fl.Blueprint('base', __name__, url_prefix="/")

@base.route("/")
def index():
    return "<br />\n".join(("""<a href="{}">{}</a>""".
                           format(fl.url_for("{}.index".format(tab.name)), tab.name) for tab in tabs))


__blueprints__ = tabs + [base]