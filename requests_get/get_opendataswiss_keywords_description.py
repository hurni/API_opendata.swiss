
# -*- coding: utf-8 -*-

"""
Created on Mon Jan 16 08:33:13 2023
@author: U80838962

creates two files:

- 'opendataswiss_keywords_descriptions_[datetime of creation].csv': 
    Dimensions: 
    columns: four columns separated by semicolons (';'). I.e.
        |package_name|language|keywords|descriptions
    rows: four rows per package as one row is created per language. 
    Line is terminated with the string '|'.
    both separators (semicolon, |) are used, as the descriptions
    can contain not only all characters but also hypertext markups.
    
    
- 'opendataswiss_unique_keywords_[datetime of creation].csv':
    contains one line with all raw unique keywords used on opendata.swiss. 
    The unique keywords are comma-separated. 
    No corrections or stemming is done!

Please be aware that excel (and other programs) might mess up the encoding

"""

import csv
from datetime import datetime,timedelta
import pandas as pd
import requests
import time
import urllib3
import math


bund = True
test = False

now = datetime.now().strftime("%Y%m%d_%H-%M-%S")


def is_bv_netz():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxies = {"http":'http://proxy-bvcol.admin.ch:8080',
              "https":'http://proxy-bvcol.admin.ch:8080'}
    return proxies

def fetch_packages(test = bool, proxies = None):
    df_keywords_descriptions = pd.DataFrame({"name":[],
                            'language':[],
                            'keywords':[],
                            'description':[]})
    s = requests.Session()
    total_packages = s.get("https://ckan.opendata.swiss/api/3/action/package_search",
                         proxies=proxies,
                         verify=False).json()["result"]['count']

    languages = ['fr','de', 'en','it']
    base_URL = 'http://opendata.swiss/api/3/action/package_search?start='

    if test:
        limit_set=1
        nr_runs = 5
    else:
        limit_set = 10
        nr_runs = int(math.ceil(total_packages/limit_set))
        
    for i in range(nr_runs):
        try: # avoid errors by packages that are not datasets - such as showcases or harvesters - without running the query multiple times.
            result_packages = s.get(base_URL+str(i*limit_set), proxies=proxies,verify=False).json()["result"]["results"]

            for i in range(10):
                name = result_packages[i]['name']
                #print(name)
                for language in languages:
                    keywords = result_packages[i]['keywords'][language]
                    
                    description = result_packages[i]['description'][language]
                    df2 = pd.DataFrame({"name":[name],
                                        'language':[language],
                                        "keywords":[keywords],
                                        'description':[description]})
                    

                    df_keywords_descriptions = pd.concat([df_keywords_descriptions,df2], ignore_index=True)
                #print(df_keywords_descriptions)
        except:
            continue
    print(f'test is {test}')
    return df_keywords_descriptions


def create_list(df_keywords_descriptions):
    list_of_keywords = list()
    #list_of_description = list()
    result = list()
    list_of_keywords = df_keywords_descriptions['keywords'].tolist()
    for item in list_of_keywords:
        result.extend(item)
    unique_keywords = list(dict.fromkeys(result))
    return unique_keywords

def save_keywords_descriptions_as_csv(df_keywords_descriptions):
    #df_keywords_descriptions
    df_keywords_descriptions.to_csv('opendataswiss_keywords_descriptions_'+now+'.csv', 
                                    sep=';',index=False,line_terminator="|")
    
def save_unique_keywords_as_csv(unique_keywords):
    with open('opendataswiss_unique_keywords_'+now+'.csv','w') as file:
        write = csv.writer(file)
        write.writerow(unique_keywords)

def main(bund = bund, test=test):
    start = time.perf_counter()
    if bund:
        proxies = is_bv_netz()
    else: 
        proxies = None
    df_keywords_descriptions = fetch_packages(proxies=proxies, test=test)
    unique_keywords = create_list(df_keywords_descriptions)
    save_unique_keywords_as_csv(unique_keywords)
    save_keywords_descriptions_as_csv(df_keywords_descriptions)
    end = time.perf_counter()
    print('Job took: ',timedelta(seconds=end-start))

if __name__=='__main__':
    main(bund=bund,test=test)