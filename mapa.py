
import requests
from main import get_token, compute_ids, use_token
import json

API_URL = "https://journey-service-int.api.sbb.ch"


def use_token(route, API_URL = API_URL):
    auth = get_token()['access_token']
    headers = {
        'Authorization': f"Bearer {auth}",
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json',
        'calculateMidpoint': 'False',
        'fromStationID': '8503000',
        'mot': 'rail',
        'generalization': 'False',
        'toStationID': '8758270 ',
        'via': '8507000'
    }
    # Include the header (and additional ones if needed in your request)

    #return requests.post(API_URL + route "/v3/trips/by-origin-destination", headers=headers, json={   "origin": "8011315",   "destination": "8507000",   "date": "2023-04-18",   "time": "13:07",   "mobilityFilter": {     "walkSpeed": 50,   },   "includeAccessibility": "ALL", }).json()
    return requests.get(API_URL + route, headers=headers).json()

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
    return requests.get(f"{url_map}?fromStationID={codi_origen}&toStationID={codi_desti}&api_key={api_key_map}")

def main_fun(init_coords, end_coords):
    id_org, id_dst = compute_ids(init_coords, end_coords)
    
    response = get_route_drawing(id_org, id_dst)
    lista = response.json()["features"][2]["geometry"]["coordinates"]
    lista = [[i[1], i[0]] for i in lista]
    return lista



