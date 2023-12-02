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

def use_token():
    auth = get_token()['access_token']
    headers = {
        'Authorization': f"Bearer {auth}",
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }
    # Include the header (and additional ones if needed in your request)

    #return requests.post(API_URL + "/v3/trips/by-origin-destination", headers=headers, json={   "origin": "8011315",   "destination": "8507000",   "date": "2023-04-18",   "time": "13:07",   "mobilityFilter": {     "walkSpeed": 50,   },   "includeAccessibility": "ALL", }).json()
    return requests.get(API_URL + "/v3/stop-places/8011315", headers=headers).json()

if __name__ == '__main__':
    #save json to a file
    with open('data2.json', 'w') as outfile:
        json.dump(use_token(), outfile)
