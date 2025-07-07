# Do not edit under this line

import json
import requests
import xmltodict
from config import config

jackett_base_url = config['default']['jackett_url'] + "/api/v2.0/indexers"
jackett_torznabs_url =  jackett_base_url + "/all/results/torznab/api?apikey=" + \
                        config['default']['jackett_apikey'] + "&t=indexers&configured=true"
jackett_indexers_url =  jackett_base_url + "?apikey=" + config['default']['jackett_apikey'] + "&t=indexers&configured=true"                        

verbose = False

def print_encoded(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # Converter caracteres problemáticos
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)

def get_jackett_session(pwd):
    session = requests.Session()
    login_data = {'password': pwd}
    login_response = session.post(
        f"{config['default']['jackett_url']}/UI/Dashboard",
        data=login_data,
        allow_redirects=True
    )
    if login_response.status_code == 200:
        return session
    else:
        print_encoded(f"[{login_response.status_code}] Login error to Jackett")
        return None

def get_jsonparsed_data_from_xml(url, headers, session=None):
    if (session==None):
        response = requests.get(url, headers)
    else:
        response = session.get(url)
    response.encoding = "utf-8"
    data = response.text
    my_dict=xmltodict.parse(data)
    return json.loads(json.dumps(my_dict))

def get_jsonparsed_data(url, headers, session=None):
    if session==None:
        response = requests.get(url, headers)
    else:
        response = session.get(url)
    response.encoding = "utf-8"
    data = response.text
    return json.loads(data)

def print_line():
    print("--------------------------------------------------------------------------------")

