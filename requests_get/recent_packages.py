# -*- coding: utf-8 -*-
"""
@author: U80838962

script  to track the packages on opendata.swiss via the API call function.

Creates a csv containing  the relevant metadata.

"""

import requests
import time
from datetime import datetime,timedelta
import urllib3 
import pandas as pd

start = time.perf_counter()

#### prepare variables and define requested intervall to be displayed
intervall = 100

now = datetime.now().strftime("%Y%m%d_%H-%M-%S")
recent = datetime.now() - timedelta(days=intervall)


#prepare session and use proxies to call API outside of BV-net
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
          "http":'http://proxy-bvcol.admin.ch:8080',
          "https":'http://proxy-bvcol.admin.ch:8080'
        }

s = requests.Session()


#### Packages
# list of alls package_ids
packages = s.get('https://opendata.swiss/api/3/action/package_list', proxies=proxies,verify=False).json()["result"] 
base_URL = "https://ckan.opendata.swiss/api/3/action/package_show?id="

#### Run the query

#df = pd.DataFrame({'publisher':[],"name":[],"added":[],"modified":[]})
df = pd.DataFrame({'organization':[],"name":[],"added":[]})

### for testing
#for package in range(7525,7535):
for package in range(len(packages)):             
    try: # avoid errors by packages that are not datasets. Such as showcases or harvesters.
        name = packages[package]
   
        added = s.get(base_URL+name, proxies=proxies,verify=False).json()["result"]["metadata_created"]
        publisher = s.get(base_URL+name, proxies=proxies,verify=False).json()["result"]['organization']['name']
        #modified = s.get(base_URL+name, proxies=proxies,verify=False).json()["result"]["metadata_modified"]
        df2 = pd.DataFrame({'publisher':[publisher],"name":[name],"added":[added],})
        #df2 = pd.DataFrame({'publisher':[publisher],"name":[name],"added":[added],"modified":[modified]})
        df = pd.concat([df,df2], ignore_index=True)
#    f.write(f"{organization} : {issued}")
#    f.write(\n)

    except:
        continue


### selecting according to "added" to create a csv with most recent changes
# order dataframe as required
df_added = df.sort_values("added",ascending=False, inplace=True)

# set format in "added" to datetime
df['added'] = pd.to_datetime(df['added'])

# select the required datarange 
df_added = df.loc[(df['added'] > recent)]
df_added = df_added[['publisher',"name","added"]]
total_added_packages = len(df_added)


### save output
#output_modified = df_modified.to_string(index=False, header=['publisher',"title for slug","date modified"])
output_added = df_added.to_string(index=False, header=['publisher',"title for slug","date added"])



# save-as location
packages_added = "packages_added_last_"+str(intervall)+"_days.txt"
#packages_modified = "packages_modified_last_"+str(intervall)+"_days.txt"


 
with open (packages_added, 'w') as f:

    f.write(f"In the last {intervall} days, a total of {total_added_packages} packages have been to opendata.swiss. \n\n")

    if total_added_packages != 0:
                
        example_added = df_added.iloc[0][0]
        
        f.write("Below you find the title for slug and the date they have been added. To directly access a dataset,  you can add its slug")
        f.write(" to the following address: opendata.swiss/dataset/; e.g.:")
        f.write(f"\n\n<https://ckan.opendata.swiss/dataset/{example_added}> \n\n\n")
        f.write(f"{output_added}")
 
"""
with open (packages_modified, 'w') as f:

    f.write(f"In the last {intervall} days, a total of {total_modified_packages} packages have been modified on opendata.swiss. \n\n")


    if total_modified_packages != 0:
        
        example_modified = df_modified.iloc[0][0]
        
        f.write("Below you find their slugs and the date of change. To directly access a dataset,  you can add its name")
        f.write(" to the following address: opendata.swiss/dataset/; e.g.:")
        f.write(f"\n\n<https://ckan.opendata.swiss/dataset/{example_modified}> \n\n\n")
        f.write(f"{output_modified}")
 
"""

### Alternative: print to screen
#print(f"In the last {intervall} days, these packages have been modified opendata.swiss: \n\n {df_modified}")
print(f"In the last {intervall} days, these packages have been added to opendata.swiss: \n\n {df_added}")     



end = time.perf_counter()

print('Job took: ',timedelta(seconds=end-start))

