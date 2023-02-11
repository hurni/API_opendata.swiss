# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 08:33:13 2023
@author: U80838962
"""

import csv
from datetime import datetime,timedelta
import pandas as pd
import requests
import time
import urllib3 


def is_bv_netz():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxies = {"http":'http://proxy-bvcol.admin.ch:8080',
              "https":'http://proxy-bvcol.admin.ch:8080'}
    return proxies

def fetch_packages(test = bool, proxies = None):
# list of alls package_ids
    s = requests.Session()
    df_keywords = pd.DataFrame({"name":[],
                            'language':[],
                            "keywords":[]})
    languages = ['fr','de', 'en','it']
    packages = s.get('https://opendata.swiss/api/3/action/package_list', proxies=proxies,verify=False).json()["result"] 
    base_URL = "https://ckan.opendata.swiss/api/3/action/package_show?id="    
    if test:
        scope = range(7525,7530)
    else:
        scope = range(len(packages))

    for package in scope:
        try: # avoid errors by packages that are not datasets - such as showcases or harvesters - without running the query multiple times.
            name = packages[package]
            for language in languages:
                keywords = s.get(base_URL+name, proxies=proxies,verify=False).json()["result"]['keywords'][language]
                df2 = pd.DataFrame({"name":[name],
                                    'language':[language],
                                    "keywords":[keywords]})
                df_keywords = pd.concat([df_keywords,df2], ignore_index=True)
        except:
            continue
    return df_keywords

def create_list(df_keywords):
    list_of_keywords = list()
    result = list()
    list_of_keywords = df_keywords['keywords'].tolist()
    for item in list_of_keywords:
        result.extend(item)
    unique_keywords = list(dict.fromkeys(result))
    return unique_keywords

def save_as_csv(unique_keywords):
    now = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    with open('opendataswiss_unique_keywords'+now+'.txt','w') as file:
        write = csv.writer(file)
        write.writerow(unique_keywords)

def main(bund = True, test = True):
    start = time.perf_counter()
    if bund:
        proxies = is_bv_netz()
    else: 
        proxies = None
    df_keywords = fetch_packages(proxies=proxies, test=test)
    unique_keywords = create_list(df_keywords)
    save_as_csv(unique_keywords)
    end = time.perf_counter()
    print('Job took: ',timedelta(seconds=end-start))

if __name__=='__main__':
    main(test=False)