def add_indexers(app):
    searchType = config[app]['type']
    replaceExistent = config[app]['replaceExistent']
    print_encoded('Processing: ' + app) 
    app_indexers_url = config[app]['url'] + config[app]['api_path'] + config[app]['indexer_path']
    app_schema_url  = app_indexers_url + "/schema"
    appkey_query = "?apikey=" + config[app]['apikey']
    
    print_encoded('Getting schema...')
    if verbose:
        print_encoded(app_schema_url + appkey_query)
    app_schemas = get_jsonparsed_data(app_schema_url + appkey_query, {})
    
    print_encoded('Getting current indexers...')
    if verbose:
        print_encoded(app_indexers_url + appkey_query)
    app_indexers = get_jsonparsed_data(app_indexers_url + appkey_query, {})
    
    for schema in app_schemas:
        if schema['implementation'] == "Torznab":
            del schema['presets']
            if verbose:
                print_encoded("Using Json template:")
                print_encoded(json.dumps(schema))
            break
    i = 0
    for tznb in torznabs:
        disabled = False
        onError = False
        priority = 25
        for idxr in indexers:
            if tznb['@id'] == idxr['id']:
                if (idxr['last_error'] != ""):
                    onError = True
                    break
                if ('disabled' in idxr['tags']):
                    disabled = True
                    break
                if 'critical' in idxr['tags']:
                    priority = 1
                elif 'higher' in idxr['tags']:
                    priority = 10
                elif 'lower' in idxr['tags']:
                    priority = 40
                elif 'minimal' in idxr['tags']:
                    priority = 50
                break
        if disabled:
            print(f"{idxr['id']} disabled, skipping...")
            print()
            continue
        if onError:
            print(f"{idxr['id']} on error, skipping...")
            print()
            continue    
        schema['priority'] = priority
        print_encoded(f"Trying to add: {tznb['@id']} to {app} with priority set to {priority}")
        
        if verbose:
            print_encoded(tznb['@id'] + ': ' + json.dumps(tznb))
             
        if tznb['caps']['searching'][searchType]['@available'].lower() == "yes":
            #Does indexer exist ?
            exist = 0
            for app_tznb in app_indexers:
                if tznb['@id'] in app_tznb['name']:
                    exist = app_tznb['id']
                    break
            if exist == 0 or (exist != 0 and replaceExistent):
                schema['name'] = f"{priority} - {tznb['@id']}"
                for k in schema:
                    if k.lower().endswith("rss") or k.lower().endswith("search"):
                        schema[k]= True

                for section in schema['fields']:
                    sectionName = section['name'].lower()
                    if sectionName == "apikey":
                        section['value'] = config['default']['jackett_apikey']
                    if sectionName == "baseurl":
                        section['value'] = jackett_base_url + "/" + tznb['@id'] + "/results/torznab/"
                    if sectionName == "categories":
                        categories = []
                        try:
                            for c in config['app'][tznb['@id']]['categories']:
                                categories.append(int(c))
                            print_encoded("Categories Overrided to: ", categories)
                        except:
                            for p in config[app]['categoryPrefixes']:
                                if type(tznb['caps']['categories']['category']) is list:
                                    catPrefix = tznb['caps']['categories']['category']
                                else:
                                    catPrefix = [tznb['caps']['categories']['category']]
                                for c in catPrefix:
                                    if c['@name'].startswith(p):
                                        categories.append(int(c['@id']))
                        
                        if len(categories) == 0:
                            print_encoded("No Categories found using default...")
                        else:
                            section['value'] = categories

                    if sectionName == "animecategories":
                        anime_categories = []
                        try:
                            for c in categories_override[tznb['@id']]['anime_categories']:
                                anime_categories.append(int(c))
                            print_encoded("Anime Categories Override: " + anime_categories)
                        except:
                            for p in config[app]['animeCategoryPrefixes']:
                                if type(tznb['caps']['categories']['category']) is list:
                                    catPrefix = tznb['caps']['categories']['category']
                                else:
                                    catPrefix = [tznb['caps']['categories']['category']]
                                for c in catPrefix:
                                    if c['@name'].startswith(p):
                                        anime_categories.append(int(c['@id']))

                        if len(anime_categories) > 0:
                            section['value'] = anime_categories
                        else:
                            print_encoded("No Anime Categories found using default...")
                            
                if exist != 0 and replaceExistent:
                    print_encoded(app_tznb['name'] + " already present, removing...")
                    url_del = app_indexers_url + "/" + str(app_tznb['id']) + appkey_query
                    r = requests.delete(url_del)
                    if r.status_code != 200:
                        print(f"[{str(r.status_code)}] Error on removing {str(app_tznb['id'])}")
                    else:
                        exist = 0
                    if verbose:
                        print_encoded(f"[{str(r.status_code)}] DEL {url_del}")
                        if r.status_code != 200:
                            print_encoded(f"response: {json.dumps(r.json())}")
               
                url_add = app_indexers_url + appkey_query
                r = requests.post(url_add, json=schema)
                if r.status_code == 201:
                    print_encoded(f"[{str(r.status_code)}] Added: {tznb['@id']}")
                else:
                    print_encoded(f"[{str(r.status_code)}] Error: {tznb['@id']}")
                if verbose:
                    print_encoded("POST " + url_add)
                    print_encoded(f"request: {json.dumps(schema)}")
                    print_encoded(f"response: {json.dumps(r.json())}")
            else:
                print_encoded(app_tznb['name'] + " already present, skipping...")
        else:
            if verbose:
                print(tznb['caps']['searching'])
            print_encoded(f"{tznb['@id']}: not for {searchType}, skipping...")
        print()

verbose = config['default']['verbose']
print("Started...")
if verbose:
    print_encoded(jackett_torznabs_url)    
all_torznabs = get_jsonparsed_data_from_xml(jackett_torznabs_url, {})
torznabs = [x for x in all_torznabs['indexers']['indexer']]
if verbose:
    print_encoded(json.dumps(torznabs)) 

if verbose:
    print_encoded(jackett_indexers_url)
session = None
if config['default']['jackett_pwd'] != "":
    session = get_jackett_session(config['default']['jackett_pwd'])
indexers = get_jsonparsed_data(jackett_indexers_url, {'X-Api-Key': config['default']['jackett_apikey']}, session)
if verbose:
    print_encoded(json.dumps(indexers))

print_encoded(str(len(torznabs)) + " indexers availlable in Jackett")
print_line()
           
for app in config:
    if app != "default":
        if config[app]['active']:
            add_indexers(app)
        else:
            print(f"{app} is not active, skipping...")
        print_line()
print("Finished...")
