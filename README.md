# ML MODEL YOM ML OPS DEPLOY HEROKU DOCKER

Este proyecto tiene como por objetivo dejar un modelo hecho en local por DS y dejarlo en un ambiente simulado de producción.

Si quieres probar el servicio te invito a entrar a https://yom-ml-app-0bb04ecda93c.herokuapp.com/

Con el siguiente CURL puedes probar el servicio:

```sh
curl -X POST https://yom-ml-app-0bb04ecda93c.herokuapp.com/predict-song \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "popularity": 60,
      "danceability": 0.607,
      "energy": 0.875,
      "key": 0,
      "loudness": -4.434,
      "mode": 1,
      "speechiness": 0.0605,
      "acousticness": 0.00114,
      "instrumentalness": 0.00765,
      "liveness": 0.467,
      "valence": 0.457,
      "tempo": 131.058,
      "duration": 264520,
      "time_signature": 4,
      "id_new": 2301
    }
  }'
```

El proyecto consiste en 3 tópicos generales:
1. Creación de un modelo de machine, abarcando la creación, preprocesamiento de información y entrenamiento.
2. Creación de un servicio que pueda ser pasado a producción con el fin de que pueda ser utilizado en distintos contextos.
3. Creación de un modulo de MLops que permita experimentar a los DS distintas configuraciones del modelo e ir evaluando la degradación del modelo.

EL proyecto tiene la siguiente estructura:

```
├── Dockerfile
├── Procfile
├── README.md
├── app
│   ├── __main__.py
│   ├── app.py
│   ├── preprocessing.py
│   └── request_example.json
├── data
│   └── t1
│       ├── data_reggaeton.csv
│       ├── data_test.csv
│       └── data_todotipo.csv
├── docker-compose.yml
├── model
│   ├── __main__.py
│   ├── preprocessing.py
│   ├── scalers
│   │   ├── loudness.pkl
│   │   └── tempo.pkl
│   └── training.py
├── model.pkl
├── requirements.txt
├── run_docker.sh
└── run_heroku.sh
```
