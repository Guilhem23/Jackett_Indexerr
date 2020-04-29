# Jackett_Indexerr
Simple Python script to create and update indexers from Jackett in Radarr, Sonarr and Lidarr

* [Source Project](https://github.com/Guilhem23/Jackett_Indexerr)

## Configuration

- Complete these values with your own

```python
jackett_apikey = "foo"
jackett_url = "https://localhost/jackett"
indexer_prefix = "AUTO: "
```

- Add or remove application as needed and complete with your own values

```python
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
```

- Overriding category for an indexer: Add your own overrides if needed

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

## Usage

```bash
make pipenv-install

make run
```

## Greatings

Started from code snippet provided by ninnghazad in Jackett Issue

Thanks to ninnghazad for saving me a copple of hours ;)

https://github.com/ninnghazad

https://github.com/Jackett/Jackett/issues/1413
