
## patch datasets on PROD or ABNAHME environment of opendata.swiss.
## for actions, see the handbook: https://handbook.opendata.swiss/de/content/nutzen/api-nutzen.html#action-api

import requests

## user and organization credentials
# cp. opendata.swiss > user page (click on your name/icon in the top right 
# corner). if you do not know your organization's id, use the API button to 
# display any dataset as json in your browser . The necessary information 
# will be displayed.

PRIVATE_API_KEY = 'YOUR-PRIVATE-API-KEY' 
OWNER_ORG = "your_organizations_ID_on_a_opendata.swiss-environment"


url = 'https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/package_patch'


s = requests.Session()

header = {
    'Authorization': PRIVATE_API_KEY
    }

# resource part works when using url = '...action/resource_create'
data = {
        "id": "52ed3fcb-b721-449c-b611-a62b28a27833", 
        "owner_org": OWNER_ORG, 
        "relations": [{'url': 'https://www.geocat.ch/geonetwork/srv/ger/catalog.search#/metadata/b6c8d9c6-a2ca-435a-af0a-6a8ac94199fc', 'label': 'geocat.ch permalink'}], 
        }


print(data)
x = s.post(url, json=data, headers=header, verify=False)
print(x.status_code, data)
