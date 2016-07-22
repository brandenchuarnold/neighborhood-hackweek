from flask import (
    Blueprint,
    current_app as app,
    jsonify
)
from flask_transmute.swagger import Swagger
from neighborhood_hackweek.routes.property_region import (
    property_region_route
)
from neighborhood_hackweek.routes.neighborhood_data import (
    neighborhood_data_route
)

def add_routes(app):
    # the standard way to add routes in flask is via blueprints.
    # these are examples.
    app.register_blueprint(property_region_route, url_prefix="/property_region")
    app.register_blueprint(neighborhood_data_route, url_prefix="/neighborhood_data")
    
    swagger = Swagger('neighborhood-hackweek', '1.0', route_prefix="/")
    swagger.init_app(app)
