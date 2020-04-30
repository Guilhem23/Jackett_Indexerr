# Jackett_Indexerr
Simple Python script to create and update indexers from Jackett in Radarr, Sonarr and Lidarr

* [Source Project](https://github.com/Guilhem23/Jackett_Indexerr)

## Usage

- Install virtual environnement
```bash
make pipenv-install
```
- Run script
```bash
make run
```

## Configuration

***Run script once to create initial config.ini file***

Complete config.ini with your own (remove unneeded apps if needed)

```python
[default]
jackett_apikey = foo
jackett_url = https://localhost/jackett
indexer_prefix = AUTO: 

[sonarr]
apikey = foo
url = https://localhost/sonarr/api/
categoryprefixes = ['TV']
animecategoryprefixes = ['Anime', 'TV']

[radarr]
apikey = foo
url = https://localhost/radarr/api/
categoryprefixes = ['Movies']
animecategoryprefixes = ['Anime', 'Movies']

[lidarr]
apikey = foo
url = https://localhost/lidarr/api/v1/
categoryprefixes = ['Audio']

```

## Extra

Overriding category for an indexer: edit add_indexer.py and add your own overrides if needed

TODO: move this expert config to config.ini

```python
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
```
## TODO

- Move override to config file
- Update indexer with new values instead of always removing

## Greetings

Started from code snippet provided by ninnghazad in Jackett Issue

Thanks to ninnghazad for saving me a copple of hours ;)

https://github.com/ninnghazad

https://github.com/Jackett/Jackett/issues/1413
