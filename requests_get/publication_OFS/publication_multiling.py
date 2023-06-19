# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:34:45 2023
@author: U80838962

readme: for every publication, two things must be done manually:

    
    a)  The filenames for the csv must be defined.
        for the quarterly publication by the FSO, the fsoNr must be changed
        according to the respective file according to KOM_PUB! 
        > Q:\KOM_PUB\PUB\30_Input\Diffusion\00\
        this information is also used to name the file-names. 
        
    b) dict_slug_fr_it_de_en.csv must be up to date. The script checks this 
       and provides a feedback.
       This csv-file contains all slugs and their respective top-level name 
       in french, english, italian and german.
    
What does the script do? 
    1. input:
    - check if csv-file 'dict_slug_fr_it_de_en.csv' is up to date.
    - all further data is gathered via API-calls
    
    2. throughput:
    - get packages per slug
    - get language versions of toplevel_names (organization) per slug
    - get language versions of federal_levels per slug
    - aggregate to required level
    - query API for metadata
    
    3. output:
    - PACKAGES_TOP_LEVEL : packages per toplevel_name. for example, all 
      organizations from Kanton Zurichs administrations are grouped to ZH. 
    - PACKAGES_FED_LEVEL : packages per federal_level, e.g. federal, 
      cantonal, commune, other 
    - PACKAGES_DEP_LEVEL : packages per departement, eg. FDEA, DDPS, DETEC, 
      FDHA, FSO, etc.
    - CSV_OPENDATASWISS : csv File of metadata on opendata.swiss

