# Funciones a usar en main.py
# Importaciones
import pandas as pd
import pyarrow.parquet as pq

df_games_items = pd.read_parquet('Data/df_games_items.parquet')
df_games_reviews = pd.read_parquet('Data/df_games_reviews.parquet')
# Funciones
def presentacion():
    '''
    Genera una página de presentación HTML para la API Steam de consultas de videojuegos.
    
    Returns:
    str: Código HTML que muestra la página de presentación.
    '''
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>¡Explora la API de Steam para obtener información sobre videojuegos! Realiza diversas consultas directamente desde la plataforma.</h1>
            <p>Cómo empezar:</p>
            <p>Agrega  <span style="background-color: lightgray;">/docs</span> al final de la URL actual para explorar e interactuar con la API.</p>
            <p>O simplemente haz clic en el enlace proporcionado para acceder a la documentación</p>
            <p><a href="http://127.0.0.1:8000/docs"><img src="https://www.kindpng.com/picc/m/590-5909635_fastapi-graphic-design-hd-png-download.png" style="width: 75px; height: auto; alt="Fastapi"></a></p>
            <p> Si deseas conocer más sobre el proyecto, puedes visitar mi perfil en<a href="https://www.linkedin.com/in/gerard-carrizo-508b16133/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
            <p> El desarrollo completo está disponible en <a href="https://github.com/IngCarlaPezzone/PI1_MLOps_videojuegos"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
        </body>
    </html>
    '''


def PlayTimeGenre(genre: str):
    """Devuelve el año de lanzamiento con más horas jugadas para el género dado.
    
    Genre: Genero a obtener el número de años de lanzamiento con más horas.
    
    returns: Año de lanzamiento con más horas jugadas para el genero dado teniendo en cuenta los generos disponibles.
    """
    
    genre = genre.capitalize()
    if genre not in df_games_items.columns:
        return {"Error": f"Género {genre} no encontrado en el dataset."}
    else:
        genre_df = df_games_items[df_games_items[genre] == 1]
        year_playtime_df = genre_df.groupby('year')['playtime_forever'].sum().reset_index()
        max_playtime_year = year_playtime_df.loc[year_playtime_df['playtime_forever'].idxmax(), 'year']
        return {"Género": genre, f"Año de lanzamiento con más horas jugadas para Género {genre} :": int (max_playtime_year)} 


def UserForGenre(genre: str) -> dict:
    """Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    
    Genre: Genero a obtener el número de usuarios que han jugado

    Returns:
        Usuario que ha jugado más horas para un género específico teniendo en cuenta los generos disponibles.
    """
    genre = genre.capitalize()
    if genre not in df_games_items.columns:
        return {"Error": f"Género {genre} no encontrado en el dataset."}
    else:
        genre_df = df_games_items[df_games_items[genre] == 1]
        user_playtime_df = genre_df.groupby('user_id')['playtime_forever'].sum().reset_index()
        max_playtime_user = user_playtime_df.loc[user_playtime_df['playtime_forever'].idxmax(), 'user_id']
        return {"Género": genre, f"Usuario con más horas jugadas para Género {genre} :": max_playtime_user}


def UsersRecommend( year : int ):
    """Devuelve el top 3 de juegos más recomendados por usuarios para el año dado.

    Year: Año a obtener los juegos más recomendados

    Returns:
        Lista con los juegos más recomendados para el año dadoy teniendo en cuenta los años que disponemos.
    """
    df_games_reviews['recommend'] = df_games_reviews['recommend'].astype(str)

    if year < 2010 or year > 2015:
        return {"Año": year, "Juegos más recomendados para el año dado": "No hay datos para el año dado"}
    else:
        filtered_df = df_games_reviews[(df_games_reviews['year'] == year) & (df_games_reviews['recommend'] == 'True')]
        if not filtered_df.empty:
            year_df = df_games_reviews[df_games_reviews['year'] == year]
            year_df = year_df.groupby('item_name')['sentiment_score'].sum().reset_index()
            year_df = year_df.sort_values(by='sentiment_score', ascending=False)
            year_df = year_df.head(3)
            return {"Año": year, "Juegos más recomendados para el año dado": year_df['item_name'].tolist()}
        else:
            return {"Año": year, "Juegos más recomendados para el año dado": "No hay datos para el año dado"}



def UsersWorstDeveloper(year: int):
    """Devuelve el top 3 de juegos menos recomendados por usuarios para el año dado.

    Year: Año a obtener los juegos menos recomendados

    Returns:
        Lista con los juegos menos recomendados para el año dado y teniendo en cuenta los años que disponemos.
    """
    df_games_reviews['recommend'] = df_games_reviews['recommend'].astype(str)
    if year < 2010 or year > 2015:
        return {"Año": year, "Juegos menos recomendados para el año dado": "No hay datos para el año dado"}
    else:
        filtered_df = df_games_reviews[(df_games_reviews['posted_year'] == year) & (df_games_reviews['recommend'] == 'False')]
        if not filtered_df.empty:
            year_df = filtered_df.groupby('item_name')['sentiment_score'].sum().reset_index()
            year_df = year_df.sort_values(by='sentiment_score', ascending=True)
            year_df = year_df.head(3)
            return {"Año": year, "Juegos menos recomendados para el año dado": year_df['item_name'].tolist()}
        else:
            return {"Año": year, "Juegos menos recomendados para el año dado": "No hay datos para el año dado"}


def sentiment_analysis( developer: str ):
    """Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    
    Developer: Empresa desarrolladora
    
    Returns:
        Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}, en caso de que no se encuentre ningúna desarrolladora dara como rsultado error.
    """
    df_games_reviews['developer'] = df_games_reviews['developer'].str.capitalize()
    developer = developer.capitalize()
    if developer not in df_games_reviews['developer'].values:
        return {developer: ["No está registrado"]}
    else:
        developer_df = df_games_reviews[df_games_reviews['developer'] == developer]
    
        negative = len(developer_df[developer_df['sentiment_score'] == 0])
        neutral = len(developer_df[developer_df['sentiment_score'] == 1])
        positive = len(developer_df[developer_df['sentiment_score'] == 2])

        return {developer: ["Negative:",negative, "Neutral:", neutral, "Positive:", positive]}