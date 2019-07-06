import requests
import json
import pandas as pd
import datetime
import random

#80km/h, in m/s
speed=80/3.6
kwh = float(0.000127)

def make_request(originLat, originLon, destinationLat, destinationLon):
    json_raw=requests.get("https://routing.openstreetmap.de/routed-car/route/v1/driving/"+
                      originLat+","+originLon+";"+
                      destinationLat+","+destinationLon+
                      "?overview=false&alternatives=false&steps=true",verify=False).text
    return json.loads(json_raw)


def get_time(distance, initial_time):
    seconds = distance / speed
    return initial_time + datetime.timedelta(seconds=seconds)


def generate_searches():
    max_journeys = 5
    df_cities=pd.read_csv("Cities Italy.csv")
    total_cities = len(df_cities)
    searches = []
    for i in range(max_journeys):
        origin_city = random.randrange(total_cities)
        destination_city= random.randrange(total_cities)
        if origin_city == destination_city:
            continue
        search_data = generate_search(origin_city, destination_city, df_cities)
        searches.append(search_data)
    return searches
        
def generate_search(origin_city_index, destination_city_index, df_cities):
    origin_city_name = df_cities.at[origin_city_index, "city"]
    destination_city_name = df_cities.at[destination_city_index, "city"]
    origin_lat =str(df_cities.at[origin_city_index, "latitude"])
    origin_lon =str(df_cities.at[origin_city_index, "longitude"])
    destination_lat =str(df_cities.at[destination_city_index, "latitude"])
    destination_lon =str(df_cities.at[destination_city_index, "longitude"])

    return {"origin": origin_city_name,
                    "destination": destination_city_name,
                    "originLat": origin_lat,
                    "originLon": origin_lon,
                    "destinationLat": destination_lat,
                    "destinationLon": destination_lon,
                    "vehicle_id":980190962}

def map_stops(search, resp, initial_time):
    search["consumptions"] = []
    current_time = initial_time
    for el in resp["routes"][0]["legs"][0]["steps"]:
        current_time = get_time(el["distance"], current_time)
        consumption = {"time": str(current_time), "lat":el["maneuver"]["location"][0], "lon": el["maneuver"]["location"][1], "consumption": get_consumption(el["distance"]) }
        search["consumptions"].append(consumption)
    return search

def get_consumption(distance):
    return distance * kwh

def generate_routes(searches):
    routes = []
    initial_time = datetime.datetime.now()
    for search in searches:
        resp = make_request(search['originLat'], search['originLon'], search['destinationLat'], search['destinationLon'])
        if resp['code'] != 'Ok':
            print("failed with reason {}".format(resp['code']))
            continue
        route = map_stops(search, resp, initial_time)
        print(f"success")
        routes.append(route)
    return routes        

def upload_to_api(routes):
    for route in routes:
        response = requests.post("http://localhost:3000/api/v1/journey", json=route)
        if response.status_code != 200:
            print(response.reason)


def main():
    searches = generate_searches()
    routes = generate_routes(searches)
    upload_to_api(routes)

if __name__ == "__main__":
    main()
