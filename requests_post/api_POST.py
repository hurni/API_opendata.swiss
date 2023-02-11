# -*- coding: utf-8 -*-
"""

how to POST updates of dataset's metadata (from within the BVerwaltungsnetz).



"""

import requests
import urllib3
from datetime import datetime


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
          'http':'http://proxy-bvcol.admin.ch:8080',
          'https':'http://proxy-bvcol.admin.ch:8080'
        }

s = requests.Session()

now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0000")
#iso_now = now.isoformat(timespec='milliseconds')

#print(now)

# id of dataset to be changed: "6fbab091-823e-43df-8b1d-de2c3e6763c9"
ids = '6fbab091-823e-43df-8b1d-de2c3e6763c9'

private_api_key = '0887bd41-1637-4334-a0ad-633b0f557667'
url = 'https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/package_patch'


header = {'Authorization': private_api_key}

data = {
        'id': ids,
        'modified' : now
        }

x = s.post(url,data=data,proxies=proxies,headers=header,verify=False)
print(x.status_code)

