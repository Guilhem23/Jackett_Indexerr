# Configuration management
import configparser

config = configparser.ConfigParser()

try:
    with open('config.ini') as f:
        config.read_file(f)
        if config['default']['jackett_apikey'] == "foo":
            print("please complete config.ini file with your own configuration")
            quit()

except IOError:
    print("config file does not exist creating dummy file. Please conmplete config before running")

    config['default'] = {
        "jackett_apikey" : "foo",
        "jackett_url" : "https://localhost/jackett",
        "indexer_prefix" : "AUTO: "
    }

    config['sonarr'] = {
        "apikey": "foo",
        "url" : "https://localhost/sonarr/api/",
        "categoryPrefixes": ["TV"],
        "animeCategoryPrefixes": ["Anime","TV"]

    }

    config['radarr'] = {
        "apikey": "foo",
        "url" : "https://localhost/radarr/api/",
        "categoryPrefixes": ["Movies"],
        "animeCategoryPrefixes": ["Anime","Movies"]

    }

    config['lidarr'] = {
        "apikey": "foo",
        "url" : "https://localhost/lidarr/api/v1/",
        "categoryPrefixes": ["Audio"],

    }
    with open('config.ini', 'w') as f:
        config.write(f)
        quit()
