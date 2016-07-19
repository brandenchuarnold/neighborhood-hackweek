from .zon import zon
from .root import root


def add_routes(app):
    # the standard way to add routes in flask is via blueprints.
    # these are examples.
    app.register_blueprint(zon, url_prefix="/monitor/zon")
    app.register_blueprint(root)
