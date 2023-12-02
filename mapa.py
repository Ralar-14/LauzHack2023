
import requests
from main import get_token
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

response = get_route_drawing(8503006, 8595419)
print("Código de estado:", response.status_code)
print("Contenido:", response)

with open('coord1.json', 'w') as f:
    lista = response.json()["features"][2]["geometry"]["coordinates"]
    f.write("[")
    for i in lista:
        f.write("[")
        f.write(str(i[1]) + "," + str(i[0]))
        f.write("],")
    f.write("]")

