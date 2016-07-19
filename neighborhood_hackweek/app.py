import os
import yaml
from flask import Flask
from .routes import add_routes
from zillowdb.session.manager import DBTransaction


def create_app(config_fn):
    app = Flask(__name__)
    # when you want to add application globals, you do so here.
    # attach the object you want to be accessible to the app object.
    # more info: http://flask.pocoo.org/docs/0.10/appcontext/#purpose-of-the-application-context
    #
    # E.G:
    # app.pet_db = PetDB("://myconnectionstring")
    add_routes(app)
    config = load_config(config_fn)
    app.config.update(config)
    DBTransaction.configure('property_db', config.get('zillow.mssql.property'))
    return app


def load_config(config_fn):
    # Load the specialized template file
    script_dir = os.path.dirname(__file__)
    config_file = os.path.join(script_dir, '..',
                               'config', 'current', config_fn)
    return yaml.load(file(config_file))
