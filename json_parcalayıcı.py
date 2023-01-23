import json
def get_coordinates():
    # read json file
    with open("map.geojson", "r") as json_file:
        data = json.load(json_file)

    # get coordinates information
    coordinates = data["features"][0]["geometry"]["coordinates"]

    # convert coordinates to tuple
    coordinates_tuple = tuple(coordinates)
    
    # print(coordinates_tuple)
    return coordinates_tuple