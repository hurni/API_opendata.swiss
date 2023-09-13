# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:37:15 2023

@author: U80838962
"""

import urllib3
import requests
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
          'http':'http://proxy-bvcol.admin.ch:8080',
          'https':'http://proxy-bvcol.admin.ch:8080'
        }

s = requests.Session()


# from dummy user - not the sys-admin
private_api_key = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX' # cp. opendata.swiss > user page (click on your name/icon in the top right corner)

url = 'https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/package_create'

header = {
    'Authorization': private_api_key
    }

# random nummer added to enable multiple usage
randomizer = str(random.randrange(100000))

# resource part works when using url = '...action/resource_create'
data = {
        "name": "name_package2"+randomizer, 
        "identifier": "namet_package2"+randomizer+"@bundesamt-fuer-open-data",
        "title_for_slug": "name_package2"+randomizer, 
        "display_name": {
        	"fr": "display_name test_API_POST package fr", 
        	"de": "display_name test_API_POST package de", 
        	"en": "display_name test_API_POST package en", 
        	"it": "display_name test_API_POST package it"
        	}, 
        "publisher": {
        	"url": 'https://opendata.swiss/organization/bundesamt-fuer-open-data',
        	"name": ""
        	}, 
        
        "issued": "2022-03-19T00:00:00", 
        "contact_points": {}, 
        
        "description": {
        	"fr": "description test_API_POST package fr", 
        	"en": "description test_API_POST package en", 
        	"de": "description test_API_POST package de", 
        	"it": "description test_API_POST package it"
        	}, 
        "title": {
        	"fr": "title test_API_POST package fr", 
        	"de": "title test_API_POST package de", 
        	"en": "title test_API_POST package en", 
        	"it": "title test_API_POST package it"
        	}, 
        
        "private": False, 
        "isopen" : False,
        "type": "dataset", 
        "accrual_periodicity": "http://publications.europa.eu/resource/authority/frequency/MONTHLY", 
        "owner_org": "98dda3ef-6f39-4e3a-b133-29dd2bec632d", 
        "url": "example.com", 
        
        "resources": [{
        	"issued": "2023-02-13T00:00.0000", 
        	"display_name": {
        		"fr": "display_name test_API_POST resource fr", 
        		"de": "display_name test_API_POST resource de", 
        		"en": "display_name test_API_POST resource en", 
        		"it": "display_name test_API_POST resource it"
        		}, 
        	"title": {
        		"fr": "title test_API_POST resource fr", 
        		"de": "title test_API_POST resource de", 
        		"en": "title test_API_POST resource en", 
        		"it": "title test_API_POST resource it"
        		}, 
        	"download_url": "example.com",
        	"state": "active", 
        	"description": {
        		"fr": "description test_API_POST resource fr", 
        		"en": "description test_API_POST resource en", 
        		"de": "description test_API_POST resource de", 
        		"it": "description test_API_POST resource it"
        		}, 
        
        	"name": {
        		"fr": "name test_API_POST resource fr", 
        		"de": "name test_API_POST resource de", 
        		"en": "name test_API_POST resource en", 
        		"it": "name test_API_POST resource it"
        		}, 
        	"rights": "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired", 
        	"url": "https://freetestdata.com/wp-content/uploads/2021/09/Free_Test_Data_200KB_CSV-1.csv", 
        	"identifier": "name_resource_2@bundesamt-fuer-open-data", 
        	}], 
        
        }



print(data)
x = s.post(url, json=data, headers=header, proxies=proxies,verify=False)
print(x.status_code)
