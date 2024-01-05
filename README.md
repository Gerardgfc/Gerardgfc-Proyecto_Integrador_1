![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)
![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)


# Proyecto individual numero uno

## Introducción

En este proyecto, asumimos el rol de un Ingeniero de MLOps, que es una combinación de un Ingeniero de Datos y un Científico de Datos, para la plataforma global de videojuegos Steam. La tarea consiste en trabajar con conjuntos de datos proporcionados y crear un Producto Mínimo Viable (MVP) que incluya una API desplegada en la nube. Este proyecto aborda dos tareas principales utilizando modelos de Machine Learning: realizar un análisis de sentimientos en los comentarios de los usuarios sobre los juegos y proporcionar recomendaciones de juegos, ya sea a partir del nombre de un juego o de las preferencias de un usuario específico.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

* **users_items.json** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

* **steam_games.json**  es un dataset que contiene datos relacionados con los juegos en sí, como los título, el desarrollador, los precios, características técnicas, etiquetas, entre otros datos.

* **user_reviews.json** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticons y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

En el documento [Diccionario de datos](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/00_Diccionario_de_datos.md) se encuentran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas desarrolladas

### Transformaciones

Se completó el proceso de Extracción, Transformación y Carga (ETL) de los tres conjuntos de datos proporcionados. Dos de estos conjuntos de datos presentaban estructuras anidadas, lo que significa que contenían columnas con diccionarios o listas de diccionarios. Para abordar esto, se implementaron diversas estrategias para transformar las claves de estos diccionarios en columnas individuales. Posteriormente, se realizaron acciones de limpieza, como el relleno de valores nulos en variables críticas para el proyecto y la eliminación de columnas con un alto número de valores nulos o que no aportaban de manera significativa al proyecto. Estas acciones se llevaron a cabo con el objetivo de optimizar el rendimiento de la API, considerando las limitaciones de almacenamiento en el entorno de implementación. En todas estas transformaciones, se utilizó la biblioteca Pandas.

Los detalles del ETL se puede ver en [ETL steam_games](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/01_ETL_steam_games.ipynb), [ETL user_reviews](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/02_ETL_user_reviews.ipynb) y [ETL users_items](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/03_ETL_users_items.ipynb).

### Feature engineering

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

* 0 si es malo
* 1 si es neutral o esta sin review
* 2 si es positivo.

Dado que el objetivo de este proyecto es realizar una prueba de concepto, se realiza un análisis de sentimiento básico utilizando **Nltl** que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo. 

Esta metodología toma una revisión de texto como entrada, utiliza **Nltl** para calcular la polaridad de sentimiento y luego clasifica la revisión como negativa, neutral o positiva en función de la polaridad calculada.

Por otra parte, y bajo el mismo criterio de optimizar los tiempos de respuesta de las consultas en la API y teniendo en cuenta las limitaciones de almacenamiento en el servicio de nube para el deploy la API, se realizaron dataframes auxiliares para cada una de las funciones solicitadas. En el mismo sentido, se guardaron estos dataframes en formato *parquet* que permite una compresión y codificación eficiente de los datos.

Todos los detalles del desarrollo se pueden ver en la Jupyter Notebook [04_Feature_Engineering](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/04_Feature%20Engineering.ipynb).

### Análisis exploratorio de los datos

Se realizó el EDA a los tres conjuntos de datos sometidos a ETL con el objetivo de identificar las variables que se pueden utilizar en la creación del modelo de recmendación. Para ello se utilizó la librería Pandas para la manipulación de los datos y las librerías Matplotlib y Seaborn para la visualización.

En particular para el modelo de recomendación, se terminó eligiendo construir un dataframe específico con el id del usuario que realizaron reviews, los nombres de los juegos a los cuales se le realizaron comentarios y una columna de rating que se construyó a partir de la combinación del análisis de sentimiento y la recomendación a los juegos.

El desarrollo de este análisis se encuentra en la Jupyter Notebook [EDA](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/05_EDA.ipynb) 

 ### Modelo de aprendizaje automático

Se crearon dos modelos de recomendación, que generan cada uno, una lista de 5 juegos ya sea ingresando el nombre de un juego o el id de un usuario.

En el primer caso, el modelo tiene una relación ítem-ítem, esto es, se toma un juego y en base a que tan similar es ese juego con el resto de los juegos se recomiendan similares. En el segundo caso, el modelo aplicar un filtro usuario-juego, es decir, toma un usuario, encuentra usuarios similares y se recomiendan ítems que a esos usuarios similares les gustaron.

Para generar estos modelos se adoptaron algoritmos basados en la memoria, los que abordan el problema del **filtrado colaborativo** utilizando toda la base de datos, tratando de encontrar usuarios similares al usuario activo (es decir, los usuarios para los que se les quiere recomendar) y utilizando sus preferencias para predecir las valoraciones del usuario activo.

Para medir la similitud entre los juegos (item_similarity) y entre los usuarios (user_similarity) se utilizó la **similitud del coseno** que es una medida comúnmente utilizada para evaluar la similitud entre dos vectores en un espacio multidimensional. En el contexto de sistemas de recomendación y análisis de datos, la similitud del coseno se utiliza para determinar cuán similares son dos conjuntos de datos o elementos, y se calcula utilizando el coseno del ángulo entre los vectores que representan esos datos o elementos.

El desarrollo para la creación de los dos modelos se presenta en la Jupyter Notebook [05_Modelo_de_recomendacion](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/JupyterNotebooks/06_Modelo_de_recomendacion.ipynb)

 ### Desarrollo de API

 Para el desarrollo de la API se decidió utilizar el framework FastAPI, creando las siguientes funciones:

* **PlayTimeGenre**: Esta función recibe como parámetro un género de videojuego y devuelve el año con mas horas jugadas para dicho género. 

* **UserForGenre**: Esta función recibe como parámetro un género de videojuego y devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

* **UsersRecommend**: Esta función recibe como parámetro un año disponible en el dataframe y devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

* **UsersWorstDeveloper**: Esta función recibe como parámetro un año disponible en el dataframe y devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado.

* **sentiment_analysis**: Esta función recibe como parámetro una desarrolladora y devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

El código para generar la API se encuentra en el archivo [main.py](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/main.py) y las funciones para su funcionamiento se encuentran en [funcion_api.py](https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1/blob/main/funcion_api.py)

- Clonar el proyecto haciendo `https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1.git`.
- Preparación del entorno de trabajo en Visual Studio Code:
    * Crear entorno `Python -m venv env`
    * Ingresar al entorno haciendo `venv\Scripts\activate`
    * Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo main.py desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.
