import flask as fl
from app.controllers.base import __blueprints__
import yaml
import ee
from pathlib import Path

if __name__ == "__main__":
    ee.Initialize()
    cfg = yaml.load(open("config.yaml"))
    cfg['commit_hash'] = ''

    my_file = Path("commit_hash.txt")
    if my_file.is_file():
        with open(my_file) as f:
            cfg['commit_hash'] = f.read()

    app = fl.Flask(__name__, template_folder="app/templates", static_folder="app/static")

    for key in cfg:
        app.config[key] = cfg[key]

    for blueprint in __blueprints__:
        app.register_blueprint(blueprint)
    
    app.config["CACHE_TYPE"] = "null"

    app.run(host="0.0.0.0")