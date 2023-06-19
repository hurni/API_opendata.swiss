
##########
# Fetch selected datasets from PROD opendata.swiss and save a copy on ABNAHME.
# Selection criteria: part of group 'energy' or having keywords 'energy' or 'energie' 
# Recquired: You need a useraccount/organization on ABNAHME environment or -more 
# precisely- your API Key.
##########


import requests as r
import urllib3 
import math
import random


## set variables: 
## BUND : Are you working within the bundesnetz resp. via vpn?
## TEST : Do you want to test the script or push all the information declared 
##        as wanted_info and wanted_organization_info?

BUND = True
TEST = False


## Your credentials are required to change metadata of your organization. 
## Check information on your account of the ABNAHME environment
PRIVATE_API_KEY = "YOUR_API_KEY" # 

# Your organization's information for destination organization.
# If you do not know the information, use the API (JSON) button 
# of any dataset of your organization.
NEW_ORG_ID = "2b05df07-14af-4c21-8be4-9fe0ac4a0f04"
NEW_ORG_SLUG = "switch_opendata"

def is_bv_netz(BUND):
    if BUND:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        proxies = {"http": "http://proxy-bvcol.admin.ch:8080",
              "https":"http://proxy-bvcol.admin.ch:8080"}
    else:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        proxies = None
    return proxies

def fetch_packages(TEST, proxies):
    result_list = []
    keyword_list = []
    s = r.Session()

    total_packages_groups = s.get("https://ckan.opendata.swiss/api/3/action/package_search?fq=groups:energy",
                         proxies=proxies,
                         verify=False).json()["result"]["count"]
    if TEST:
        limit_set=1
        nr_runs_groups = 1
    else:
        limit_set = 1000
        nr_runs_groups = int(math.ceil(total_packages_groups/limit_set))
    
    # add packages from group "energy" to result_list
    for i in range(nr_runs_groups):
        query_list = s.get(f"https://ckan.opendata.swiss/api/3/action/package_search?q=groups:energy&rows={str(limit_set)}&start={str(i*limit_set)}",
                           proxies=proxies,
                           verify=False).json()["result"]["results"]
        result_list.extend(query_list)   
    print(f"{len(result_list)} packages for group \'energie\'")
    
    # add packages with keyword "energy" or "energie" to result_list
    total_packages_keywords = s.get("https://ckan.opendata.swiss/api/3/action/package_search?q=keywords%3D%28energy+OR+energie%29",
                         proxies=proxies,
                         verify=False).json()["result"]["count"]
    if TEST:
        limit_set=1
        nr_runs_keywords = 1
    else:
        limit_set = 1000
        nr_runs_keywords = int(math.ceil(total_packages_keywords/limit_set))

    for i in range(nr_runs_keywords):
        query_list = s.get(f"https://ckan.opendata.swiss/api/3/action/package_search?q=keywords%3D%28energy+OR+energie%29&rows={str(limit_set)}&start={str(i*limit_set)}",
                           proxies=proxies,
                           verify=False).json()["result"]["results"]
        keyword_list.extend(query_list)
        result_list.extend(query_list)

    #cleanup - remove duplicates
    clean_results = [i for n, i in enumerate(result_list) if i not in result_list[n + 1:]]
    print(f"{len(clean_results)} total packages")

    return clean_results


def prepare_and_repost(clean_results,new_org,proxies):

    header = {"Authorization": PRIVATE_API_KEY}

    required_attributes_dataset = [
        "name",
        "identifier",
        "title_for_slug",
        "display_name",
        "publisher",
        "issued",
        "contact_points",
        "description",
        "title",
        "private",
        "isopen",
        "type",
        "accrual_periodicity",
        "owner_org",
        "url",
        "resources",
        "groups",
        "see_alsos",
        "num_resources"
        ]

    required_attributes_resource = [
        "issued",
        "display_name",
        "title",
        "download_url",
        "state",
        "description",
        "name",
        "rights",
        "url",
        "identifier",
        "format"
        ]
        
    for i in clean_results:
        # add random number to avoid collisions with existing slugs
        randomizer = str(random.randrange(100000))
        remove_characters = [" ",".",":","ä","ö","ü","é","è","à"]
        
        original_identifier = i["identifier"]
        original_identifier = str(original_identifier).lower()
        
        for char in remove_characters:
            original_identifier = original_identifier.replace(char, "")
        
        i["see_alsos"] = [{"dataset_identifier" : original_identifier}]
        i["owner_org"] = NEW_ORG_ID
        
        new_title_for_slug = i["title_for_slug"]
        new_title_for_slug = new_title_for_slug.lower()

        for char in remove_characters:
            new_title_for_slug = new_title_for_slug.replace(char, "")

        new_title_for_slug = new_title_for_slug[:15]+(f"_{randomizer}")
        
        i["name"] = new_title_for_slug
        i["title_for_slug"] = new_title_for_slug
            
        i["identifier"] = str(f"{new_title_for_slug}@{NEW_ORG_SLUG}")

        
        for key in i["resources"]:
            rand = str(random.randrange(256))
            key["identifier"] = str(f"resource_{new_title_for_slug}_{rand}@{NEW_ORG_SLUG}")
    clean_up = clean_results.copy()

    url_post = "https://ckan.ogdch-abnahme.clients.liip.ch/api/3/action/package_create"
    for dataset in clean_up:
        num_resources = dataset["num_resources"]
        try:
            del dataset["modified"]
        except KeyError:
            continue

        for key in dataset.copy():
            if key not in required_attributes_dataset:
                del dataset[key]
            if key == "resources":
                for resource in range(num_resources):
                    try:
                        del dataset["resources"][resource]["modified"]
                    except KeyError:
                        continue
                    dataset["resources"][resource]["download_url"] = dataset["resources"][resource]["url"]
                    for resource_key in dataset["resources"][resource].copy():
                        res = dataset["resources"][resource]
                        if resource_key not in required_attributes_resource:
                            del res[resource_key]
        
        s = r.Session()                    
        x = s.post(url_post, json=dataset, headers=header, proxies=proxies,verify=False)
        print(x.status_code)

    return clean_results
    

def main(BUND,TEST):
    proxies = is_bv_netz(BUND)
    clean_results = fetch_packages(TEST, proxies)
    prepare_and_repost(clean_results, NEW_ORG_ID, proxies)    

if __name__ == "__main__":
    main(BUND,TEST)
