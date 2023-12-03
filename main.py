import requests
import json

API_URL = "https://journey-service-int.api.sbb.ch"
CLIENT_SECRET = "MU48Q~IuD6Iawz3QfvkmMiKHtfXBf-ffKoKTJdt5"
CLIENT_ID = "f132a280-1571-4137-86d7-201641098ce8"
SCOPE = "c11fa6b1-edab-4554-a43d-8ab71b016325/.default"

def get_token():
    params = {
        'grant_type': 'client_credentials',
        'scope': SCOPE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    return requests.post('https://login.microsoftonline.com/2cda5d11-f0ac-46b3-967d-af1b2e1bd01a/oauth2/v2.0/token',
                         data=params).json()

def use_token(route, method="GET", js=None):
    auth = get_token()['access_token']
    headers = {
        'Authorization': f"Bearer {auth}",
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    
    if method == "POST":
        return requests.post(API_URL + route, headers=headers, json=js).json()
    else:
        return requests.get(API_URL + route, headers=headers).json()
    
def get_data():
    api_data = use_token(route = "/v3/stop-places")
    jf = {"stopPlaces": [{"id": data['id'], "vehicleModes": [i["id"] for i in data['vehicleModes']]} for data in api_data['stopPlaces']]}

    json_filtrado = json.dumps(jf, indent=4)
         
    return json_filtrado

def compute_ids(coords_init, coords_end):
    print(coords_init)
    org = use_token(f"/v3/places/by-coordinates?longitude={coords_init[1]}&latitude={coords_init[0]}&includeVehicleModes=true&type=StopPlace")
    #org = [place for place in org["places"] if any(mode["id"] == "TRAIN" for mode in place.get("vehicleModes", []))]
    id_org = org["places"][0]["id"]
    dst = use_token(f"/v3/places/by-coordinates?longitude={coords_end[1]}&latitude={coords_end[0]}&includeVehicleModes=true&type=StopPlace")
    #dst = [place for place in dst["places"] if any(mode["id"] == "TRAIN" for mode in place.get("vehicleModes", []))]
    id_dst = dst["places"][0]["id"]
    return id_org, id_dst

# jsn = {"origin": id_org, "destination": id_dst}
# b = use_token("/v3/trips/by-origin-destination", method="POST", js=jsn)["trips"][0]
    
    
    
    
    
