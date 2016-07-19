from flask import Blueprint, jsonify
import httplib

from neighborhood_hackweek.db.property_region import get_property_regions_by_region_id_neighborhood

property_region_route = Blueprint('property_region', __name__)


@property_region_route.route('/<int:region_id_neighborhood>', methods=['GET'])
def get_property_regions_by_region_id_neighborhood(region_id_neighborhood=0):
    if region_id_neighborhood > 0:
        property_regs = get_property_regions_by_region_id_neighborhood(region_id_neighborhood)
        if property_regs:
            status = httplib.OK
        else:
            status = httplib.NOT_FOUND
            return jsonify(property_regions=property_regs), status

    return "Invalid parameter", httplib.BAD_REQUEST
