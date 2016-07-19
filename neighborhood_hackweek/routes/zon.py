import json
from flask import Blueprint, jsonify

# Test definition for a zon test to fetch the home page
test_json = json.loads("""
{
    "homepage": {
        "verbs": [
            {
                "paths": [ "/" ],
                "production_safe": true,
                "type": "simple_http"
            }
        ],
        "description": "Fetch the homepage"
    }
}
""")


zon = Blueprint('zon', __name__)


@zon.route('/')
def render_test_definitions():
    """ returns a json blob, describing the zon tests to execute """
    return jsonify(**test_json)
