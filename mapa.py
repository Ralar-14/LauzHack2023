
import requests
from main import get_token, compute_ids, use_token
import json

API_URL = "https://journey-service-int.api.sbb.ch"


def map(init_station, end_station):
    auth = get_token()['access_token']
    headers = {
        'Authorization': f"Bearer {auth}",
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    
    return requests.post("https://journey-maps.api.sbb.ch/v1/route?fromStationID=" + init_station + "&toStationID=" + end_station + "&api_key=" + auth, headers=headers)

url_map = "https://journey-maps.api.sbb.ch/v1/route"
api_key_map = "bf9e3a88ab8101ba22ba8c752bbbcfd8"

def get_route_drawing(codi_origen, codi_desti):
    return requests.get(f"{url_map}?fromStationID={codi_origen}&toStationID={codi_desti}&api_key={api_key_map}&mot=rail")

def get_route_drawing2(id_org, id_dst):
    jsn = {"origin": f"{id_org}", "destination": f"{id_dst}"}
    #jsn = {"origin": "8501042", "destination": "8506041"}
    a = use_token("/v3/trips/by-origin-destination", method="POST", js=jsn)
    id = a["trips"][0]["id"]
    n_legs = len(a["trips"][0]["legs"])
    url_map = "https://journey-maps.api.sbb.ch/v1/journey"
    response = requests.get(f"{url_map}?ctx={id}&lang=en&api_key={api_key_map}")
    lista = [i["geometry"]["coordinates"] for i in response.json()["features"] if i["properties"]["type"] == "path" and i["properties"]["legId"] in [f"{i}" for i in range(n_legs)] and i["geometry"]["type"] == "LineString" and i["properties"]["generalization"] == 0]
    #lista = response.json()["features"][2]["geometry"]["coordinates"]
    l = []
    for i in lista:
        l.extend(i)

    lista = [[i[1], i[0]] for i in l]
    return lista

def main_fun(init_coords, end_coords):
    id_org, id_dst = compute_ids(init_coords, end_coords)
    
    lista = get_route_drawing2(id_org, id_dst)
    
    return lista



