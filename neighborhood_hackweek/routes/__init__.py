from flask import (
    Blueprint,
    current_app as app,
    jsonify
)
from flask_transmute.swagger import Swagger
from neighborhood_hackweek.routes import (
    root,
    zon,
    property_region
)

def add_routes(app):
    # the standard way to add routes in flask is via blueprints.
    # these are examples.
    app.register_blueprint(zon, url_prefix="/monitor/zon")
    app.register_blueprint(root)
    app.register_blueprint(property_region.property_region_route, url_prefix="/property_region/")
    
    swagger = Swagger('neighborhood-hackweek', '1.0', route_prefix="/")
    swagger.init_app(app)
