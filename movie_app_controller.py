from fastapi import APIRouter, HTTPException
import pymysql
import pymysql.cursors
from movie1 import Movie1
from movie2 import Movie2

router = APIRouter()

connection = pymysql.connect(
    host="localhost",
    user="rajeev",
    password="Rajeev2005",
    database="movie_app_db",
    cursorclass=pymysql.cursors.DictCursor,
)


@router.get(path="", response_model=list[Movie1])
def get_all_movies():
    with connection.cursor() as cursor:
        query = '''SELECT m.id,image_url, m.name, certificate, imdb_rating, m.likes, l.language, f.label
        FROM movie_app_db.movies as m
        INNER JOIN movie_app_db.language as l
        ON m.language_id = l.id
        INNER JOIN movie_app_db.format as f
        ON m.format_id = f.id'''
        cursor.execute(query=query)
        movies = cursor.fetchall()
        return movies


@router.get(path="/{movie_id}", response_model=Movie2 | dict[str, str])
def get_movie_by_id(movie_id: str) -> Movie2 | dict[str, str]:
    with connection.cursor() as cursor:
        query = '''SELECT m.id,image_url, m.name, certificate, imdb_rating, m.likes, l.language, f.label, g.genre, movie_duration, release_date,m.about
        FROM movie_app_db.movies as m
        INNER JOIN movie_app_db.language as l
        ON m.language_id = l.id
        INNER JOIN movie_app_db.format as f
        ON m.format_id = f.id
        INNER JOIN movie_app_db.movie_genre as mg 
        ON mg.movie_id=m.id
        INNER JOIN movie_app_db.genre as g 
        ON mg.genre_id=g.id
        WHERE m.id=%s'''
        cursor.execute(query=query, args=movie_id)
        movie = cursor.fetchone()
        if movie == None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
