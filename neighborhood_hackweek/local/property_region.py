import json

def get_property_regions_by_region_id_neighborhood(region_id_neighborhood):
    with open('property_region/' + str(region_id_neighborhood) + '.json') as json_file:
        json_data = json.load(json_file)
    return json_data
