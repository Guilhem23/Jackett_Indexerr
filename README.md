# Jackett_Indexerr
Simple Python script to create and update indexers from Jackett in Radarr, Sonarr and Lidarr

* [Source Project](https://github.com/Guilhem23/Jackett_Indexerr)

## Usage
Follow this https://packaging.python.org/en/latest/tutorials/installing-packages/

***Linux***
- Install virtual environnement
```bash
make pipenv-install
```
- Run script
```bash
make run
```

***Windows***
```bash
pipenv
```
```bash
pip install requests
```

## Configuration

***Run script once to create initial config.json file***
```bash
python add_indexers.py
```

Complete config.json with your own (remove unneeded apps if needed)

```json
{
    "default": {
        "jackett_apikey": "foo",
        "jackett_url": "https://localhost/jackett",
        "indexer_prefix": "AUTO: ",
        "verbose": false
    },
    "sonarr": {
        "active": true,
        "apikey": "foo",
        "url": "https://localhost/sonarr/api/",
        "categoryPrefixes": [
            "TV"
        ],
        "animeCategoryPrefixes": [
            "Anime",
            "TV"
        ],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "tv-search",
        "replaceExistent": false,
        "categories_override": {}
    },
    "radarr": {
        "active": true,
        "apikey": "foo",
        "url": "https://localhost/radarr/api/",
        "categoryPrefixes": [
            "Movies"
        ],
        "animeCategoryPrefixes": [
            "Anime",
            "Movies"
        ],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "tv-search",
        "replaceExistent": false,
        "categories_override": {
            "my_favorite_tracker": {
                "categories": [2000],
                "anime_categories": [5000]
            }
        }
    },
    "lidarr": {
        "active": false,
        "apikey": "foo",
        "url": "https://localhost/lidarr/api/v1/",
        "categoryPrefixes": [
            "Audio"
        ],
        "api_path": "api/v3/",
        "indexer_path": "indexer",
        "type": "audio-search",
        "replaceExistent": false,
        "categories_override": {
            "my_favorite_tracker": {
                "categories": [2000],
                "anime_categories": [5000]
            }
        }
	}
}
```

## Extra
- Added ***verbose*** to print all messages if true
- Added ***api_path*** and ***indexer_path***, if your app version differs one from another
- Included ***type*** on config to skip indexers which caps.searching.[type] is not available
- Removed replacing fields from an existing indexers, instead if replaceExistent is true delete the indexer and add it again
- Created method to add priority to an indexer using tags [critical - 1; higher - 10; lower - 40; minimal - 50], if not set defaut is 25
- Created method to skip if indexer tags contains disabled, or last_error is not empty

## Greetings

Started from code snippet provided by ninnghazad in Jackett Issue

Thanks to ninnghazad for saving me a couple of hours ;)

https://github.com/ninnghazad

https://github.com/Jackett/Jackett/issues/1413
