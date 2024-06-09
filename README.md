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
├── mlops
│   ├── monitoring.py
│   └── train.py
├── model
│   ├── __main__.py
│   ├── monitoring.py
│   ├── preprocessing.py
│   ├── scalers
│   │   ├── loudness.pkl
│   │   └── tempo.pkl
│   └── training.py
├── model.pkl
├── requirements.txt
├── run_docker.sh
├── run_heroku.sh
└── utils
    ├── load_monitoring_data.py
    └── mongo_handler.py
```

Explicación del proyecto: 
1. Modulo App: Se realiza mediante flask el levantamiento de un microservicio que permite la ejecución de métodos POST que entregan las predicciones a través de una request en formato JSON. Además se configuran Cron Job para ir monitoreando de forma períodica el modelo.
2. Modulo Model: Se realiza todo el pipeline del modelo para dejarlo una versión entrada en el proyecto. Se realiza un preprocesamiento, tranining y monitoring.
3. Modulo MLops: Se trabaja la integración de Neptune.ai para ir haciendo pruebas en el modelo se integra con el modulo model lo que permite que el ambos sean escalables. Se realiza un archivo de train donde pueden experimentar los DS las distintas configruaciones y un archivo monitoring donde se crea una clase para ir guardando los datos para el monitoreo en la plataforma.
4. Docker: Se dejó todo configurado para iniciar/crear docker. Falta las variables de ambiente(pedirmelas). Además de que es una excelente herramienta ue permite contener el ambiente creado para la ejecución y
hacerlo reproducible fácilmente para alguien que quiera ejecutarlo.
5. Heroku: Se levantó el servicio aqui ya que permite automatizar el flujo de DevOps de creación de infrastructura. Se dejó código con los pasos de actualización. 
6. MongoDB: Se dejo en utils y se trabajó en una clase que permite en el manejo de esta para ir guardando los datos de las requests/predicciones que se les hace al modelo.

Interacción con el mundo real.
```sh
Aquí lo ideal es dejar el modelo funcionando en algún que se pueda ir consumiento puede ser de forma remota o en la misma maquina que se utilice.
De forma remota se abarca en este caso en donde se levantó un microservicio/api que permite mediante peticiones ir realizando las predicciones.
Para Spotify puede ser de utilizada al momento de que un artista suba una canción clasificarla de manera automatica (mediante el modelo) si es reggeaton o no.
También puede darse que en spotify se quieran hacer listas de recomendaciónd de regeaton para ello tambien se puede realizar un método especifico
que maneje la entrada de una petición con muchas canciones a predecir teniendo cuidado con sobrecargar el microservicio
(habilitar y refactorizar algunas partes para no sobrecargar el modelo) o ejecutarlo de manera periodica. 

En otros casos, como un modelo de recomendación por ejemplo dentro de un ecommerce sería bueno levantar un servicio que pueda permitir dado los datos
realizar una predicciones de producto(s) a recomendar. Una recomendación es definir que acción es la que sirve para ir validando las predicciones.
Por ejemplo si se compró o añadió el producto al carrito ir a rescatar esa información con el objetivo de tener un mejor monitoreo del modelo.
```




