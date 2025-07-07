import json

configPath = './config.json'   
try:
    with open(configPath) as f:
        config = json.load(f)
        if config['default']['jackett_apikey'] == "foo":
            print("please complete config.ini file with your own configuration")
            quit()

except:
    print("config file does not exist creating dummy file. Please complete config before running")
    config = {}
    config['default'] = {
        "jackett_apikey" : "foo",
        "jackett_url" : "https://localhost/jackett",
        "indexer_prefix" : "AUTO: ",
        "verbose": False
    }

    config['sonarr'] = {
        "active": True,
        "apikey": "foo",
        "url" : "https://localhost/sonarr/api/",
        "categoryPrefixes": ["TV"],
        "animeCategoryPrefixes": ["Anime","TV"],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "tv-search",
        "replaceExistent": False,
        "categories_override": {}
    }

    config['radarr'] = {
        "active": True,
        "apikey": "foo",
        "url" : "https://localhost/radarr/api/",
        "categoryPrefixes": ["Movies"],
        "animeCategoryPrefixes": ["Anime","Movies"],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "tv-search",
        "replaceExistent": False,
        "categories_override": {}
    }

    config['lidarr'] = {
        "active": False,
        "apikey": "foo",
        "url" : "https://localhost/lidarr/api/v1/",
        "categoryPrefixes": ["Audio"],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "audio-search",
        "replaceExistent": False,
        "categories_override": {}
    }
    with open(configPath, 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        quit()
