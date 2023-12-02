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
    api_data = use_token("/v3/stop-places")
    jf = {"stopPlaces": [{"id": data['id'], "vehicleModes": [i["id"] for i in data['vehicleModes']]} for data in api_data['stopPlaces']]}

    json_filtrado = json.dumps(jf, indent=4)
         
    return json_filtrado

if __name__ == '__main__':
    # get_data()
    #46.22083551986927, 6.120279059147888
    #47.47444774490644, 8.51004368853066
    
    org = use_token("/v3/places/by-coordinates?longitude=6.120&latitude=46.220&limit=1&includeVehicleModes=false&type=StopPlace")
    id_org = org["places"][0]["id"]
    dst = use_token("/v3/places/by-coordinates?longitude=8.5100&latitude=47.4744&limit=1&includeVehicleModes=false&type=StopPlace")
    id_dst = dst["places"][0]["id"]
    jsn = {"origin": id_org, "destination": id_dst}
    b = use_token("/v3/trips/by-origin-destination", method="POST", js=jsn)["trips"][0]

    print(id_org)
    print(id_dst)
    with open('data5.json', 'w') as f:
       f.write(json.dumps(dst, indent=4))
    
    
    
    
