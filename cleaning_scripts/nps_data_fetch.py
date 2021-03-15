import json
import requests

with open("../data/secrets.json", "r") as secrets:
    keys = json.load(secrets)

parks_url = "https://developer.nps.gov/api/v1/parks"

r = requests.get(parks_url, params=keys)
parks_json = r.json()

keys["limit"] = parks_json["total"]

r2 = requests.get(parks_url, params=keys)
parks_json = r2.json()

# filter data to just get national parks or preserves
natl_parks = []
unwanted_designations = ["Historical", "Battlefield", "Military", "Monument", "Memorial", "Parkway"]
for park in parks_json["data"]:
    valid = True
    if "Park" in park["designation"]:
        for desgn in unwanted_designations:
            if desgn in park["designation"]:
                valid = False
        if valid == True:
            designations = park["designation"].split(" ")
            if len(designations) > 1:
                natl_parks.append({
                    "name": park["name"].lower(), 
                    "lat": park["latitude"], 
                    "lon": park["longitude"] })

with open("../data/nps_data_fetch.json", "w") as outfile:
    json.dump(natl_parks, outfile, indent=4)