"""

# required modules
import csv
import math
import pandas as pd
import requests as r
import time
import urllib3
from sys import exit
from os import remove

"""
## define variables:
## define filenames for the csv-files
"""
PACKAGES_FED_LEVEL = ['ts-d-00.02-OGD-01.csv','ts-f-00.02-OGD-01.csv',
                     'ts-i-00.02-OGD-01.csv','ts-e-00.02-OGD-01.csv']
PACKAGES_DEP_LEVEL = ['ts-d-00.02-OGD-02.csv','ts-f-00.02-OGD-02.csv',
                      'ts-i-00.02-OGD-02.csv','ts-e-00.02-OGD-02.csv']
PACKAGES_TOP_LEVEL = ['ts-d-00.02-OGD-04.csv','ts-f-00.02-OGD-04.csv',
                      'ts-i-00.02-OGD-04.csv','ts-e-00.02-OGD-04.csv']
 
CSV_OPENDATASWISS = ['ts-i-00.02-OGD-03 .csv', 'ts-d-00.02-OGD-03 .csv',
                      'ts-e-00.02-OGD-03 .csv', 'ts-f-00.02-OGD-03 .csv']

"""
## define variables:
## bund : Are you working within the bundesnetz resp. via vpn?
## test : Do you want to test the script or get all the information declared 
##        as wanted_package_info, wanted_organization_info and 
##        wanted_resource_info.
"""


BUND = True
TEST = False



def is_bv_netz(BUND):
     if BUND:
         urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
         proxies = {"http":'http://proxy-bvcol.admin.ch:8080',
               "https":'http://proxy-bvcol.admin.ch:8080'}
     else:
         proxies = None
     return proxies


def test_completeness_csv(proxies):
    s = r.Session()
    """ get list of orgnizations """
    listed_organizations = s.get('https://ckan.opendata.swiss/api/3/action/organization_list',
                                 verify=False,proxies=proxies).json()['result']
    organizations = []
    for slug in listed_organizations:
        try:
             s.get(f"https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:{slug}",
                   verify=False,proxies=proxies).json()['result']['results'][0]['organization']['political_level']
             organizations.append(slug)
        except IndexError:
            """
            # some organizations do not have packages as only their 
            # underorganisations publish. Skip these organizations
            """
            continue
        

    df_slug_toplevel_names = pd.read_csv("dict_slug_fr_it_de_en.csv")

    for slug in organizations:
        if slug not in df_slug_toplevel_names['organisation_slug'].unique() :
            exit(f'Organisation is not up to date. Add {slug} to \
dict_slug_fr_it_de_en.csv')

            
    print(f'dict_slug_fr_it_de_en.csv is up to date \nOrganizations on \
opendata.swiss: {len(listed_organizations)}')

    return organizations, df_slug_toplevel_names


def slug_packages(organizations,proxies):
    """
    # create dictionary with organization-slugs and corresponding number 
    # of packages 
    """
    s = r.Session()
    slugs_packages_dict = {} 
    for slug in organizations:
        nr_packages = s.get(f"https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:{slug}",
                            verify=False, proxies=proxies).json()['result']['count']
        slugs_packages_dict[slug] = nr_packages
    print(f'Publishing organizations: {len(organizations)}')
    nr_packages=[]
    for slug in slugs_packages_dict:
        nr_packages.append(slugs_packages_dict[slug])
    return slugs_packages_dict, nr_packages


def slug_names(slugs_packages_dict, df_slug_toplevel_names, organizations):
    fr_slug_name = pd.Series(df_slug_toplevel_names.top_level_name_fr.values,
                                  index= df_slug_toplevel_names.organisation_slug).to_dict()
    it_slug_name = pd.Series(df_slug_toplevel_names.top_level_name_it.values,
                                  index= df_slug_toplevel_names.organisation_slug).to_dict()
    de_slug_name = pd.Series(df_slug_toplevel_names.top_level_name_de.values,
                                  index= df_slug_toplevel_names.organisation_slug).to_dict()
    en_slug_name = pd.Series(df_slug_toplevel_names.top_level_name_en.values,
                                  index= df_slug_toplevel_names.organisation_slug).to_dict()
    names_fr = []
    names_it = []
    names_de = []
    names_en = []
    for slug in organizations:
        names_fr.append(fr_slug_name[slug])
    for slug in organizations:
        names_it.append(it_slug_name[slug])
    for slug in organizations:
        names_de.append(de_slug_name[slug])
    for slug in organizations:
        names_en.append(en_slug_name[slug])
        
    return names_fr, names_it, names_de, names_en

"""
## create dictionary with slugs and federal level using pandas.DataFrame() 
"""
def slug_federal_level(organizations, df_slug_toplevel_names, proxies):
    s = r.Session()
    levels_en = []    
    for i in organizations:
        political_level = s.get(f'https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:{i}',
                                verify=False,proxies=proxies).json()['result']['results'][0]['organization']['political_level']
        levels_en.append(political_level)
    federal_level_dict = pd.read_csv("dict_federallevels_fr_it_de_en.csv")
    fr_federal_level_dict = pd.Series(federal_level_dict.fr.values,
                                  index= federal_level_dict.en).to_dict()
    it_federal_level_dict = pd.Series(federal_level_dict.it.values,
                                  index= federal_level_dict.en).to_dict()
    de_federal_level_dict = pd.Series(federal_level_dict.de.values,
                                  index= federal_level_dict.en).to_dict()    
    levels_fr = []
    levels_it = []
    levels_de = []
    for slug in levels_en:
        levels_fr.append(fr_federal_level_dict[slug])
    for slug in levels_en:
        levels_it.append(it_federal_level_dict[slug])
    for slug in levels_en:
        levels_de.append(de_federal_level_dict[slug])
        
    return levels_fr, levels_it, levels_de, levels_en


def create_dataframe(organizations,nr_packages, names_fr, names_it, names_de, names_en, levels_fr, levels_it, levels_de, levels_en):
    df = pd.DataFrame(columns=['slugs','nr_packages','political_level',
                               'toplevel_fr','toplevel_it','toplevel_de',
                               'toplevel_en','levels_fr', 'levels_it', 
                               'levels_de', 'levels_en'])
    df['slugs'] = organizations
    df['nr_packages'] = nr_packages
    df['toplevel_fr'] = levels_en
    df['toplevel_fr'] = names_fr
    df['toplevel_it'] = names_it
    df['toplevel_de'] = names_de
    df['toplevel_en'] = names_en
    df['levels_en'] = levels_en
    df['levels_de'] = levels_de
    df['levels_fr'] = levels_fr
    df['levels_it'] = levels_it
    dataframe = df
    
    return dataframe


def create_csv_from_dataframe(dataframe,PACKAGES_TOP_LEVEL,PACKAGES_DEP_LEVEL,PACKAGES_FED_LEVEL):
    toplevels = ['toplevel_de','toplevel_fr','toplevel_it', 'toplevel_en']
    for index,value in enumerate(toplevels):
        df = dataframe[[value,'nr_packages']].copy()
        df['nr_packages'] = df.groupby([value])['nr_packages'].transform('sum')
        df = df.drop_duplicates()
           
        df.set_index(value,inplace=True)
        df.to_csv(PACKAGES_TOP_LEVEL[index],quoting = csv.QUOTE_ALL,
                  quotechar = '"',encoding= "utf_8_sig")
        """ #dep_level """
        df_dep = dataframe[['nr_packages','levels_en',value]].copy()
        df_dep = df_dep.loc[df_dep['levels_en']== "confederation"]
        df_dep['nr_packages'] = df_dep.groupby([value])['nr_packages'].transform('sum')
        df_dep = df_dep[[value,'nr_packages']]
        df_dep = df_dep.drop_duplicates()
        df_dep.set_index(value,inplace=True)
        df_dep.to_csv(PACKAGES_DEP_LEVEL[index], quoting = csv.QUOTE_ALL,
                      quotechar = '"', encoding= "utf_8_sig")
    """ # fed_pack"""
    levels = ['levels_de', 'levels_fr', 'levels_it', 'levels_en']
    for index,value in enumerate(levels):
        df = dataframe[[value,'nr_packages']].copy()
        df['nr_packages'] = df.groupby([value])['nr_packages'].transform('sum')
        df = df.drop_duplicates()
        df.set_index(value,inplace=True)
        df.to_csv(PACKAGES_TOP_LEVEL[index],quoting = csv.QUOTE_ALL, 
                  quotechar = '"',encoding= "utf_8_sig")


