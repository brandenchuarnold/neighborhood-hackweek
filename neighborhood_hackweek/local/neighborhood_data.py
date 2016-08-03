import json

def get_neighborhood_data_by_region_id_neighborhood(region_id_neighborhood):
    with open('neighborhood_data/' + str(region_id_neighborhood) + '.json') as json_file:
        json_data = json.load(json_file)
    return json_data
