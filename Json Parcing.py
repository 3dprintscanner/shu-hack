import requests
import json
from geopy import distance
import pandas as pd
import datetime
import random

df_cities=pd.read_csv("Cities Italy.csv")
origin_index=random.randrange(len(df_cities))

origin=df_cities.at[origin_index, "city"]
originLat=str(df_cities.at[origin_index, "latitude"])
originLon=str(df_cities.at[origin_index, "longitude"])

destination_index=random.randrange(len(df_cities))

while True:
    if destination_index!=origin_index:
        break
    else:
        destination_index=random.randrange(len(df_cities))
        
destination=df_cities.at[destination_index, "city"]
destinationLat=str(df_cities.at[destination_index, "latitude"])
destinationLon=str(df_cities.at[destination_index, "longitude"])

vehicle_id=random.randrange(10000000)

#80km/h, in m/s
speed=80/3.6

json_raw=requests.get("https://routing.openstreetmap.de/routed-car/route/v1/driving/"+
                      originLat+","+originLon+";"+
                      destinationLat+","+destinationLon+
                      "?overview=false&alternatives=false&steps=true").text

json_clean=json.loads(json_raw)

def get_time(originLat, originLon, destLat, destLon):
    this_distance = distance.distance((float(originLat), float(originLon)), (float(destLat), float(destLon))).km * 1000 
    
    seconds = this_distance / speed
    return datetime.timedelta(seconds=seconds)



coords=[]

#coordinates of turning points:
for el in json_clean["routes"][0]["legs"][0]["steps"]:
    coords.append([el["maneuver"]["location"][0], el["maneuver"]["location"][1]])

json_output={}
json_output.update({"origin": origin,
                    "destination": destination,
                    "originLat": originLat,
                    "originLon": originLon,
                    "destinationLat": destinationLat,
                    "destinationLon": destinationLon,
                    "vehicle_id":vehicle_id})

consumptions=
