from fastapi import FastAPI
import pandas as pd

# Cargar el archivo CSV con el DataFrame modificado
movies_df = pd.read_csv('C:/Users/Jonatan Sivisstum/Desktop/ProyectoIndividualN1/ProyectoN1/movies_modificado.csv')

# Asegurarte de que 'release_date' sea del tipo datetime
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')

# Inicializar FastAPI
app = FastAPI()

# Endpoint para cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses_espanol = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_numero = meses_espanol.get(mes.lower(), None)
    if mes_numero is None:
        return {"error": "Mes no válido"}

    # Filtrar las películas que se estrenaron en el mes
    peliculas_mes = movies_df[movies_df['release_date'].dt.month == mes_numero]
    return {"mensaje": f"{len(peliculas_mes)} cantidad de películas fueron estrenadas en el mes de {mes}"}

# Endpoint para cantidad de filmaciones por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias_espanol = {
        "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
        "viernes": 4, "sábado": 5, "domingo": 6
    }
    dia_numero = dias_espanol.get(dia.lower(), None)
    if dia_numero is None:
        return {"error": "Día no válido"}

    # Filtrar las películas que se estrenaron en el día de la semana
    peliculas_dia = movies_df[movies_df['release_date'].dt.weekday == dia_numero]
    return {"mensaje": f"{len(peliculas_dia)} cantidad de películas fueron estrenadas en los días {dia}"}

# Endpoint para obtener score y título de la película
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    pelicula = movies_df[movies_df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    pelicula = pelicula.iloc[0]
    return {
        "mensaje": f"La película {pelicula['title']} fue estrenada en el año {pelicula['release_year']} con un score/popularidad de {pelicula['popularity']}"
    }

# Endpoint para obtener votos y título de la película
@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = movies_df[movies_df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    
    pelicula = pelicula.iloc[0]
    if pelicula['vote_count'] < 2000:
        return {"mensaje": "La película no tiene suficientes votos (menos de 2000)"}
    
    return {
        "mensaje": f"La película {pelicula['title']} fue estrenada en el año {pelicula['release_year']}. La misma cuenta con un total de {pelicula['vote_count']} valoraciones, con un promedio de {pelicula['vote_average']}"
    }

# Endpoint para obtener datos del actor
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    actor_films = movies_df[movies_df['cast'].str.contains(nombre_actor, case=False, na=False)]
    if actor_films.empty:
        return {"error": "Actor no encontrado"}
    
    cantidad_peliculas = len(actor_films)
    total_retorno = actor_films['revenue'].sum()
    promedio_retorno = actor_films['revenue'].mean()
    
    return {
        "mensaje": f"El actor {nombre_actor} ha participado de {cantidad_peliculas} películas, el mismo ha obtenido un retorno de {total_retorno} con un promedio de {promedio_retorno} por filmación"
    }

# Endpoint para obtener datos del director
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_films = movies_df[movies_df['director'].str.contains(nombre_director, case=False, na=False)]
    if director_films.empty:
        return {"error": "Director no encontrado"}
    
    peliculas = []
    for index, film in director_films.iterrows():
        peliculas.append({
            "titulo": film['title'],
            "fecha_estreno": film['release_date'],
            "retorno": film['revenue'],
            "costo": film['budget'],
            "ganancia": film['revenue'] - film['budget']
        })
    
    return {"mensaje": f"Películas dirigidas por {nombre_director}", "peliculas": peliculas}
