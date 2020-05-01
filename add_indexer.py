# Advanced usage not yet in config file ...
# Overriding category for an indexer
categories_override = {
    "cpasbienclone" : {
        "categories" : "7000",
        "anime_categories" : "7000"
    },
     "my_favorite_tracker" : {
         "categories" : "2000",
         "anime_categories" : "5000"
     }
}

# Do not edit under this line

import urllib
import urllib.request as request
import json
import requests
import xmltodict
from config import config

jackett_baseurl = config['default']['jackett_url'] + "/api/v2.0/indexers/"
jackett_indexers_url =  jackett_baseurl + "all/results/torznab/api?apikey=" + \
                        config['default']['jackett_apikey'] + "&t=indexers&configured=true"

app_indexers_url = "indexer"
app_schema_url  = app_indexers_url + "/schema"
verbose = False

class MyHTTPRedirectHandler(request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

def get_jsomparsed_data_from_xml(url):
    response = request.urlopen(url)
    data = response.read().decode("utf-8")
    my_dict=xmltodict.parse(data)
    return json.loads(json.dumps(my_dict))

def get_jsomparsed_data(url):
    response = request.urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


cookieprocessor = request.HTTPCookieProcessor()
opener = request.build_opener(MyHTTPRedirectHandler, cookieprocessor)
request.install_opener(opener)

all_indexers = get_jsomparsed_data_from_xml(jackett_indexers_url)
indexers = [x for x in all_indexers['indexers']['indexer']]

print(str(len(indexers)) + " indexers availlable in Jackett ")

def add_indexers(app):
    app_schemas = get_jsomparsed_data(config[app]['url'] + app_schema_url + "?apikey="+config[app]['apikey'])
    app_indexers = get_jsomparsed_data(config[app]['url'] + app_indexers_url + "?apikey="+config[app]['apikey'])

    for schema in app_schemas:
        if schema['implementation'] == "Torznab":
            del schema['presets']
            if verbose:
                print("Using Json template:")
                print(json.dumps(schema, sort_keys=True, indent=4, separators=(',', ': ')))
            break

    for idxr in indexers:
        #Does indexer exist ?
        exist = 0
        changed = True

        for app_idxr in app_indexers:
            if idxr['@id'] in app_idxr['name']:
                exist = app_idxr['id']
                changed = False
                break

        schema['name'] = config['default']['indexer_prefix'] + " " + idxr['@id']
        for k in schema:
            if "Search" in k or "Rss" in k:
                schema[k]= 'true'
                if exist != 0 and app_idxr[k] != True:
                    changed = True
                    print(app_idxr['name'], " ", k, " ", app_idxr[k])

        for section in schema['fields']:
            if section['name'].lower() == "apikey":
                section['value'] = config['default']['jackett_apikey']
            if section['name'].lower() == "baseurl":
                section['value'] = jackett_baseurl + idxr['@id'] + "/results/torznab/"
            if section['name'].lower() == "categories":
                categories = []
                try:
                    categories.append(int(categories_override[idxr['@id']]['categories']))
                    print("Categories Override: ", categories)
                except:
                    for p in config[app]['categoryPrefixes']:
                        for c in idxr['caps']['categories']['category']:
                            if c['@name'].startswith(p):
                                categories.append(int(c['@id']))
                
                if len(categories) == 0:
                    print("No Categories found using default...")
                else:
                    section['value'] = categories

            if section['name'].lower() == "animecategories":
                anime_categories = []
                try:
                    anime_categories.append(int(categories_override[idxr['@id']]['anime_categories']))
                    print("Anime Categories Override: ", anime_categories)
                except:
                    for p in config[app]['animeCategoryPrefixes']:
                        for c in idxr['caps']['categories']['category']:
                            if c['@name'].startswith(p):
                                anime_categories.append(int(c['@id']))

                if len(anime_categories) == 0:
                    print("No Anime Categories found using default...")
                else:
                    section['value'] = anime_categories
            try:
                if exist != 0 and app_idxr['fields'][schema['fields'].index(section)]['value'] != section['value']:
                    changed = True
                    print("Value changed ", section['name'], " ", section['value'], " ", app_idxr['fields'][schema['fields'].index(section)]['value'])
            except:
                if verbose:
                    print("No key Value!! in ", section['name'])
            if verbose:
                print(section)

        if verbose:
            print(json.dumps(schema, sort_keys=True, indent=4))
        if exist != 0 and changed is not False:
            print(app_idxr['name'], " already present, removing!")
            r = requests.delete(config[app]['url'] + app_indexers_url + "/" + str(app_idxr['id']) + "?apikey=" + config[app]['apikey'])
            if verbose:
                print(config[app]['url'] + app_indexers_url + "/" + str(app_idxr['id']) + "?apikey=" + config[app]['apikey'])
                print("[" + str(r.status_code) + "]")
                print(json.dumps(r.json(), indent=4, sort_keys=True))


        if changed is not False:
            print("Trying to add: " + idxr['@id'] + " to " + app)
            r = requests.post(config[app]['url'] + app_indexers_url + "?apikey=" + config[app]['apikey'], json=schema)

            print("Finished: " + idxr['@id'] + " [" + str(r.status_code) + "]")
            if r.status_code != 201:
                print(json.dumps(r.json(), indent=4, sort_keys=True))


for app in config.sections():
    if app != "default":
        add_indexers(app)
