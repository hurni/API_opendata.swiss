# -*- coding: utf-8 -*-

"""

how to crate a resource for an existing package: 
    package = 
    organisation_name = bundesamt-fuer-open-data
    org_id
cp. https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/organization_show?id=bundesamt-fuer-open-data


than: 
    > new organization (from within the BVerwaltungsnetz).

"""

from requests import session as s
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
          'http':'http://proxy-bvcol.admin.ch:8080',
          'https':'http://proxy-bvcol.admin.ch:8080'
        }

private_api_key = YOUR_API_KEY # see https://ckan.opendata.swiss/de/user/YOUR_USER_NAME

url = 'https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/resource_create'
header = {'Authorization': private_api_key}

data = {
        'identifier' : 'demo-resource_0002',
        'package_id' : '6fbab091-823e-43df-8b1d-de2c3e6763c9',
        'fr_description' : 'description for demo-resource_0002',
        'url':	'example.com',
        'format' : 'freepascal',
        'name' : 'demo-resource_0002',
        'issued': '2022-02-22T00:00:00.0000',
        'rights': 'NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired',
        'coverage' : 'coverage is imported as a string instead of two dates (i.e. dct:startDate | dct:endDate)',
        'some_none_existing_field' : 'random content can be added (and displayed via api)',
        }

"""

        'description' : {'fr':'This package was created via API POST'},

        'description' : {0 : {"fr":'This resource was created via API POST'},
                         1 : {"de" : 'german_description: This resource was created via API POST'}}

"""

x = s.post(url,data=data,proxies=proxies,headers=header,verify=False)
print(x.status_code)


"""

data = {
        'name': 'demo-package_0001',
        'description' : '',
        'identifier' : 'demo-package_0001@bundesamt-fuer-open-data',
        'title_for_slug':'demo-package_0001',
        'private': False,
        'issued':"2023-01-01T00:00:00",
        'owner_org': "98dda3ef-6f39-4e3a-b133-29dd2bec632d",
        'resources' :  {
            "package_id" : "6fbab091-823e-43df-8b1d-de2c3e6763c9",
            'some_none_existing_field' : 'random_content',
            "url":"",
            "name": "demo-resource_0002_testname",
            "title": "demo-resource_0002",
            "rights": "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired"
            },
        'organization': "bundesamt-fuer-open-data",

                              
        }



# create organization:

url = 'https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/organization_create'


header = {'Authorization': private_api_key}

data = {
        'name': {'de':'demo-organization'},
        'title' : {'en':'demo-organization'},
        'description' : {'fr':'This is an organization created vie API POST'},

        }

x = s.post(url,data=data,proxies=proxies,headers=header,verify=False)
print(x.status_code)









"""
