import flask as fl
from app.controllers.base import __blueprints__
import yaml
import ee

if __name__ == "__main__":
    ee.Initialize()
    cfg = yaml.load(open("config.yaml"))

    app = fl.Flask(__name__, template_folder="app/templates", static_folder="app/static")

    for key in cfg:
        app.config[key] = cfg[key]

    for blueprint in __blueprints__:
        app.register_blueprint(blueprint)

    app.run()