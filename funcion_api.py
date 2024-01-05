# Funciones a usar en main.py
# Importaciones
import pandas as pd
import operator

df_games_items = pd.read_parquet('Data/df_games_items.parquet')
df_games_reviews = pd.read_parquet('Data/df_games_reviews.parquet')
piv_norm = pd.read_parquet('Data/piv_norm.parquet')
user_sim_df = pd.read_parquet('Data/user_sim_df.parquet')

# Funciones
def presentacion():
    '''
    Genera una página de presentación HTML para la API Steam de consultas de videojuegos.
    
    Returns:
    str: Código HTML que muestra la página de presentación.
    '''
    return '''
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explora la API de Steam</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-image: url('https://i.blogs.es/400138/steam-boicot-reddit/1366_2000.png');
            background-attachment: fixed;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: white;
            padding: 18.5px;
            text-align: center;
        }

        main {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        a {
            color: #007bff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        footer {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background-color: #333;
            color: white;
        }
    </style>
</head>
<body>
    <header>
        <h1>Explora la API de Steam</h1>
    </header>
    
    <main>
        <h2>¡Explora la API de Steam para obtener información sobre videojuegos! Realiza diversas consultas directamente desde la plataforma.</h2>
        
        <h3><strong>Cómo empezar:</strong></h3>
        <ul>
            <li>Agrega <span style="background-color: lightgray;">/docs</span> al final de la URL actual para explorar e interactuar con la API.</li>
            <li>O simplemente hacé <a href="https://proyecto-integrador-1.onrender.com/docs" target="_blank">click acá</a> para acceder a la documentación.</li>
        </ul>

        <p>Si deseas conocer más sobre el proyecto, puedes visitar mi perfil en <a href="https://www.linkedin.com/in/gerard-carrizo-508b16133/" target="_blank">LinkedIn</a>.</p>

        <p>El desarrollo completo está disponible en <a href="https://github.com/Gerardgfc/Gerardgfc-Proyecto_Integrador_1" target="_blank">GitHub</a>.</p>
    </main>
    <br>
    <br>
    <br>
    <br>
    <br>
    <footer>
        <p>&copy; 2023 Gerardo Carrizo</p>
    </footer>
</body>
</html>
    '''


def PlayTimeGenre(genre: str):
    """Devuelve el año de lanzamiento con más horas jugadas para el género dado.
    
    Genre: Genero a obtener el número de años de lanzamiento con más horas.
    
    returns: Año de lanzamiento con más horas jugadas para el genero dado teniendo en cuenta los géneros disponibles.
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
        Usuario que ha jugado más horas para un género específico teniendo en cuenta los géneros disponibles.
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
        Lista con los juegos más recomendados para el año dado teniendo en cuenta los años que disponemos.
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
        Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}, en caso de que no se encuentre ninguna desarrolladora dará como resultado error.
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



def recomendacion_usuario(user):
    '''
    Genera una lista de los juegos más recomendados para un usuario, basándose en las calificaciones de usuarios similares.

    Args:
        user (str): El nombre o identificador del usuario para el cual se desean generar recomendaciones.

    Returns:
        list: Una lista de los juegos más recomendados para el usuario basado en la calificación de usuarios similares.

    '''
    # Verifica si el usuario está presente en las columnas de piv_norm (si no está, devuelve un mensaje)
    if user not in piv_norm.columns:
        return('No data available on user {}'.format(user))
    
    # Obtiene los usuarios más similares al usuario dado
    sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
    
    best = [] # Lista para almacenar los juegos mejor calificados por usuarios similares
    most_common = {} # Diccionario para contar cuántas veces se recomienda cada juego
    
    # Para cada usuario similar, encuentra el juego mejor calificado y lo agrega a la lista 'best'
    for i in sim_users:
        i = str(i)
        max_score = piv_norm.loc[:, i].max()
        best.append(piv_norm[piv_norm.loc[:, i]==max_score].index.tolist())
    
    # Cuenta cuántas veces se recomienda cada juego
    for i in range(len(best)):
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1
            else:
                most_common[j] = 1
    
    # Ordena los juegos por la frecuencia de recomendación en orden descendente
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
    recomendaciones = {} 
    contador = 1 
    # Devuelve los 5 juegos más recomendados
    for juego, _ in sorted_list:
        if contador <= 5:
            recomendaciones[contador] = juego 
            contador += 1 
        else:
            break
    
    return recomendaciones