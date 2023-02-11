# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 17:12:02 2022

@author: U80838962

Creates a list of organizations that joined recently with the date it joined.
- Recently is defined as having joined in the last [intervall] days. 
- Default value for intervall is 90 days.

prints list to screen and creates a csv-files



"""


import requests
import time
from datetime import datetime,timedelta
import urllib3 
import pandas as pd


start = time.perf_counter()


#### prepare variables and define requested intervall to be displayed

intervall = 90

now = datetime.now()
now = now.strftime("%Y%m%d_%H-%M-%S")

recent = datetime.now() - timedelta(days=intervall)


#prepare session and use proxies to call API outside of BV-net
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
          "http":'http://proxy-bvcol.admin.ch:8080',
          "https":'http://proxy-bvcol.admin.ch:8080'
        }



s = requests.Session()

#### request.get Organizations 
organizations = s.get('https://ckan.opendata.swiss/api/3/action/organization_list', proxies=proxies,verify=False).json()["result"]
base_URL_org = "https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:"


#### Run the query


df = pd.DataFrame({"name":[],"joined":[]})
    
for organization in range(len(organizations)):             # for testing

    try: # certain organizations do not have datasets, i.e. only their suborganisations have such
        name = organizations[organization]
        joined = s.get(base_URL_org+name, proxies=proxies,verify=False).json()["result"]["results"][0]["organization"]["created"]
        df2 = pd.DataFrame({"name":[name],"joined":[joined]})
        df2['joined'] = pd.to_datetime(df2['joined'])
        df = pd.concat([df,df2], ignore_index=True)
#    f.write(f"{organization} : {issued}")
#    f.write(\n)
    except:
        continue


# order dataframe as required and set dataformat in 'joined' as datetime
df.sort_values("joined",ascending=False, inplace=True)
df['joined'] = pd.to_datetime(df['joined'])

 
df_joined = df.loc[(df['joined'] > recent)]


### safe output
df_joined.to_csv("new_organizations_last_"+str(intervall)+"_days.txt", index=False, header=False)


### Alternative: print to screen
print(f"In the last {intervall} days, these organizations have been added to opendata.swiss: \n {df_joined}")     


end = time.perf_counter()

print('Job took: ',timedelta(seconds=end-start))

