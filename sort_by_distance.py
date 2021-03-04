# inspired by https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

from math import radians, cos, sin, asin, sqrt
import json

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3959 # Radius in Miles
    return c * r

def returnDistance(elem):
    return elem["distance"]

if __name__ == "__main__":
    
    with open("distance_settings.json", "r") as infile:
        settings = json.load(infile)

    with open(settings["data"], "r") as data:
        parks = json.load(data)

    sorted_parks = []
    for park in parks:
        park["distance"] = haversine(settings["longitude"], settings["latitude"], float(park["lon"]), float(park["lat"]))
        park["name"] = park["name"].replace(" ", "")
        sorted_parks.append(park)

    sorted_parks.sort(key=returnDistance)

    with open(settings["sorted"], "w") as outfile:
        json.dump(sorted_parks, outfile, indent=4)