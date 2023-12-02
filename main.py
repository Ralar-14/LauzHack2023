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

def use_token(route, API_URL = API_URL):
    auth = get_token()['access_token']
    headers = {
        'Authorization': f"Bearer {auth}",
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    # Include the header (and additional ones if needed in your request)

    #return requests.post(API_URL + route "/v3/trips/by-origin-destination", headers=headers, json={   "origin": "8011315",   "destination": "8507000",   "date": "2023-04-18",   "time": "13:07",   "mobilityFilter": {     "walkSpeed": 50,   },   "includeAccessibility": "ALL", }).json()
    return requests.get(API_URL + route, headers=headers).json()

def get_data():
    api_data = use_token(route = "/v3/stop-places")
    jf = {"stopPlaces": [{"id": data['id'], "vehicleModes": [i["id"] for i in data['vehicleModes']]} for data in api_data['stopPlaces']]}

    json_filtrado = json.dumps(jf, indent=4)
    
    with open('data2.json', 'w') as f:
        f.write(json_filtrado)
         
    return json_filtrado

if __name__ == '__main__':
    use
    # get_data()
    
    
        
    
    
    
    
