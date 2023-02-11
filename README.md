# <How to> API_opendata.swiss. All files are work in progress.

## How to use the CKAN-API of opendata.swiss for with python requests. 

Basic python scripts for practical applications of the CKAN-API of opendata.swiss. Main module used: requests.get() and requests.post()

Examples are: 

[get_keywords_ogdswiss](https://github.com/hurni/API_opendata.swiss/blob/main/requests_get/get_keywords_ogdswiss.py) : use requests.get() for basic reporting on datasets and organizations. 
As queries via the API of opendata.swiss do not require any authentification, anyone should be able to use this script.  

[create_dictionarie_for_OGDswiss](https://github.com/hurni/API_opendata.swiss/blob/main/requests_get/create_dictionaries_for_OGDswiss.py) : create a python dictionaries and csv-files on 
- organization_slugs and political_level
- political_level and number of packages
- swiss federal administration departements ("ministries") and number of packages
- nr_packages grouped to the organisations top level (i.e. canton, swiss federal administration departement ("ministries"), city, ngo, etc.).

[resource_create](https://github.com/hurni/API_opendata.swiss/blob/main/requests_post/resource_create.py) : use requests.post(). For usage: You need the proper role within your organization. 
- add distributions to packages (admin)
- add users / organizations (sysadmin)

For more documentation, see the [handbook of opendata.swiss](https://handbook.opendata.swiss/) and the [official ckan API-guide]:(https://docs.ckan.org/en/2.9/api/index.html) 
In case of questions, please [contact opendata.swiss](mailto:opendata(at)bfs.admin.ch).