def fetch_packages(TEST, proxies):
    results = []
    s = r.Session()
    total_packages = s.get("https://ckan.opendata.swiss/api/3/action/package_search",
                           proxies=proxies,verify=False).json()["result"]['count']
    if TEST:
        limit_set=100
        nr_runs = 3
    else:
        limit_set = 1000
        nr_runs = int(math.ceil(total_packages/limit_set))
    print(f'limit_set: {limit_set}, \nnr_runs_required: {nr_runs}\n')
    for i in range(nr_runs):
        query_list = s.get(f"http://opendata.swiss/api/3/action/current_package_list_with_resources?offset={i*limit_set}&limit={limit_set}",
                            proxies=proxies, verify=False).json()["result"]
        results.extend(query_list)

    return results

def get_max_resources(results):
    max_resources = 0
    for nr,item in enumerate(results):
        x = results[nr]['num_resources']
        if x > max_resources:
            max_resources = x
        else:
            continue
    print(f'{max_resources} is max resources')

    return max_resources


def save_as_csv(results,max_resources):
    output = []
    error_list_res = []
    error_list_orgs = []
    error_list_write = []
    error_list_datasets = []
    wanted_package_info = [
        'name',
        'title_for_slug',
        'id',
        'owner_org',
        'maintainer',
        'type',
        'url',
        'metadata_created',
        'metadata_modified',
        'num_resources'
        ]
    wanted_organization_info = [
        'name', 
        'url',
        'package_count',
        'created',
        'political_level',
        'id'
        ]
    wanted_resource_info = [
        'id',
        'download_url',
        'created',
        'format',
        'rights',
        'url',
        'uri'
        ]
    columns = wanted_package_info.copy()
    columns.extend(wanted_organization_info)
    columns.extend(max_resources*wanted_resource_info)

    throughput_filename = "refactured_next_test_data_via_API.csv"
    with open (throughput_filename, 'w') as file:
        writer = csv.writer(file,dialect='excel', quoting=csv.QUOTE_ALL,)
        writer.writerow(columns)
        for nr,item in enumerate(results):
            throughput = []
            for info in wanted_package_info:
                """
                # some datasets have been added manually and have never been
                # modified - thus the field "modified" may be missing.
                """
                try:
                    info_data = results[nr][info]
                    throughput.append(info_data)
                except KeyError:
                    throughput.append('NaN')
                    error_list_datasets.append([nr,item,wanted_package_info])
                    continue
            try:
                for org_info in wanted_organization_info:
                    org_info_data = results[nr]['organization'][org_info]
                    throughput.append(org_info_data)
            except KeyError:
                throughput.append('NaN')
                error_list_orgs.append([nr, item,org_info])
                continue

            num_resources = results[nr]['num_resources']
            for resource in range(num_resources):
                    #print(resource)

                for resource_info in wanted_resource_info:
                    try:
                        resource_info_data = results[nr]['resources'][resource][resource_info]
                        throughput.append(resource_info_data)
                    except KeyError:
                        throughput.append('NaN')
                        error_list_res.append([nr, item,resource_info])
                        continue
            output.append(throughput)

        for dataset in output:
            try:
                writer.writerow(dataset)
            except UnicodeEncodeError as e:
                error_list_res.append([nr, item,resource_info])
                error_list_write.append([dataset, e])
                continue

    return throughput_filename,output


def fill_nan(CSV_OPENDATASWISS,throughput_filename,output):
    
    dataframe = pd.read_csv(
            throughput_filename,
            encoding='latin-1',
            low_memory=False,
            sep=',',
            #index_col=0
            )
    for names in CSV_OPENDATASWISS:
        dataframe.to_csv(
            names,
            na_rep='NaN',
            index=False,
            sep=',',
            quoting=csv.QUOTE_ALL, 
            encoding= "utf_8_sig"
            )
    print(dataframe.shape)
    remove(throughput_filename)



def main(BUND,TEST):
    start = time.perf_counter()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxies = is_bv_netz(BUND)
    organizations, df_slug_toplevel_names = test_completeness_csv(proxies)
    slugs_packages_dict, nr_packages = slug_packages(organizations,proxies)
    levels_fr, levels_it, levels_de, levels_en = slug_federal_level(organizations, 
                                                                    df_slug_toplevel_names,
                                                                    proxies)
    names_fr,names_it,names_de,names_en = slug_names(slugs_packages_dict, 
                                                     df_slug_toplevel_names, 
                                                     organizations)
    dataframe = create_dataframe(organizations,nr_packages, names_fr, names_it, 
                                 names_de, names_en, levels_fr, levels_it, 
                                 levels_de, levels_en)
    create_csv_from_dataframe(dataframe,PACKAGES_TOP_LEVEL,PACKAGES_DEP_LEVEL,
                              PACKAGES_FED_LEVEL)
    results = fetch_packages(TEST, proxies)
    max_resources = get_max_resources(results)
    throughput_filename,output = save_as_csv(results,max_resources)
    fill_nan(CSV_OPENDATASWISS,throughput_filename,output)
    end = time.perf_counter()
    print(f'{end-start} total runtime')

if __name__ == "__main__":
    main(BUND,TEST)
