![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)


# Proyecto individual numero uno

## Introdución

En este proyecto, asumimos el rol de un Ingeniero de MLOps, que es una combinación de un Ingeniero de Datos y un Científico de Datos, para la plataforma global de videojuegos Steam. La tarea consiste en trabajar con conjuntos de datos proporcionados y crear un Producto Mínimo Viable (MVP) que incluya una API desplegada en la nube. Este proyecto aborda dos tareas principales utilizando modelos de Machine Learning: realizar un análisis de sentimientos en los comentarios de los usuarios sobre los juegos y proporcionar recomendaciones de juegos, ya sea a partir del nombre de un juego o de las preferencias de un usuario específico.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

* **users_items.json** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

* **steam_games.json**  es un dataset que contiene datos relacionados con los juegos en sí, como los título, el desarrollador, los precios, características técnicas, etiquetas, entre otros datos.

* **user_reviews.json** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

En el documento [Diccionario de datos] se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas desarrolladas

### Transformaciones

