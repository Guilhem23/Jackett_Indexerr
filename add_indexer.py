
# Edit with your values
jackett_apikey = "foo"
jackett_url = "https://localhost/jackett"
indexer_prefix = "AUTO: "

targets = [
    {
        "name": "sonarr",
        "apikey": "foo",
        "url" : "https://localhost/sonarr/api/",
        "categoryPrefixes": ["TV"],
        "animeCategoryPrefixes": ["Anime","TV"],
    },
    {
        "name": "radarr",
        "apikey": "foo",
        "url" : "https://localhost/radarr/api/",
        "categoryPrefixes": ["Movies"],
        "animeCategoryPrefixes": ["Anime","Movies"],
    },
    {
        "name": "lidarr",
        "apikey": "foo",
        "url" : "https://localhost/lidarr/api/v1/",
        "categoryPrefixes": ["Audio"]
    },
]

#Overriding category for an indexer
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

jackett_baseurl = jackett_url + "/api/v2.0/indexers/"
jackett_indexers_url = jackett_baseurl + "all/results/torznab/api?apikey=" + jackett_apikey + "&t=indexers&configured=true"

app_indexers_url = "indexer"
app_schema_url  = app_indexers_url + "/schema"
verbose = False

import urllib.request as request
import urllib
import json
import requests
import xmltodict

class MyHTTPRedirectHandler(request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

class ddict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

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

for t in targets:
    t = ddict(t)
    print("Adding " + str(len(indexers)) + " indexer to ", t.name)
    app_schemas = get_jsomparsed_data(t.url + app_schema_url + "?apikey="+t.apikey)
    app_indexers = get_jsomparsed_data(t.url + app_indexers_url + "?apikey="+t.apikey)

    for entry in range(0, len(app_schemas)):
        if app_schemas[entry]['implementation'] == "Torznab":
            req = app_schemas[entry]
            req['presets'] = []
            if verbose:
                print("Using Json template:")
                print(json.dumps(req, sort_keys=True, indent=4, separators=(',', ': ')))
    
    for idxr in indexers:
        #Does indexer exist ?
        for app_idxr in app_indexers:
            if idxr['@id'] in app_idxr['name']:
                print(app_idxr['name'], " already present! Removing")
                r = requests.delete(t['url'] + app_indexers_url + "/" + str(app_idxr['id']) + "?apikey=" + t['apikey'])
                if verbose:
                    print(t['url'] + app_indexers_url + "/" + str(app_idxr['id']) + "?apikey=" + t['apikey'])
                    print("[" + str(r.status_code) + "]")
                    print(json.dumps(r.json(), indent=4, sort_keys=True))

        print("Trying to add: " + idxr['@id'] + " to " + t['name'])
        req['name'] = indexer_prefix + idxr['@id']
        for k in req:
            if "Search" in k:
                req[k]= 'true'
            if "Rss" in k:
                req[k]= 'true'

        for section in req['fields']:
            if section['name'].lower() == "apikey":
                section['value'] = jackett_apikey
            if section['name'].lower() == "baseurl":
                section['value'] = indexer_url = jackett_baseurl + idxr['@id'] + "/results/torznab/"
            if section['name'].lower() == "categories":
                categories = []
                try:
                    categories.append(categories_override[idxr['@id']]['categories'])
                    print("Categories Override: ", categories)
                except:
                    for p in t['categoryPrefixes']:
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
                    anime_categories.append(categories_override[idxr['@id']]['anime_categories'])
                    print("Anime Categories Override: ", anime_categories)
                except:
                    for p in t['animeCategoryPrefixes']:
                        for c in idxr['caps']['categories']['category']:
                            if c['@name'].startswith(p):
                                anime_categories.append(int(c['@id']))
                
                if len(anime_categories) == 0:
                    print("No Anime Categories found using default...")
                else:
                    section['value'] = anime_categories
            
            if verbose:
                print(section)

        if verbose:
            print(json.dumps(req, sort_keys=True, indent=4))

        r = requests.post(t['url'] + app_indexers_url + "?apikey=" + t['apikey'], json=req)

        print("\tFinished: " + idxr['@id'] + " [" + str(r.status_code) + "]")
        if verbose and r.status_code != 201:
            print(json.dumps(r.json(), indent=4, sort_keys=True))
