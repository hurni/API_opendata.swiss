# <How to> API_opendata.swiss. All files are work in progress.

## How to use the CKAN-API of opendata.swiss for with python requests. 

Basic python scripts for practical applications of the CKAN-API of opendata.swiss. 

Examples are: 

_[ADD NAME OF REPO]_ : use requests.get() for basic reporting on datasets and organizations. 
As queries via the API of opendata.swiss do not require any authentification, anyone should be able to use this script.  

_[ADD NAME OF REPO]_ : create a python dictionaries and csv-files on 
    - organization_slugs and political_level
    - political_level and number of packages
    - swiss federal administration departements ("ministries") and number of packages
    - nr_packages grouped to the organisations top level (i.e. canton, swiss federal administration departement ("ministries"), city, ngo, etc.).

_[ADD NAME OF REPO]_ : use requests.post(). For usage: You need the proper role within your organization. In case of questions, please [contact opendata.swiss](mailto:opendata(at)bfs.admin.ch).
    - add packages resp. distributions (admin)
    - add users / organizations (sysadmin)

