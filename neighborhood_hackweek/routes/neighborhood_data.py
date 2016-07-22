from flask import Blueprint, jsonify
import httplib

from neighborhood_hackweek.db.neighborhood_data import (
    get_neighborhood_data_by_region_id_neighborhood as get_neighborhood_data
)

neighborhood_data_route = Blueprint('neighborhood_data', __name__)


@neighborhood_data_route.route('/<int:region_id_neighborhood>', methods=['GET'])
def get_neighborhood_data_by_region_id_neighborhood(region_id_neighborhood=0):
    if region_id_neighborhood > 0:
        hood_data = get_neighborhood_data(region_id_neighborhood)
        if hood_data:
            status = httplib.OK
        else:
            status = httplib.NOT_FOUND
        return jsonify(neighborhood_data=hood_data), status

    return "Invalid parameter", httplib.BAD_REQUEST
