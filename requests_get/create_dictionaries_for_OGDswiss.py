# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 21:21:45 2022

@author: haema

creates dictionaries/lists/csv-file.

name_packages_dict = organisation name : nr packages
> organization name entspricht slug/name.

toplevel_dictionary = organization_name : top_level.
> toplevel is the departement (exception: BFS), canton, commune or ngo-name 
  that suborganizations share.
  
toplevel_packages_dict = toplevel and number of packages

org_political_Level_dict = organization_slugs and political_level 
> political_level is federal, canton, commune or other



"""

# required modules
import requests as r
import time
import pandas as pd
import urllib3
import csv
#import json
#import math


start = time.perf_counter()

# To be updated manually, when new organisations join 
toplevel_dictionary = {
    'canton-du-jura': 'JU',
    'kantonspolizei-kanton-zuerich': 'ZH',
    'kanton-basel-landschaft' : 'BL',
    'agroscope' : 'WBF',
    'awel-kanton-zuerich' : 'ZH',
    'amt-fuer-geoinformation-des-kantons-bern' : 'BE',
    'amt-geoinformation-kanton-schaffhausen' : 'SH',
    'are-kanton-zuerich' : 'ZH',
    'amt-fuer-raumentwicklung-und-geoinformation-areg-kanton-st-gallen' : 'SG',
    'bernmobil' : 'bernmobil',
    'bibliothek-am-guisanplatz-big' : 'VBS',
    'bildungsstatistik-kanton-zuerich' : 'ZH',
    'bundesamt-fur-bevolkerungsschutz-babs' : 'VBS',
    'bundesamt-fur-energie-bfe' : 'UVEK',
    'bundesamt-fur-gesundheit-bag' : 'EDI (ohne BFS und BAR)',
    'bundesamt_fuer_justiz' : 'EJPD',
    'bundesamt-fur-kommunikation-bakom' : 'UVEK',
    'bundesamt-fur-kultur-bak' : 'EDI (ohne BFS und BAR)',
    'bundesamt-fur-landestopografie-swisstopo' : 'VBS',
    'bundesamt-fur-landwirtschaft-blw' : 'WBF',
    'bundesamt-fur-meteorologie-und-klimatologie-meteoschweiz' : 'EDI (ohne BFS und BAR)',
    'bundesamt-fur-raumentwicklung-are' : 'UVEK',
    'bundesamt-fur-statistik-bfs' : 'BFS (EDI)',
    'bundesamt-fur-strassen-astra' : 'UVEK',
    'bundesamt-fur-umwelt-bafu' : 'UVEK',
    'bundesamt-fur-verkehr-bav' : 'UVEK',
    'bundesamt-fur-zivilluftfahrt-bazl' : 'UVEK',
    'eidgenoessische_zollverwaltung_ezv' : 'EFD',
    'dienst-ueberwachung-post-und-fernmeldeverkehr-uepf' : 'EJPD',
    'dienstzweig-geomatik-gemeinde-koeniz' : 'Koeniz',
    'swisspost' : 'Die Post',
    'direktion-fur-entwicklung-und-zusammenarbeit-deza' :  'EDA',
    'eidgenossische-finanzverwaltung-efv' : 'EFD',
    'wsl' : 'WSL',
    'eidgenoessisches_amt_fuer_das_handelsregister_ehra' : 'EJPD',
    'envidat' : 'envidat',
    'eth-bibliothek' : 'ETH Zurich',
    'fachstelle-fur-statistik-kanton-st-gallen' : 'SH',
    'fachstelle-geoinformation-des-kantons-glarus' : 'GL',
    'fachstelle-ogd-kanton-zuerich' : 'ZH',
    'efv_finanzstatistik' : 'EFD',
    'finanzverwaltung-der-stadt-bern' : 'Bern',
    'finanzverwaltung-kanton-zuerich' : 'ZH',
    'gemeindeamt-kanton-zuerich' : 'ZH',
    'gemeinde_emmen' : 'Emmen',
    'gemeinde_koeniz' : 'Koeniz',
    'geoimpact' : 'Geoimpact',
    'geoinformation_kanton_freiburg' : 'FR',
    'geoinformation-kanton-zuerich' : 'ZH',
    'geoinformation-der-stadt-bern' : 'Bern',
    'geschaeftsfeld-gesellschaft-stadt-uster' : 'Uster',
    'oevch' : 'SBB',
    'gesundheitsdirektion-kanton-zuerich' : 'ZH',
    'gis-kanton-zug' : 'ZG',
    'gruppe-verteidigung' : 'VBS',
    'handelsregisteramt-kanton-zuerich' : 'ZH',
    'identitas' : 'Identitas',
    'immobilien-stadt-bern' : 'Bern',
    'administration-cantonale-geneve' : 'GE',
    'kanton-basel-stadt' : 'BS',
    'kanton-bern-2' : 'BE',
    'kanton_freiburg' : 'FR',
    'canton-geneve' : 'GE',
    'kanton-glarus' : 'GL',
    'kanton-graubuenden' : 'GR',
    'kanton_luzern' : 'LU',
    'kanton-schaffhausen' : 'LU',
    'kanton-st-gallen' : 'SG',
    'kanton-thurgau' : 'TG',
    'kanton-wallis' : 'VS',
    'kanton-zuerich' : 'ZH',
    'kanton-zug' : 'ZG',
    'kof-konjunkturforschungsstelle' : 'ETH Zurich',
    'lustat' : 'LU',
    'oberjugendanwaltschaft-kanton-zuerich' : 'ZH',
    'openglam' : 'openglam',
    'ostschweiz_tourismus' : 'Ostschweiz Tourismus',
    'parlamentsdienste-pd' : 'Parlamentsdienste',
    'participatory-image-archives' : 'PIA - Participatory Image Archives',
    'personalamt-kanton-zuerich' : 'ZH',
    'schweizerische-bundesbahnen-sbb' : 'SBB',
    'schweizerische-nationalbibliothek-nb' : 'SNB', 
    'schweizerischer-nationalfonds-zur-forderung-der-wissenschaftlichen-forschung-snf': 'SNF',
    'schweizerisches-bundesarchiv-bar' : 'BAR - Schweizerisches Bundesarchiv (EDI)',
    'sik-isea' : 'Schweizerisches Institut fuer Kunstwissenschaften',
    'schweizerisches-nationalmuseum-snm' : 'SNM - Schweizerisches Nationalmuseum',
    'sitg-systeme-dinformation-du-territoire-a-geneve' : 'GE',
    'schweizer-radio-und-fernsehen-srg' : 'SRG SSR',
    'staatsarchiv-kanton-zuerich' : 'ZH',
    'staatskanzlei-kanton-st-gallen' : 'SG',
    'staatskanzlei-kanton-zuerich' : 'ZH',
    'staatskanzlei-zug' : 'ZG',
    'sbfi' : 'WBF',
    'staatssekretariat-fuer-migration-sem' : 'EJPD',
    'stadtarchiv-bern' : 'Bern',
    'stadt-bern' : 'Bern',
    'stadt-luzern' : 'Luzern',
    'stadtrat-bern' : 'Bern',
    'stadt-uster' : 'Uster',
    'stadt-winterthur' : 'Winterthur',
    'stadt-zurich' : 'Zuerich',
    'standeskanzlei-graubuenden' : 'GR',
    'statistik-stadt-bern' : 'Bern',
    'statistisches-amt-kanton-zuerich' : 'ZH',
    'swissbib' : 'swissbib (eingestellt)',
    'swissmedic' : 'swissmedic',
    'tiefbauamt-kanton-zuerich' : 'ZH', 'unabhangige-expertenkommission-uek-administrative-versorgungen' : 'UEK Administrative Versorgung (eingestellt)',
    'volksschulamt-kanton-zuerich' : 'ZH',
    'digitale_medien_der_armee_dma' : 'VBS',
    'canton-du-valais-cc-geo' : 'VS',
    'eth-zuerich' : 'ETH Zurich'
    }


s = r.Session()

## condition and proxy to call API from within the BV-net
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



proxies = {
           'http':'http://proxy-bvcol.admin.ch:8080',
           'https':'http://proxy-bvcol.admin.ch:8080'
         }



# get list of orgnizations
organizations = s.get('https://ckan.opendata.swiss/api/3/action/organization_list',verify=False,proxies=proxies).json()['result']

# create dictionary with organization-slugs and corresponding number of packages 
name_packages_dict = {} 
for i in organizations:
    nr_packages = s.get("https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:"+i,verify=False, proxies=proxies).json()['result']['count']
    name_packages_dict[i] = nr_packages

# create dictionary with toplevel-names and corresponding number of packages using pandas.DataFrame() #toplevel_packages_dict = {}

df = pd.DataFrame(columns=['top_level','nr_packages'])
df['top_level'] = pd.Series(toplevel_dictionary) 
df["nr_packages"] = pd.Series(name_packages_dict) 
df['nr_packages'] = df.groupby(['top_level'])['nr_packages'].transform('sum')
df = df.drop_duplicates()
df.set_index('top_level',inplace=True)
df.to_csv('toplevel_packages_dict.csv')

# create dictionary with organization_slugs and political_level:
org_political_Level_dict = {}
for i in organizations:
     try:
         political_level = s.get("https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:"+i,verify=False,proxies=proxies).json()['result']['results'][0]['organization']['political_level']
         org_political_Level_dict[i] = political_level
     except IndexError:
         continue

# create dictionary with political_level and corresponding number of packages using pandas.DataFrame() 
df_pl = pd.DataFrame(columns=['political_level','nr_packages'])
df_pl['political_level'] = pd.Series(org_political_Level_dict)
df_pl["nr_packages"] = pd.Series(name_packages_dict)

## sum nr_packages per top_level
df_pl['nr_packages'] = df_pl.groupby(['political_level'])['nr_packages'].transform('sum')
df_pl = df_pl.drop_duplicates()
df_pl.set_index('political_level',inplace=True)
df_pl.to_csv('political_level_packages_dict.csv')

# create dictionary with toplevel=departement and corresponding number of packages using pandas.DataFrame() 
departement = ['WBF','EDA','UVEK','VBS','EDI (ohne BFS und BAR)','BAR - Schweizerisches Bundesarchiv (EDI)','BFS (EDI)','EJPD'] 
df_dep = pd.DataFrame(columns=['departement','nr_packages'])
df_dep['departement'] = pd.Series(toplevel_dictionary) 
df_dep["nr_packages"] = pd.Series(name_packages_dict)

## sum nr_packages per top_level
df_dep['nr_packages'] = df_dep.groupby(['departement'])['nr_packages'].transform('sum')
df_dep = df_dep.drop_duplicates()
df_dep = df_dep[df_dep['departement'].isin(departement)]
df_dep.set_index('departement',inplace=True)
df_dep.to_csv('departemente_packages_dict.csv')

# create list with all cantons and corresponding number of packages using pandas.DataFrame() 

cantons_org = [] 
canton = []

#list of keys
for key in org_political_Level_dict:
     if org_political_Level_dict[key] == 'canton':
         cantons_org.append(key)

for organisation in cantons_org:
     kuerzel = toplevel_dictionary[organisation]
     canton.append(kuerzel)


df_cantons = pd.DataFrame(columns=['cantons','nr_packages'])
df_cantons['cantons'] = pd.Series(toplevel_dictionary) 
df_cantons["nr_packages"] = pd.Series(name_packages_dict)

## sum nr_packages per top_level
df_cantons['nr_packages'] = df_cantons.groupby(['cantons'])['nr_packages'].transform('sum')
df_cantons = df_cantons.drop_duplicates() 
df_cantons = df_cantons[df_cantons['cantons'].isin(canton)]
df_cantons.set_index('cantons',inplace=True)
df_cantons.to_csv('cantons_packages_dict.csv')

# creating csv-files from dictionaries
with open('toplevel_dictionary.csv', 'w', newline='') as csvfile:
     header_key = ['organisation_slug', 'top_level_name']
     new_val = csv.DictWriter(csvfile, fieldnames=header_key)
     new_val.writeheader()
     for new_k in toplevel_dictionary:
         new_val.writerow({'organisation_slug': new_k, 'top_level_name':
toplevel_dictionary[new_k]})

with open('name_packages_dict.csv', 'w', newline='') as csvfile:
     header_key = ['organisation_slug', 'nr_packages']
     new_val = csv.DictWriter(csvfile, fieldnames=header_key)
     new_val.writeheader()
     for new_k in name_packages_dict:
         new_val.writerow({'organisation_slug': new_k, 'nr_packages':
name_packages_dict[new_k]})

with open('org_political_Level_dict.csv', 'w', newline='') as csvfile:
     header_key = ['organisation_slug', 'political_level']
     new_val = csv.DictWriter(csvfile, fieldnames=header_key)
     new_val.writeheader()
     for new_k in org_political_Level_dict:
         new_val.writerow({'organisation_slug': new_k,
'political_level': org_political_Level_dict[new_k]})

end = time.perf_counter()
print(f'{end-start} total runtime.')


