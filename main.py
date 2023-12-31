from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse
import funcion_api as fa

import importlib
importlib.reload(fa)

#Se inicializa la APP
app = FastAPI(debug=True)

#Funciones
@app.get(path="/",
         response_class=HTMLResponse,
         tags=["Inicio"])

def home():
    '''
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return fa.presentacion()

@app.get(path="/PlayTimeGenre",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Responses" para ver el año con más horas jugadas para un género específico teniendo en cuenta los géneros disponibles.
                        </font>
                    """,
         tags=["Consultas Frecuentes"])

def PlayTimeGenre(genre: str = Query(...,
                                     description="Género a obtener el número de años de lanzamiento con más horas",
                                     example="Action")):
    return fa.PlayTimeGenre(genre)

@app.get(path="/UserForGenre",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Responses" para ver el usuario con más horas jugadas para un género específico teniendo en cuenta los géneros disponibles.)
                        </font>
                    """,
            tags=["Consultas Frecuentes"])

def UserForGenre(genre: str = Query(...,
                                     description="Género a obtener el número de usuarios que han jugado",
                                     example="Action")):
    return fa.UserForGenre(genre)

@app.get(path="/UsersRecommend",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese el año en el box abajo.<br>
                        3. Scrollear a "Responses" para ver los juegos más recomendados para el año dado.
                        </font>
                    """,
            tags=["Consultas Frecuentes"])
            
def UsersRecommend( year : int = Query(...,
                                     description="Año a obtener los juegos más recomendados para el año dado",
                                     example=2013)):
    return fa.UsersRecommend(year)

@app.get(path="/UsersWorstDeveloper",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese el año en el box abajo.<br>
                        3. Scrollear a "Responses" para ver los juegos menos recomendados para el año dado.
                        </font>
                    """,
                tags=["Consultas Frecuentes"])

def UsersWorstDeveloper(year : int = Query(...,
                                            description="Año a obtener los juegos menos recomendados para el año dado",
                                            example=2013)):
    return fa.UsersWorstDeveloper(year)

@app.get(path="/sentiment_analysis",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese la empresa desarrolladora en el box abajo.<br>
                        3. Scrollear a "Responses" para ver el análisis de sentimiento de la empresa desarrolladora.
                        </font>
                    """,
                tags=["Análisis de sentimiento"])

def sentiment_analysis(developer: str = Query(...,
                                              description="Empresa desarrolladora a analizar",
                                              example="Valve")):
    return fa.sentiment_analysis(developer)

@app.get(path = "/recomendacion_juego",
         description= """ <front color='blue'>
                        INSTRUCCIONES<br>
                        1. Haga click en "Try it out".<br>
                        2. Ingrese el nombre del juego en el box abajo.<br>
                        3. Scrollear a "Responses" para ver los juegos más recomendados para el juego dado.
                        </font>
                    """,
                tags=["Recomendación"])
def recomendacion_juego(game: str = Query(...,
                                           description="Nombre del juego a recomendar",
                                           example="Counter-strike nexon: zombies")):
    return fa.recomendacion_juego(game)

@app.get('/recomendacion_usuario',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga click en "Try it out".<br>
                    2. Ingrese el id del usuario en box abajo.<br>
                    3. Scrollear a "Responses" para ver los juegos recomendados para ese usuario.
                    </font>
                    """,
         tags=["Recomendación"])
def recomendacion_usuario(user: str = Query(..., 
                                         description="Usuario a partir del cuál se hace la recomendación de los juego", 
                                         example="zeroepix")):
    return fa.recomendacion_usuario(user) 

