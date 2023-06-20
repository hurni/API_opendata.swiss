# -*- coding: utf-8 -*-

# required modules

import requests as r
import time
import urllib3 
import csv
import math


## define variables: 
## bund : are you working within the bundesnetz resp. via vpn?
## test: do you want to test the script or get all the information declared as
## wanted_info and wanted_organization_info

bund = True
test = False


csv_file = "test_data_via_API.csv"

## proxy to call API outside of BV-net
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_bv_netz(bund):
    if bund:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        proxies = {"http":'http://proxy-bvcol.admin.ch:8080',
              "https":'http://proxy-bvcol.admin.ch:8080'}
    else:
        proxies = None
    return proxies

def fetch_packages(test, proxies):
    results = []
    s = r.Session()
    total_packages = s.get("https://ckan.opendata.swiss/api/3/action/package_search",
                         proxies=proxies,
                         verify=False).json()["result"]['count']
    if test:
        limit_set=1
        nr_runs = 5
    else:
        limit_set = 10
        nr_runs = int(math.ceil(total_packages/limit_set))
    print(f'limit_set: {limit_set}, \nnr_runs_required: {nr_runs}')
    for i in range(nr_runs):
        query_list = s.get("http://opendata.swiss/api/3/action/package_search?start="+str(i*limit_set),
                           proxies=proxies,
                           verify=False).json()["result"]["results"]
        results.extend(query_list)
    return results

def save_as_csv(csv_file,results):
    wanted_info = ['name',
               'title_for_slug',
               'id',
               'maintainer_email',
               'type',
               'metadata_created',
               'metadata_modified',
               'modified',
               'num_resources']
    wanted_organization_info = ['name','political_level','id']
    columns = wanted_info.copy()
    columns.extend(wanted_organization_info)

    error_list_datasets = []
    error_list_orgs = []
    output = []
    
    with open (csv_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for nr,item in enumerate(results):
            throughput = list()
            try: # some datasets have been added manually and have never been 
                 # modified - thus the field "modified" is missing.
                for info in wanted_info:
                    info_data = results[nr][info]
                    throughput.append(info_data)
            except KeyError as e:
                ids = item['id']
                error_list_datasets.append([ids, e.args[0]])
                
                s = r.Session()
                proxies = {"http":'http://proxy-bvcol.admin.ch:8080',"https":'http://proxy-bvcol.admin.ch:8080'}
                private_api_key = YOUR_API_KEY # see https://ckan.opendata.swiss/de/user/YOUR_USER_NAME
                url = 'https://ckan.opendata.swiss/api/3/action/package_patch'
                header = {'Authorization': private_api_key}
                data = {
                        'id': ids,
                        e.args[0] : ''
                        }
                s.post(url,data=data,proxies=proxies,headers=header,verify=False)
                
                continue

            try:
                for org_info in wanted_organization_info:
                    org_info_data = results[nr]['organization'][org_info]
                    throughput.append(org_info_data)
            except KeyError:
                throughput.append('NaN')
                error_list_orgs.append([nr, item,org_info])
                continue
            output.append(throughput)

        for dataset in output:
            writer.writerow(dataset)

def main(bund,test):
    start = time.perf_counter()
    proxies = is_bv_netz(bund)
    print(f'bundesnetz is {bund},\ntest is {test}')
    print(f'{proxies}\n')
    split_1 = time.perf_counter()
    results = fetch_packages(test, proxies)
    print(f'{fetch_packages} finished')
    split_2 = time.perf_counter()
    save_as_csv(csv_file, results)
    print(f'{save_as_csv} finished')
    end = time.perf_counter()
    total = end - start

    print(f'{total}: total runtime, with \n\
    {split_1-start}: setup and getting package names, \n\
    {split_2-split_1}: create list with all packages, and\n\
    {end-split_2}: retrieve the required data from list and save as csv-file')


if __name__ == "__main__":
    main(bund=True,test=False)

